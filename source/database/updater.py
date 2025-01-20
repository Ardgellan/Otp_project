from loguru import logger

from .connector import DatabaseConnector


class Updater(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Updater object was initialized")

    async def add_days_to_user_subscription(self, user_id: int, days: int) -> bool:
        return True
