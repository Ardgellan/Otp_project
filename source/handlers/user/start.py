from aiogram import types
from aiogram.dispatcher import FSMContext

from source.utils import localizer

async def start(message: types.Message):
    await message.answer(
        text=localizer.message.greetings_message
    )