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
