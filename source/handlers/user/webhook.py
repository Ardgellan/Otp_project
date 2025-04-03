from flask import Flask, request, abort
from loguru import logger
import json
import asyncio

# Импортируем уже инициализированные компоненты из loader.py
from loader import bot  # импортируем глобально инициализированный объект bot
from source.handlers.user import start  # импортируем вашу логику старта


# Настройка Flask
app = Flask(__name__)

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     if request.method == 'POST':
#         # Получаем данные от Digiseller в формате JSON
#         data = request.get_json()

#         # Логируем полученные данные для отладки
#         logger.info(f"Received data: {json.dumps(data, indent=2)}")

#         # Проверяем статус от Digiseller, который должен быть 200 или успешное событие
#         if data.get('status') == 200:  # Предположим, что статус в ответе Digiseller = 200
#             # Запускаем вашу логику (выполняем функцию start)
#             asyncio.create_task(execute_start())  # Запуск асинхронной задачи

#             return 'success', 200
#         else:
#             logger.error(f"Received unexpected status: {data.get('status')}")
#             return 'failure', 400
#     else:
#         abort(400)


@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработчик Webhook (без проверок)."""
    data = request.get_json()

    logger.info(f"Received data: {json.dumps(data, indent=2)}")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(execute_start())  
    loop.close()

    return 'success', 200

async def execute_start():
    # Запускаем вашу функцию start
    await start()  # start должна использовать глобально инициализированный bot


if __name__ == '__main__':
    # Запуск Flask сервера
    app.run(host="0.0.0.0", port=5000)