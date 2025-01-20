from loguru import logger

from .connector import DatabaseConnector


class Inserter(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Inserter object was initialized")

    async def upsert_user(self, user_id: int, username: str):
        query = f"""--sql
                INSERT INTO users (user_id, username, subscription_end_date)
                VALUES ({user_id},'{username}', DATE '2030-01-01')
                ON CONFLICT (user_id)
                DO UPDATE SET username = '{username}', subscription_end_date = DATE '2030-01-01';
            """

        await self._execute_query(query)

        logger.debug(f"User {user_id} was upserted")
