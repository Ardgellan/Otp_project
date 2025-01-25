from aiogram import types
from aiogram.dispatcher import FSMContext

from source.utils import localizer
from source.keyboard import inline

async def start(message: types.Message):
    await message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=message.from_user.language_code,
            text_localization=localizer.message.greetings_message,
        ),
        reply_markup=await inline.start_menu_kb(
            language_code=message.from_user.language_code,
        )
    )

async def main_menu_by_button(message: types.Message):
    await message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=message.from_user.language_code,
            text_localization=localizer.message.greetings_message,
        ),
        reply_markup=await inline.start_menu_kb(
            language_code=message.from_user.language_code,
        )
    )