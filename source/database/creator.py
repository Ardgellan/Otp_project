from loguru import logger

from .connector import DatabaseConnector


class Creator(DatabaseConnector):
    def __init__(self):
        super().__init__()
        logger.debug("Creator object was initialized")

    async def recreate_all_tables(self):
        await self._drop_all_tables()
        await self._create_all_tables()

    async def _create_all_tables(self):
        logger.warning("Creating all tables...")
        await self._create_table_sellers()
        await self._create_table_buyers()
        logger.warning("All tables were created")

    async def _drop_all_tables(self):
        table_names = await self._get_all_table_names()
        logger.warning(f"Tables to drop: {table_names}")
        for table_name in table_names:
            await self._drop_table_cascade(table_name)
        logger.warning("All tables were dropped")

    async def _get_all_table_names(self) -> list[str]:
        query = """--sql
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """
        result = await self._execute_query(query)
        return [record["table_name"] for record in result]

    async def _drop_table_cascade(self, table_name: str):
        query = f"""--sql
            DROP TABLE {table_name} CASCADE;
        """
        await self._execute_query(query)
        logger.debug(f"Table {table_name} was dropped")

    async def _create_table_sellers(self):
        query = """--sql
            CREATE TABLE sellers (
                id SERIAL PRIMARY KEY NOT NULL,
                seller_id BIGINT PRIMARY KEY NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
            """

        if await self._execute_query(query) == []:
            logger.debug("Table sellers was created")
        else:
            logger.error("Error while creating table sellers")

    async def _create_table_buyers(self):
        query = """--sql
            CREATE TABLE vpn_configs (
                id SERIAL PRIMARY KEY NOT NULL,
                buyer_id BIGINT NOT NULL REFERENCES users(user_id),
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
            """
        if await self._execute_query(query) == []:
            logger.debug("Table buyers was created")
        else:
            logger.error("Error while creating table buyers")
