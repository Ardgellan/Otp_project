from aiogram import Dispatcher
from loguru import logger

from loader import dp


def register_seller_handlers(dp: Dispatcher):
    try:

    except Exception as e:
        logger.error(f"Error while registering seller handlers: {e}")
    else:
        logger.info("Seller handlers registered successfully")