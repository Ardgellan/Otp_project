from aiogram import Dispatcher

from loader import dp

from .seller import register_seller_handlers
from .admin import register_admin_handlers

def setup(dp: Dispatcher):
    register_seller_handlers(dp)
