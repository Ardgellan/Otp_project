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


    async def activate_trial_period(self, seller_id: int, months: int, conn=None) -> bool:
        query = f"""
            UPDATE sellers
            SET 
                subscription_is_active = TRUE,
                subscription_until = NOW() + INTERVAL '{months} months',
                last_subscription_payment = NOW(),
                trial_is_used = TRUE
            WHERE seller_id = {seller_id}
            AND trial_is_used = FALSE;
        """
        try:
            if conn:
                result = await conn.execute(query)
            else:
                result = await self._execute_query(query)
            
            if result is False or (hasattr(result, "rowcount") and result.rowcount == 0):
                logger.warning(f"Триал уже использован или ошибка при активации для пользователя {seller_id}")
                return False
            
            logger.info(f"Пробный период активирован для пользователя {seller_id}")
            return True

        except Exception as e:
            logger.error(f"Ошибка при активации пробного периода для пользователя {seller_id}: {e}")
            return False

        
    async def update_product(self, seller_id: int, product_db_id: int, name: str, product_id: str, otp: str):
        query = """
            UPDATE products
            SET product_name = $1, product_id = $2, product_otp = $3
            WHERE seller_id = $4 AND id = $5
        """
        await self._execute_query(query, name, product_id, otp, seller_id, product_db_id)

