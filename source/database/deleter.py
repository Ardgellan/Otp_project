from loguru import logger

from .connector import DatabaseConnector


class Deleter(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Deleter object was initialized")

    async def delete_seller(self, seller_id: int) -> None:
        query = f"""--sql
            DELETE FROM sellers
            WHERE seller_id = {seller_id};
        """
        await self._execute_query(query)
        logger.debug(f"Seller {seller_id} was deleted")

    async def delete_seller(self, buyer_id: int) -> None:
        query = f"""--sql
            DELETE FROM buyers
            WHERE buyer_id = {buyer_id};
        """
        await self._execute_query(query)
        logger.debug(f"Buyer {buyer_id} was deleted")


    async def delete_product_by_id(self, seller_id: int, product_id: int) -> None:
        query = """
            DELETE FROM products
            WHERE seller_id = $1 AND product_id = $2;
        """
        await self._execute_query(query, seller_id, product_id)
        logger.debug(f"Product {product_id} for seller {seller_id} was deleted")

    
    async def deactivate_seller_subscription(self, seller_id: int) -> bool:
        """
        Помечает подписку продавца как неактивную.
        """
        query = """
            UPDATE sellers
            SET subscription_is_active = FALSE
            WHERE seller_id = $1
        """
        try:
            await self._execute_query(query, seller_id)
            logger.debug(f"Subscription for seller {seller_id} marked as inactive.")
            return True
        except Exception as e:
            logger.error(f"Failed to deactivate subscription for seller {seller_id}: {e}")
            return False
    

    async def delete_seller_data(self, seller_id: int):
        """
        Удаляет все данные продавца, включая его заказы и товары, но саму запись продавца сохраняет.
        """
        queries = [
            "DELETE FROM orders WHERE seller_id = $1",
            "DELETE FROM products WHERE seller_id = $1"
            # Таблица sellers намеренно НЕ трогаем
        ]
        try:
            async with self._db_pool.acquire() as conn:
                async with conn.transaction():
                    for query in queries:
                        await conn.execute(query, seller_id)
            logger.info(f"Seller {seller_id} and related data deleted successfully.")
        except Exception as e:
            logger.error(f"Failed to delete seller {seller_id} data: {e}")
            raise

