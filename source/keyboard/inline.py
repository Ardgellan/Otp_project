from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db_manager
from source.data import config
from source.utils import localizer
from source.utils.callback import support_callback

from loguru import logger

async def start_menu_kb(language_code: str):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.main_menu_button,
            ),
            callback_data="main_menu_button",
        ),
    ]

    for button in buttons:
        keyboard.insert(button)

    return keyboard

