import asyncio
import aiohttp

from datetime import datetime, timedelta
from aiogram.utils.exceptions import BotBlocked
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from aiogram import types

from loader import bot, db_manager
from source.utils import localizer
from source.utils.models import SubscriptionStatus

class SubscriptionChecker:
    def __init__(self):
        self._messages_limits_counter = 0
        self._scheduler = AsyncIOScheduler()
        # start checking subscriptions every day at 12:00;
        self._scheduler.add_job(self._check_subscriptions, "cron", hour=12, minute=0)
        self._scheduler.start()
        logger.info("Subscription checker was started...")

    async def _check_subscriptions(self):
        """Проверяем подписки пользователей"""        
        # Блок в котором мы блокируем истекших селлеров
        sellers_expiration_list = await db_manager.get_sellers_with_subscriptions_expired() # Это список селлеров на "Первичное" отключение
                                                                                                   # Первичное отключение, это когда мы блокируем продавцам и их покупателям
                                                                                                   # доступ к основному функционалу, но еще не удаляем их товары и заказы из БД
        if sellers_expiration_list:
            await self._disconnect_expired_sellers(sellers_expiration_list)

        last_day_expiration_sellers = await db_manager.get_sellers_ids_with_last_day_left_subscription_expiration()
        last_two_days_expiration_sellers = await db_manager.get_sellers_ids_with_two_days_left_subscription_expiration()

        if last_two_days_expiration_sellers:
            await self._find_and_notify_sellers_with_last_two_days_left_subscription(sellers_ids=last_two_days_expiration_sellers, phase="expiration")
        if last_day_expiration_sellers:
            await self._find_and_notify_sellers_with_last_day_left_subscription(sellers_ids=last_day_expiration_sellers, phase="expiration")


        # Блок в котором мы удаляем истекших селлеров
        sellers_termination_list = await db_manager.get_sellers_to_terminate() # По прошествии двух недель после того как подписка была приостановлена а селлерам
                                                                               # и их покупателям заблочен доступ к основному функционалу, мы снова отправляем уведомление за
                                                                               # два дня до, за день до и в последний день, отправляем уведомление и теперь уже удаляем все
                                                                               # товары и заказы ассоциированные с продавцом
        
        if sellers_termination_list:
            await self._terminate_expired_sellers(sellers_termination_list)

        last_day_termination_sellers = await db_manager.get_sellers_ids_with_last_day_left_subscription_termination()
        last_two_days_termination_sellers = await db_manager.get_sellers_ids_with_two_days_left_subscription_termination()

        if last_two_days_termination_sellers:
            await self._find_and_notify_sellers_with_last_two_days_left_subscription(sellers_ids=last_two_days_termination_sellers, phase="termination")
        if last_day_termination_sellers:
            await self._find_and_notify_sellers_with_last_day_left_subscription(sellers_ids=last_day_termination_sellers, phase="termination")
        
        self._messages_limits_counter = 0


    async def _disconnect_expired_sellers(self, seller_ids: list[int]):
        """
        Первичное отключение селлеров — деактивация подписки и нотификация.
        """
        for seller_id in seller_ids:
            try:
                await db_manager.deactivate_seller_subscription(seller_id)
                logger.info(f"Seller {seller_id} subscription marked as inactive")
            except Exception as e:
                logger.error(f"Failed to deactivate seller {seller_id}: {e}")

        # Уведомляем всех пачкой (по статусу expired)
        await self._notify_users_about_subscription_status(
            users_ids=seller_ids,
            status=SubscriptionStatus.expired
        )


    async def _terminate_expired_sellers(self, seller_ids: list[int]):
        """
        Полное удаление селлеров и уведомление об этом.
        """
        for seller_id in seller_ids:
            try:
                await db_manager.delete_seller_data(seller_id)
                logger.info(f"Seller {seller_id} and related data deleted")
            except Exception as e:
                logger.error(f"Failed to delete data for seller {seller_id}: {e}")

        # Уведомляем всех о терминации
        await self._notify_users_about_subscription_status(
            users_ids=seller_ids,
            status=SubscriptionStatus.terminated  # Нужен такой статус и сообщение
        )


    async def _find_and_notify_sellers_with_last_two_days_left_subscription(self, sellers_ids: list[int], phase: str):
        if phase == "expiration":
            status = SubscriptionStatus.last_two_days_left_expiration
        elif phase == "termination":
            status = SubscriptionStatus.last_two_days_left_termination
        else:
            raise ValueError(f"Unknown phase: {phase}")

        await self._notify_users_about_subscription_status(users_ids=sellers_ids, status=status)


    async def _find_and_notify_sellers_with_last_day_left_subscription(self, sellers_ids: list[int], phase: str):
        if phase == "expiration":
            status = SubscriptionStatus.last_day_left_expiration
        elif phase == "termination":
            status = SubscriptionStatus.last_day_left_termination
        else:
            raise ValueError(f"Unknown phase: {phase}")

        await self._notify_users_about_subscription_status(users_ids=sellers_ids, status=status)



    async def _notify_users_about_subscription_status(self, users_ids: list[int], status: SubscriptionStatus):
        """Notify users about subscription status"""

        match status:
            case SubscriptionStatus.expired:
                message_text = localizer.message.subscription_expired_notification_message
            case SubscriptionStatus.last_day_left_expiration:
                message_text = localizer.message.subscription_last_day_left_notification_message
            case SubscriptionStatus.last_two_days_left_expiration:
                message_text = localizer.message.subscription_last_two_days_left_notification_message
            
            case SubscriptionStatus.terminated:
                message_text = localizer.message.subscription_terminated_notification_message
            case SubscriptionStatus.last_day_left_termination:
                message_text = localizer.message.subscription_last_day_left_termination_notification_message
            case SubscriptionStatus.last_two_days_left_termination:
                message_text = localizer.message.subscription_last_two_days_left_termination_notification_message

            case _:
                raise ValueError(f"Unknown subscription status: {status}")

        tasks = []
        for user_id in users_ids:
            tasks.append(self._send_subscription_notification(user_id, message_text))
        await asyncio.gather(*tasks)


    async def _send_subscription_notification(self, user_id: int, message_text: str):
        """Helper function to send notification to a single user"""
        try:
            user = (await bot.get_chat_member(chat_id=user_id, user_id=user_id)).user
  
            await bot.send_message(
                chat_id=user_id,
                text=localizer.get_user_localized_text(
                    user_language_code=user.language_code,
                    text_localization=message_text,
                ).format(user=user.full_name),
                parse_mode=types.ParseMode.HTML,
            )
        except BotBlocked:
            logger.error(f"Bot was blocked by user {user_id}")
        except Exception as e:
            logger.error(e)
        else:
            logger.info(f"User {user_id} was notified about subscription status")
        finally:
            self._messages_limits_counter += 1
            if self._messages_limits_counter == 20:
                await asyncio.sleep(1)
                self._messages_limits_counter = 0
