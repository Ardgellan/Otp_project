from flask import Flask, request, abort
from loguru import logger
import json
import asyncio

# Импортируем уже инициализированные компоненты из loader.py
from loader import bot  # импортируем глобально инициализированный объект bot
from source.handlers.user.start import test_function


# Настройка Flask
app = Flask(__name__)

def configure_flask_logging():
    flask_logger = logging.getLogger('flask')  # Получаем логгер Flask
    flask_logger.setLevel(logging.INFO)  # Устанавливаем уровень логирования
    flask_logger.addHandler(logging.StreamHandler(sys.stdout))  # Перенаправляем логи во внешний вывод (консоль)
    # Перенаправляем все логи в loguru
    flask_logger.addHandler(logger._handlers[0])  # Это добавляет обработчик loguru для перенаправления логов

# Перенастроим Flask для использования loguru
configure_flask_logging()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработчик Webhook (без проверок)."""
    data = request.get_json()

    logger.info(f"Received data: {json.dumps(data, indent=2)}")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(execute_test_function())  
    loop.close()

    return 'success', 200

async def execute_test_function():
    # Запускаем вашу функцию start
    await test_function()  # start должна использовать глобально инициализированный bot


if __name__ == '__main__':
    # Запуск Flask сервера
    app.run(host="0.0.0.0", port=5000)