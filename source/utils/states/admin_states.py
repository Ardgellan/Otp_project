from aiogram.dispatcher.filters.state import State, StatesGroup


class AnswerSupport(StatesGroup):
    wait_for_support_answer = State()