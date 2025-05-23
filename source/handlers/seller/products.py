from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from source.utils import localizer
from source.keyboard import inline
from loader import db_manager
from .subscription import check_subscription_active

from source.utils.states.seller_states import ProductInputFlow

@check_subscription_active()
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


# Обработчик для ввода имени товара
# async def handle_product_name(message: types.Message, state: FSMContext):
#     logger.debug("Salam_2")
#     # Получаем имя товара от пользователя
#     product_name = message.text
#     # Сохраняем его в состояние FSM
#     await state.update_data(product_name=product_name)

#     # Переходим к запросу ID товара
#     await request_user_for_product_id(message, state)


async def handle_product_name(message: types.Message, state: FSMContext):
    logger.debug("Salam_2")
    product_name = message.text.strip()

    # Проверка: непустое и не только цифры
    if not product_name or product_name.isdigit():
        await message.answer("❌ Имя товара не может быть пустым или состоять только из цифр. Попробуйте снова.")
        await ProductInputFlow.waiting_for_product_name.set()  # ВОТ ЭТО ДОБАВЬ
        return

    if len(product_name) > 128:
        await message.answer("❌ Имя товара слишком длинное. Максимум 128 символов.")
        await ProductInputFlow.waiting_for_product_name.set()  # ВОТ ЭТО ДОБАВЬ
        return

    await state.update_data(product_name=product_name)
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


# # Обработчик для ввода ID товара
# async def handle_product_id(message: types.Message, state: FSMContext):
#     logger.debug("Salam_4")
#     # Получаем ID товара от пользователя
#     product_id = message.text
#     # Сохраняем его в состояние FSM
#     await state.update_data(product_id=product_id)

#     # Переходим к запросу OTP товара
#     await request_user_for_product_otp(message, state)


async def handle_product_id(message: types.Message, state: FSMContext):
    logger.debug("Salam_4")
    product_id_text = message.text.strip()

    # Проверка: число
    if not product_id_text.isdigit():
        await message.answer("❌ ID товара должен быть числом. Пожалуйста, введите корректный ID.")
        await ProductInputFlow.waiting_for_product_id.set()
        return

    product_id = int(product_id_text)

    # Проверка: диапазон
    if product_id <= 0 or product_id > 999999999999:
        await message.answer("❌ Неверный диапазон ID товара. Попробуйте другое значение.")
        await ProductInputFlow.waiting_for_product_id.set()
        return

    await state.update_data(product_id=product_id)
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


# # Обработчик для ввода OTP товара
# async def handle_product_otp(message: types.Message, state: FSMContext):
#     logger.debug("Salam_6")
#     # Получаем OTP от пользователя
#     product_otp = message.text
#     # Сохраняем его в состояние FSM
#     await state.update_data(product_otp=product_otp)

#     # После того как все данные собраны, вызываем функцию для добавления товара в БД
#     await add_product_to_db_and_notify(message, state)


async def handle_product_otp(message: types.Message, state: FSMContext):
    logger.debug("Salam_6")
    product_otp = message.text.strip()

    if not product_otp:
        await message.answer("❌ OTP не может быть пустым.")
        await ProductInputFlow.waiting_for_product_otp.set()
        return

    if len(product_otp) > 50:
        await message.answer("❌ OTP слишком длинный. Максимум 50 символов.")
        await ProductInputFlow.waiting_for_product_otp.set()
        return

    await state.update_data(product_otp=product_otp)
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
        # Извлекаем ID товара из callback_data (например, "delete_product_12345")
        product_id_str = call.data.split("_")[-1]

        # Проверяем и преобразуем в int
        product_id = int(product_id_str)
        logger.debug(f"Извлечён product_id: {product_id}")

        # Удаляем товар из базы данных
        await db_manager.delete_product_by_id(
            seller_id=call.from_user.id,
            product_id=product_id
        )
        logger.info(f"Товар с ID {product_id} успешно удалён.")

        # Уведомляем пользователя об успехе
        await call.message.edit_text(
            text=localizer.get_user_localized_text(
                user_language_code=call.from_user.language_code,  # исправлено: параметр должен называться user_language_code
                text_localization=localizer.message.product_successfully_deleted_message,
            ),
            parse_mode=types.ParseMode.HTML,
            reply_markup=await inline.insert_button_back_to_main_menu(language_code=call.from_user.language_code)
        )
        await call.answer()

    except ValueError:
        logger.error("Неверный формат product_id в callback_data.")
        await call.message.answer("Ошибка: неверный формат ID товара.")
        await call.answer()

    except Exception as e:
        logger.error(f"Ошибка при удалении товара: {e}")
        await call.message.answer(
            text="Произошла ошибка при удалении товара. Попробуйте позже.",
            parse_mode=types.ParseMode.HTML,
        )
        await call.answer()
