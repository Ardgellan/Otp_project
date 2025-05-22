from loguru import logger

from .connector import DatabaseConnector


class Updater(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Updater object was initialized")

    async def extend_user_subscription(self, seller_id: int, months: int, conn=None) -> bool:
        query = f"""
            UPDATE sellers
            SET 
                subscription_is_active = TRUE,
                subscription_until = (
                    CASE 
                        WHEN subscription_until > NOW() THEN subscription_until + INTERVAL '{months} months'
                        ELSE NOW() + INTERVAL '{months} months'
                    END
                ),
                last_subscription_payment = NOW()
            WHERE seller_id = {seller_id};
        """
        try:
            if conn:
                await conn.execute(query)
            else:
                if await self._execute_query(query) is False:
                    logger.error(f"Ошибка при продлении подписки пользователя {seller_id}")
                    return False
            logger.debug(f"Подписка пользователя {seller_id} продлена на {months} мес.")
            return True
        except Exception as e:
            logger.error(f"Исключение при продлении подписки пользователя {seller_id}: {e}")
            return False
