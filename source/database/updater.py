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

        
    # async def update_product_by_id(self, seller_id: int, product_id: int, new_product_name: str, new_product_id: str, new_product_otp: str):
    #     query = """
    #         UPDATE products
    #         SET product_name = $1, product_id = $2, product_otp = $3
    #         WHERE seller_id = $4 AND id = $5
    #     """
    #     await self._execute_query(query, new_product_name, new_product_id, new_product_otp, seller_id, product_id)


    async def update_product_by_id(self, seller_id: int, product_id: int, new_product_name: str, new_product_id: int, new_product_otp: str):
        logger.debug(f"Обновление товара в БД: seller_id={seller_id}, product_id={product_id}, "
                    f"new_product_name={new_product_name}, new_product_id={new_product_id}, new_product_otp={new_product_otp}")

        query = """
            UPDATE products
            SET product_name = $1, product_id = $2, product_otp = $3
            WHERE seller_id = $4 AND product_id = $5
        """

        result = await self._execute_query(query, new_product_name, new_product_id, new_product_otp, seller_id, product_id)
        logger.debug(f"Результат выполнения update запроса: {result}")


