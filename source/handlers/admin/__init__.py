from aiogram import Dispatcher, types
from loguru import logger

from source.utils.callback import support_callback


from .answer_support import *



def register_admin_handlers(dp: Dispatcher):
    try:

        dp.register_callback_query_handler(
            ask_admin_for_support_answer,
            # allow any callback data with support_callback
            support_callback.filter(),
            state="*",
        )

        dp.register_message_handler(
            send_support_answer_to_user,
            state=AnswerSupport.wait_for_support_answer,
        )

        register_admin_show_user_handlers(dp)

    except Exception as e:
        logger.error(f"Error while registering admin handlers: {e}")

    else:
        logger.info("Admin handlers registered successfully")
