from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from source.utils import localizer
from source.keyboard import inline
from loader import db_manager


async def trial_period_func(call: types.CallbackQuery, state: FSMContext):
    logger.debug("TRIAL_1")
    sub_is_active = await db_manager.is_subscription_active(call.from_user.id)
    logger.debug("TRIAL_2")
    try:
        if not sub_is_active:
            await call.message.answer(
                text=localizer.get_user_localized_text(
                    user_language_code=call.from_user.language_code,
                    text_localization=localizer.message.trial_period_message
                ),
                parse_mode=types.ParseMode.HTML,
                reply_markup=await inline.trial_period_keyboard(
                    language_code=call.from_user.language_code
                )
            )
        else:
            await call.message.answer(
                text=localizer.get_user_localized_text(
                    user_language_code=call.from_user.language_code,
                    text_localization=localizer.message.trial_period_refusal_message
                ),
                parse_mode=types.ParseMode.HTML,
                reply_markup=await inline.insert_button_back_to_main_menu(
                    language_code=call.from_user.language_code
                )
            )
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

    await call.answer()


async def trial_period_activation_func(call: types.CallbackQuery, state: FSMContext):
    
    await db_manager.extend_user_subscription(seller_id=call.from_user.id, months=1)

    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.trial_period_activated_message
        ),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.insert_button_back_to_main_menu(
            language_code=call.from_user.language_code
        )
    )
    
    await call.answer()