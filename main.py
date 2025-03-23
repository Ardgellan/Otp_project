# from aiogram import executor

# async def on_startup(dp):
#     import time

#     from loguru import logger
#     from source import handlers

#     logger.add(
#         f'logs/{time.strftime("%Y-%m-%d__%H-%M")}.log',
#         level="DEBUG",
#         rotation="500 MB",
#         compression="zip",
#     )

#     handlers.setup(dp)

#     logger.success("[+] Bot started successfully")



# if __name__ == "__main__":
#     # Launch
#     from aiogram import executor

#     from source.handlers import dp

#     executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

import time
import asyncio
import threading
from flask import Flask, request
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Update
from loguru import logger

# === Конфигурация ===
WEBAPP_HOST = "0.0.0.0"  # Хост для Flask
WEBAPP_PORT = 5000       # Порт Flask

# === Логирование ===
logger.add(
    f'logs/{time.strftime("%Y-%m-%d__%H-%M")}.log',
    level="DEBUG",
    rotation="500 MB",
    compression="zip",
)

# === Создаем бота и Flask ===
app = Flask(__name__)

# === Обработчик Вебхуков (Flask) ===
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        update = Update(**data)
        asyncio.create_task(dp.process_update(update))  # Асинхронная обработка
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Ошибка вебхука: {e}")
        return {"error": "Ошибка обработки"}, 500

# === Функция запуска Flask в потоке ===
def run_flask():
    app.run(host=WEBAPP_HOST, port=WEBAPP_PORT, debug=False, use_reloader=False)

# === Функция запуска бота ===
async def on_startup(dp):
    from source import handlers
    handlers.setup(dp)
    logger.success("[+] Bot started successfully")

# === Точка входа ===
if __name__ == "__main__":

    from aiogram import executor
    from source.handlers import dp

    # Запускаем Flask в отдельном потоке
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Запускаем Telegram-бота
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
