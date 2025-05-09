from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db_manager
from source.data import config
from source.utils import localizer
from source.utils.callback import support_callback

from loguru import logger


async def insert_button_back_to_main_menu(
    keyboard: InlineKeyboardMarkup | None = None, language_code: str = "ru"
):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.main_menu_button,
            ),
            callback_data="main_menu_button",
        )
    )
    return keyboard


async def start_menu_kb(language_code: str):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.seller_button,
            ),
            callback_data="seller_button",
        ),
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.buyer_button,
            ),
            callback_data="buyer_button",
        ),
    ]

    for button in buttons:
        keyboard.insert(button)

    keyboard = await insert_button_back_to_main_menu(keyboard=keyboard, language_code=language_code)

    return keyboard


async def seller_keyboard(language_code: str):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.trial_period_button,
            ),
            callback_data="trial_period_button",
        ),
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.pay_subscription_button,
            ),
            callback_data="pay_subscription_button",
        ),
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.status_subscription_button,
            ),
            callback_data="status_subscription_button",
        ),
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.my_products_button,
            ),
            callback_data="my_products_button",
        ),
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.add_product_button,
            ),
            callback_data="add_product_button",
        ),
    ]

    for button in buttons:
        keyboard.insert(button)

    keyboard = await insert_button_back_to_main_menu(keyboard=keyboard, language_code=language_code)

    return keyboard


async def seller_products_list_keyboard(seller_id: int, language_code: str) -> InlineKeyboardMarkup:
    # Получаем продукты продавца
    logger.debug("Salam klaviatura prodavca_1")
    seller_products = await db_manager.get_seller_products(seller_id)
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = [
        InlineKeyboardButton(
        text=localizer.get_user_localized_text(
            user_language_code=language_code,
            text_localization=localizer.button.add_product_button,
        ),
        callback_data="add_product_button",
    ),
    ]

    keyboard.add(*buttons)

    # Добавляем кнопки с товарами, если они есть
    if seller_products:
        product_buttons = [
            InlineKeyboardButton(
                text=product["product_name"],
                callback_data=f"product_{product['product_id']}",
            )
            for product in seller_products
        ]
        keyboard.add(*product_buttons)

    # Кнопка "Назад в главное меню"
    keyboard = await insert_button_back_to_main_menu(keyboard=keyboard, language_code=language_code)

    return keyboard

async def specific_product_keyboard(product_id: int, language_code: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    buttons = [
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.edit_product_button,
            ),
            callback_data=f"edit_product_{product_id}",
        ),
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.delete_product_button,
            ),
            callback_data=f"delete_product_{product_id}",
        ),
    ]

    keyboard.add(*buttons)

    keyboard = await insert_button_back_to_main_menu(keyboard=keyboard, language_code=language_code)

    return keyboard


async def confirm_delete_product_keyboard(product_id: int, language_code: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    button = InlineKeyboardButton(
        text=localizer.get_user_localized_text(
            user_language_code=language_code,
            text_localization=localizer.button.confirm_delete_button,
        ),
        callback_data=f"delete_product_{product_id}"
    )

    keyboard.add(*button)

    keyboard = await insert_button_back_to_main_menu(keyboard=keyboard, language_code=language_code)

    return keyboard