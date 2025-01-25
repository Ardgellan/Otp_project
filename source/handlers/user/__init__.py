from aiogram import Dispatcher
from loguru import logger

from loader import dp

from .start import *

def register_user_handlers(dp: Dispatcher):
    try:

        dp.register_message_handler(start, commands=["start"], state="*")

        dp.register_callback_query_handler(
            main_menu_by_button,
            lambda call: call.data == "main_menu_button",
            state="*",
        )

    except Exception as e:
        logger.error(f"Error while registering user handlers: {e}")
    else:
        logger.info("User handlers registered successfully")