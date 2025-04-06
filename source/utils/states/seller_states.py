from aiogram.dispatcher.filters.state import State, StatesGroup

class ProductInputFlow(StatesGroup):
    waiting_for_product_name = State()
    waiting_for_product_id = State()
    waiting_for_product_otp = State()


class AskSupport(StatesGroup):
    waiting_for_question = State()
