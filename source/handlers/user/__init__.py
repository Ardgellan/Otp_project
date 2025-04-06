from aiogram import Dispatcher
from loguru import logger

from loader import dp

from .start import *
from .seller import *
from .products import *

def register_user_handlers(dp: Dispatcher):
    try:
        dp.register_message_handler(start, commands=["start"], state="*")

        dp.register_callback_query_handler(
            main_menu_by_button,
            lambda call: call.data == "main_menu_button",
            state="*",
        )

        dp.register_callback_query_handler(
            seller_start_menu,
            lambda call: call.data == "seller_button",
            state="*",
        )

        # FSM-хендлер: старт добавления продукта
        dp.register_callback_query_handler(
            request_user_for_product_name,
            lambda call: call.data == "add_product_button",  # кнопка должна иметь такой data
            state="*"
        )

         # Обработчики для каждого этапа ввода данных
        dp.register_message_handler(
            handle_product_name,
            state=ProductInputFlow.waiting_for_product_name
        )

        dp.register_message_handler(
            handle_product_id,
            state=ProductInputFlow.waiting_for_product_id
        )

        dp.register_message_handler(
            handle_product_otp,
            state=ProductInputFlow.waiting_for_product_otp
        )

    except Exception as e:
        logger.error(f"Error while registering user handlers: {e}")
    else:
        logger.info("User handlers registered successfully")