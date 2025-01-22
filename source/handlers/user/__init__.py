from aiogram import Dispatcher

from loader import dp

def register_user_handlers(dp: Dispatcher):
    try:

        dp.register_message_handler(start, commands=["start"], state="*")

    except Exception as e:
        logger.error(f"Error while registering user handlers: {e}")
    else:
        logger.info("User handlers registered successfully")