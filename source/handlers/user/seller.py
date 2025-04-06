from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from source.utils import localizer
from source.keyboard import inline
from loader import db_manager

async def seller_start_menu(call: types.CallbackQuery, state: FSMContext):
    logger.debug("Salam")
    await db_manager.upsert_seller(
        seller_id=call.from_user.id,
    )
    
    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.seller_menu_message,
        ),
        reply_markup=await inline.seller_keyboard(
            language_code=call.from_user.language_code,
        )
    )