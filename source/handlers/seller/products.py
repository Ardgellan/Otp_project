from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from source.utils import localizer
from source.keyboard import inline
from loader import db_manager

from source.utils.states.seller_states import ProductInputFlow

async def request_user_for_product_name(call: types.CallbackQuery, state: FSMContext):
    logger.debug("Salam_1")
    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.request_product_name_message,
        ),
        parse_mode=types.ParseMode.HTML,
    )
    await ProductInputFlow.waiting_for_product_name.set()
    await call.answer()


# Обработчик для ввода имени товара
async def handle_product_name(message: types.Message, state: FSMContext):
    logger.debug("Salam_2")
    # Получаем имя товара от пользователя
    product_name = message.text
    # Сохраняем его в состояние FSM
    await state.update_data(product_name=product_name)

    # Переходим к запросу ID товара
    await request_user_for_product_id(message, state)


async def request_user_for_product_id(message: types.Message, state: FSMContext):
    logger.debug("Salam_3")
    await message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=message.from_user.language_code,
            text_localization=localizer.message.request_product_id_message,
        ),
        parse_mode=types.ParseMode.HTML,
    )
    logger.debug("Balam_3")
    await ProductInputFlow.waiting_for_product_id.set()
    await call.answer()


# Обработчик для ввода ID товара
async def handle_product_id(message: types.Message, state: FSMContext):
    logger.debug("Salam_4")
    # Получаем ID товара от пользователя
    product_id = message.text
    # Сохраняем его в состояние FSM
    await state.update_data(product_id=product_id)

    # Переходим к запросу OTP товара
    await request_user_for_product_otp(message, state)


async def request_user_for_product_otp(message: types.Message, state: FSMContext):
    logger.debug("Salam_5")
    await message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=message.from_user.language_code,
            text_localization=localizer.message.request_product_otp_message,
        ),
        parse_mode=types.ParseMode.HTML,
    )
    await ProductInputFlow.waiting_for_product_otp.set()
    await call.answer()


# Обработчик для ввода OTP товара
async def handle_product_otp(message: types.Message, state: FSMContext):
    logger.debug("Salam_6")
    # Получаем OTP от пользователя
    product_otp = message.text
    # Сохраняем его в состояние FSM
    await state.update_data(product_otp=product_otp)

    # После того как все данные собраны, вызываем функцию для добавления товара в БД
    await add_product_to_db_and_notify(message, state)


# Функция для добавления товара в БД и уведомления пользователя
async def add_product_to_db_and_notify(message: types.Message, state: FSMContext):
    logger.debug("Salam_7")
    # Получаем данные из состояния FSM
    data = await state.get_data()

    # Логирование для проверки данных
    logger.info(f"Полученные данные от пользователя {message.from_user.id}: {data}")

    # Пример добавления товара в БД (здесь должен быть твой реальный метод для добавления)
    try:
        await db_manager.add_product(
            seller_id=message.from_user.id,
            product_name=data['product_name'],
            product_id=data['product_id'],
            product_otp=data['product_otp']
        )
        logger.info(f"Товар {data['product_name']} добавлен в БД успешно.")

        # Отправляем пользователю сообщение об успешном добавлении
        await message.answer(
            text=localizer.get_user_localized_text(
                user_language_code=message.from_user.language_code,
                text_localization=localizer.message.product_successfully_added_message
            ),
            parse_mode=types.ParseMode.HTML,
        )

        # Завершаем процесс FSM
        await state.finish()

    except Exception as e:
        logger.error(f"Ошибка при добавлении товара в БД: {e}")
        await message.answer(
            text=localizer.get_user_localized_text(
                user_language_code=message.from_user.language_code,
                text_localization=localizer.message.error_adding_product_message
            ),
            parse_mode=types.ParseMode.HTML,
        )
        await state.finish()


async def show_product_info(call: types.CallbackQuery, state: FSMContext):
    try:
        logger.debug(f"Received callback data: {call.data}")

        product_id_str = call.data.split("_")[1]
        logger.debug(f"Extracted product_id: {product_id_str}")

        product_id = int(product_id_str)
        product = await db_manager.get_product_by_id(product_id)

        logger.debug(f"Product fetch result: {product}")

        if product:
            text = (
                f"🛒 <b>{product['product_name']}</b>\n"
                f"🆔 ID: <code>{product['product_id']}</code>\n"
                f"🔐 OTP: <code>{product['product_otp']}</code>\n"
                f"📅 Добавлено: {product['created_at'].strftime('%Y-%m-%d %H:%M')}"
            )
        else:
            text = "❌ Товар не найден."
            logger.warning(f"Product with ID {product_id} not found in database.")

        await call.answer()
        await call.message.answer(
            text,
            parse_mode="HTML",
            reply_markup=await inline.specific_product_keyboard(
                language_code=call.from_user.language_code,
                product_id=product_id
            )
        )

    except Exception as e:
        logger.error(f"Exception in show_product_info: {e}", exc_info=True)
        await call.answer()
        await call.message.answer("⚠️ Произошла ошибка при получении информации о товаре.")



# async def edit_product_info(call: types.CallbackQuery, state: FSMContext):


async def confirm_delete_product(call: types.CallbackQuery, state: FSMContext):
    logger.debug("Функция удаление подтверждение 1")
    # await call.message.delete()
    product_id = call.data.split("_")[-1]
    logger.debug("Функция удаление подтверждение 2")
    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.confirm_delete_product_message,
        ),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.confirm_delete_product_keyboard(
            product_id=product_id, language_code=call.from_user.language_code
        ),
    )
    logger.debug("Функция удаление подтверждение 3")



async def delete_product(call: types.CallbackQuery, state: FSMContext):
    logger.debug("Начинается процесс удаления товара.")

    try:
        # Получаем ID товара из callback_data (например, "delete_12345")
        product_id = call.data.split("_")[1]

        # Удаляем товар (предполагается, что есть метод delete_product_by_id)
        await db_manager.delete_product_by_id(
            seller_id=call.from_user.id,
            product_id=product_id
        )
        logger.info(f"Товар с ID {product_id} успешно удалён.")

        # Уведомляем пользователя
        await call.message.edit_text(
            text=localizer.get_user_localized_text(
                user_language_code=call.from_user.language_code,
                text_localization=localizer.message.product_successfully_deleted_message,
            ),
            parse_mode=types.ParseMode.HTML,
            reply_markup=await inline.insert_button_back_to_main_menu(language_code=language_code)
        )
        await call.answer()

    except Exception as e:
        logger.error(f"Ошибка при удалении товара: {e}")
        await call.message.answer(
            text="Произошла ошибка при удалении товара. Попробуйте позже.",
            parse_mode=types.ParseMode.HTML,
        )
        await call.answer()