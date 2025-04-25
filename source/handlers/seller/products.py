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


async def show_product_info(callback_query: CallbackQuery):
    product_id = int(callback_query.data.split("_")[1])
    product = await db_manager.get_product_by_id(product_id)

    if product:
        text = (
            f"🛒 <b>{product['product_name']}</b>\n"
            f"🆔 ID: <code>{product['product_id']}</code>\n"
            f"🔐 OTP: <code>{product['product_otp']}</code>\n"
            f"📅 Добавлено: {product['created_at'].strftime('%Y-%m-%d %H:%M')}"
        )
    else:
        text = "❌ Товар не найден."

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text, parse_mode="HTML")
