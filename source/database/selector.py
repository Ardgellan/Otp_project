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
