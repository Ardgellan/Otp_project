from aiogram import types
from aiogram.dispatcher import FSMContext

from source.utils import localizer

async def start(message: types.Message):
    await message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=message.from_user.user_language_code,
            text_localization=localizer.message.payment_confirmation_message,
        )
    )