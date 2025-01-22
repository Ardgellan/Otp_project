from aiogram import types
from aiogram.dispatcher import FSMContext

async def start(message: types.Message):
    await message.answer(
        text="Salam"
    )