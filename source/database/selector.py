from datetime import datetime

from loguru import logger

from source.data import config

from .connector import DatabaseConnector


class Selector(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Selector object was initialized")

    async def is_seller_registered(self, user_id: int) -> bool:
        query = f"""--sql
            SELECT EXISTS(
                SELECT 1
                FROM sellers
                WHERE seller_id = {seller_id}
            );
        """
        result = await self._execute_query(query)
        logger.debug(f"Seller {seller_id} exist: {result[0][0]}")
        return result[0][0]


    async def get_seller_products(self, seller_id: int) -> list[dict]:
        query = """
            SELECT product_name, product_id
            FROM products
            WHERE seller_id = $1;
        """
        result = await self._execute_query(query, seller_id)
        logger.debug(f"Found {len(result)} products for seller {seller_id}")

        products = [
            {
                "product_name": row[0],
                "product_id": row[1],
            }
            for row in result
        ]
    
        return products


    async def get_product_by_id(self, product_id: int) -> dict | None:
        query = """
            SELECT product_name, product_id, product_otp, created_at
            FROM products
            WHERE product_id = $1;
        """
        result = await self._execute_query(query, product_id)
        if result:
            row = result[0]
            return {
                "product_name": row[0],
                "product_id": row[1],
                "product_otp": row[2],
                "created_at": row[3],
            }
        return None


    async def is_subscription_active(self, seller_id: int) -> bool:
        query = f"""
            SELECT subscription_is_active
            FROM sellers
            WHERE seller_id = {seller_id};
        """
        result = await self._execute_query(query)
        if result:
            return result[0][0]  # True или False из базы
        return False  # Если записи нет — подписки тоже нет


    async def get_subscription_info(self, seller_id: int) -> dict | None:
        query = """
            SELECT last_subscription_payment, subscription_until
            FROM sellers
            WHERE seller_id = $1;
        """
        result = await self._execute_query(query, seller_id)
        if result:
            row = result[0]
            return {
                "last_subscription_payment": row[0],
                "subscription_until": row[1],
            }
        return None

    
    async def get_sellers_with_subscriptions_expired(self) -> list[int]:
        query = """
            SELECT seller_id
            FROM sellers
            WHERE subscription_until < NOW()
              AND subscription_is_active = TRUE;
        """
        result = await self._execute_query(query)
        if result:
            seller_ids = [row[0] for row in result]
            logger.debug(f"Found {len(seller_ids)} sellers with expired subscriptions")
            return seller_ids
        logger.debug("No sellers with expired subscriptions found")
        return []

    
    async def get_sellers_to_terminate(self) -> list[int]:
        query = """
            SELECT seller_id
            FROM sellers
            WHERE subscription_is_active = FALSE
                AND subscription_until + INTERVAL '14 days' < NOW();
        """
        result = await self._execute_query(query)
        sellers = [row[0] for row in result] if result else []
        logger.debug(f"Found {len(sellers)} sellers to terminate (delete)")
        return sellers

    
    async def get_sellers_ids_with_last_day_left_subscription_expiration(self) -> list[int]:
        query = """
            SELECT seller_id
            FROM sellers
            WHERE subscription_is_active = TRUE
                AND DATE(subscription_until) = DATE(NOW() + INTERVAL '1 day')
        """
        result = await self._execute_query(query)
        sellers = [row[0] for row in result] if result else []
        logger.debug(f"Found {len(sellers)} sellers with 1 day left before subscription expiration")
        return sellers


    async def get_sellers_ids_with_two_days_left_subscription_expiration(self) -> list[int]:
        query = """
            SELECT seller_id
            FROM sellers
            WHERE subscription_is_active = TRUE
                AND DATE(subscription_until) = DATE(NOW() + INTERVAL '2 day')
        """
        result = await self._execute_query(query)
        sellers = [row[0] for row in result] if result else []
        logger.debug(f"Found {len(sellers)} sellers with 2 days left before subscription expiration")
        return sellers

    
    async def get_sellers_ids_with_last_day_left_subscription_termination(self) -> list[int]:
        """
        Возвращает seller_id, у которых остался 1 день до терминации подписки (после отключения).
        """
        query = """
            SELECT seller_id
            FROM sellers
            WHERE subscription_is_active = FALSE
            AND DATE(subscription_until + INTERVAL '14 days') = DATE(NOW() + INTERVAL '1 day');
        """
        result = await self._execute_query(query)
        sellers = [row[0] for row in result] if result else []
        logger.debug(f"Found {len(sellers)} sellers with 1 day left before subscription termination")
        return sellers


    async def get_sellers_ids_with_two_days_left_subscription_termination(self) -> list[int]:
        """
        Возвращает seller_id, у которых осталось 2 дня до терминации подписки (после отключения).
        """
        query = """
            SELECT seller_id
            FROM sellers
            WHERE subscription_is_active = FALSE
            AND DATE(subscription_until + INTERVAL '14 days') = DATE(NOW() + INTERVAL '2 days');
        """
        result = await self._execute_query(query)
        sellers = [row[0] for row in result] if result else []
        logger.debug(f"Found {len(sellers)} sellers with 2 days left before subscription termination")
        return sellers


    async def is_trial_used(self, seller_id: int) -> bool:
        query = "SELECT trial_is_used FROM sellers WHERE seller_id = $1"
        try:
            async with self._db_pool.acquire() as conn:
                result = await conn.fetchval(query, seller_id)
                return result is True
        except Exception as e:
            logger.error(f"Ошибка при проверке использования триала для seller_id {seller_id}: {e}")
            return True  # на всякий случай лучше по дефолту True, чтобы не дать триал


