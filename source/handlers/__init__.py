from aiogram import Dispatcher

from loader import dp

from .user import register_seller_handlers


def setup(dp: Dispatcher):
    register_seller_handlers(dp)
