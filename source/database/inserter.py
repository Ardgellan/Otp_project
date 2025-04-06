from loguru import logger
import random
from datetime import datetime


from .connector import DatabaseConnector


class Inserter(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Inserter object was initialized")


    async def upsert_seller(self, seller_id: int):
        query = f"""--sql
            INSERT INTO sellers (seller_id)
            VALUES ({seller_id})
            ON CONFLICT (seller_id)
            DO NOTHING;
        """
        await self._execute_query(query)
        logger.debug(f"User {seller_id} was upserted (if not already exists)")



    async def insert_fake_sellers_data(self, num_entries: int = 1):
        """Вставка фейковых данных в таблицу sellers."""
    
        for _ in range(num_entries):
            seller_id = random.randint(1000, 9999)  # Генерация случайного seller_id
            order_id = random.randint(10000, 99999)  # Генерация случайного order_id
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Используем текущее время

            query = f"""--sql
                INSERT INTO sellers (seller_id, order_id, created_at)
                VALUES ({seller_id}, {order_id}, '{created_at}');
            """
        
            await self._execute_query(query)
            logger.debug(f"Inserted fake seller_id: {seller_id}, order_id: {order_id} at {created_at}")

        logger.info(f"Inserted {num_entries} fake entries into sellers table.")
