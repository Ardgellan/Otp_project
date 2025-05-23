from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from loader import db_manager
from source.utils.states.seller_states import ProductEditFlow
from source.utils import localizer
from source.keyboard import inline
from loguru import logger


async def start_edit_product(call: CallbackQuery, state: FSMContext):
    product_id = int(call.data.split("_")[-1])
    product = await db_manager.get_product_by_id(product_id)

    if not product:
        await call.answer("❌ Товар не найден")
        return

    await state.update_data(
        edit_product_id=product_id,
        product_name=product['product_name'],
        product_id_value=product['product_id'],
        product_otp=product['product_otp']
    )

    await call.message.answer(
        f"Редактирование товара: <b>{product['product_name']}</b>\n"
        f"Введите новое название или повторите текущее:",
        parse_mode="HTML"
    )
    await ProductEditFlow.waiting_for_product_name.set()
    await call.answer()


# async def handle_edit_product_name(message: types.Message, state: FSMContext):
#     await state.update_data(product_name=message.text)

#     await message.answer("Введите новый ID товара или повторите текущий:")
#     await ProductEditFlow.waiting_for_product_id.set()
#     await call.answer()


async def handle_edit_product_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    
    if not name:
        await message.answer("❌ Название товара не может быть пустым. Пожалуйста, введите корректное имя.")
        return  # Остаёмся в том же состоянии, чтобы пользователь исправил
    
    if len(name) > 100:
        await message.answer("❌ Слишком длинное название. Максимум 100 символов.")
        return

    await state.update_data(product_name=name)
    await message.answer("Введите новый ID товара или повторите текущий:")
    await ProductEditFlow.waiting_for_product_id.set()


# async def handle_edit_product_id(message: types.Message, state: FSMContext):
#     await state.update_data(product_id_value=message.text)

#     await message.answer("Введите новый OTP товара или повторите текущий:")
#     await ProductEditFlow.waiting_for_product_otp.set()
#     await call.answer()


async def handle_edit_product_id(message: types.Message, state: FSMContext):
    user_input = message.text.strip()

    if not user_input.isdigit():
        await message.answer("❌ Ошибка: ID товара должен содержать только цифры. Попробуйте ещё раз.")
        return  # Не меняем состояние, просим ввести заново

    product_id_int = int(user_input)
    await state.update_data(product_id_value=product_id_int)

    # Переходим к следующему шагу или даём подтверждение и так далее
    await message.answer("Введите OTP для товара:")
    await ProductEditFlow.waiting_for_product_otp.set()


# async def handle_edit_product_otp(message: types.Message, state: FSMContext):
#     await state.update_data(product_otp=message.text)
#     data = await state.get_data()
#     logger.debug(f"Данные для обновления товара: {data}")
#     try:
#         await db_manager.update_product_by_id(
#             seller_id=message.from_user.id,
#             product_id=data['edit_product_id'],
#             new_product_name=data['product_name'],
#             new_product_id=data['product_id_value'],
#             new_product_otp=data['product_otp']
#         )

#         await message.answer(
#             text="✅ Товар успешно обновлён.",
#             parse_mode="HTML",
#             reply_markup=await inline.insert_button_back_to_main_menu(
#                 language_code=message.from_user.language_code
#             )
#         )
#         await state.finish()

#     except Exception as e:
#         logger.error(f"Ошибка при обновлении товара: {e}")
#         await message.answer("❌ Произошла ошибка при обновлении товара.")
#         await state.finish()


async def handle_edit_product_otp(message: types.Message, state: FSMContext):
    otp = message.text.strip()

    # Проверяем, что otp не пустой
    if not otp:
        await message.answer("❌ OTP не может быть пустым. Пожалуйста, введите корректное значение.")
        return  # Остаёмся в том же состоянии

    # Максимальная длина
    if len(otp) > 50:
        await message.answer("❌ OTP слишком длинный. Максимум 20 символов.")
        return

    await state.update_data(product_otp=otp)
    data = await state.get_data()
    logger.debug(f"Данные для обновления товара: {data}")
    try:
        await db_manager.update_product_by_id(
            seller_id=message.from_user.id,
            product_id=data['edit_product_id'],
            new_product_name=data['product_name'],
            new_product_id=data['product_id_value'],
            new_product_otp=data['product_otp']
        )

        await message.answer(
            text="✅ Товар успешно обновлён.",
            parse_mode="HTML",
            reply_markup=await inline.insert_button_back_to_main_menu(
                language_code=message.from_user.language_code
            )
        )
        await state.finish()

    except Exception as e:
        logger.error(f"Ошибка при обновлении товара: {e}")
        await message.answer("❌ Произошла ошибка при обновлении товара.")
        await state.finish()
