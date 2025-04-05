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
        await self._create_table_orders()
        await self._create_table_products()
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


    async def _create_table_orders(self):
        query = """--sql
            CREATE TABLE orders (
                id SERIAL PRIMARY KEY NOT NULL,
                id_i BIGINT NOT NULL,
                id_d BIGINT NOT NULL,
                amount DECIMAL(10, 2),
                currency VARCHAR(5),
                buyer_email VARCHAR(50),
                date TIMESTAMP NOT NULL DEFAULT NOW()
            );
            """
        if await self._execute_query(query) == []:
            logger.debug("Table orders was created")
        else:
            logger.error("Error while creating table orders")

    
    async def _create_table_products(self):
        query = """--sql
            CREATE TABLE orders (
                id SERIAL PRIMARY KEY NOT NULL,
                seller_id BIGINT NOT NULL,
                product_id BIGINT NOT NULL,
                product_otp VARCHAR(128) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
            """
        if await self._execute_query(query) == []:
            logger.debug("Table products was created")
        else:
            logger.error("Error while creating table products")


    async def _create_table_sellers(self):
        query = """--sql
            CREATE TABLE sellers (
                id SERIAL PRIMARY KEY NOT NULL,
                seller_id BIGINT NOT NULL,
                subscription_is_active BOOLEAN NOT NULL DEFAULT FALSE,
                last_subscription_payment TIMESTAMP NOT NULL DEFAULT TO_TIMESTAMP(0),
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
            """

        if await self._execute_query(query) == []:
            logger.debug("Table sellers was created")
        else:
            logger.error("Error while creating table sellers")


    async def _create_table_buyers(self):
        query = """--sql
            CREATE TABLE buyers (
                id SERIAL PRIMARY KEY NOT NULL,
                buyer_id BIGINT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
            """
        if await self._execute_query(query) == []:
            logger.debug("Table buyers was created")
        else:
            logger.error("Error while creating table buyers")
