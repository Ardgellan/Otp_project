from aiogram import Dispatcher

from loader import dp

from .user import register_user_handlers


def setup(dp: Dispatcher):
    register_user_handlers(dp)
