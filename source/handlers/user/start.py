from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from source.utils import localizer
from source.keyboard import inline
from loader import db_manager

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

async def main_menu_by_button(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.greetings_message,
        ),
        reply_markup=await inline.start_menu_kb(
            language_code=call.from_user.language_code,
        )
    )
async def test_function():
    """Временная функция для проверки работы вебхука"""
    logger.info("✅ Webhook вызван, асинхронная функция запущена!")
    
    # Здесь вы вызываете метод для вставки фейковых данных
    await db_manager.insert_fake_sellers_data(num_entries=1)

    logger.info("✅ Фейковые данные успешно вставлены!")