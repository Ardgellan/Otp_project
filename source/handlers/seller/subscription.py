from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger
from functools import wraps 

from source.utils import localizer
from source.keyboard import inline
from loader import db_manager


async def subscription_status(call: types.CallbackQuery, state: FSMContext):
    seller_id = call.from_user.id
    lang = call.from_user.language_code

    # Получаем статус подписки
    is_active = await db_manager.is_subscription_active(seller_id)
    status_emoji = '🟢' if is_active else '🔴'

    # Получаем подробную информацию о подписке
    info = await db_manager.get_subscription_info(seller_id)
    if info and is_active:
        last_payment = info["last_subscription_payment"].strftime("%d.%m.%Y %H:%M")
        subscription_until = info["subscription_until"].strftime("%d.%m.%Y %H:%M")
    else:
        last_payment = "N/A"
        subscription_until = "N/A"

    # Получаем текст с локализацией
    text = localizer.get_user_localized_text(
        user_language_code=lang,
        text_localization=localizer.message.subscription_status_message,
    ).format(
        sub_status=status_emoji,
        last_sub_payment=last_payment,
        sub_expiration=subscription_until
    )

    # Отправляем сообщение
    await call.message.answer(
        text=text,
        reply_markup=await inline.insert_button_back_to_main_menu(language_code=lang),
        parse_mode=types.ParseMode.HTML,
    )


def check_subscription_active():
    def decorator(func):
        @wraps(func)
        async def wrapper(call: types.CallbackQuery, *args, **kwargs):

            is_active = await db_manager.is_subscription_active(call.from_user.id)
            if not is_active:
                await call.message.answer(
                    text=localizer.get_user_localized_text(
                    user_language_code=call.from_user.language_code,
                    text_localization=localizer.message.subscription_required_message,
                ),
                    reply_markup=await inline.insert_button_back_to_main_menu(language_code=call.from_user.language_code),
                    parse_mode=types.ParseMode.HTML,
                )
                return  # ⛔ Прекращаем выполнение целевой функции

            return await func(call, *args, **kwargs)

        return wrapper
    return decorator