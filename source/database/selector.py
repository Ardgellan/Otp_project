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


