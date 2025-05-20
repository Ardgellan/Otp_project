from loguru import logger

from .connector import DatabaseConnector


class Updater(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Updater object was initialized")

    async def extend_user_subscription(self, seller_id: int, months: int):
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
        await self._execute_query(query)
        logger.debug(f"Подписка пользователя {seller_id} продлена на {months} мес.")

