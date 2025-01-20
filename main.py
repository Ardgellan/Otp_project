import telebot
import pyotp
import time

from source.data import config

# Замените на ваш токен и секретный ключ
API_TOKEN = config.bot_token
TOTP_SECRET = config.totp_secret

bot = telebot.TeleBot(API_TOKEN)

# Хранение разрешённых пользователей (ID Telegram)
AUTHORIZED_USERS = {470464896}  # Укажите свой ID

# Генерация TOTP кода
def generate_totp():
    totp = pyotp.TOTP(TOTP_SECRET)
    return totp.now()

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in AUTHORIZED_USERS:
        bot.reply_to(message, "Привет! Отправь /code, чтобы получить TOTP код.")
    else:
        bot.reply_to(message, "Извините, у вас нет доступа к этому боту.")

# Команда /code
@bot.message_handler(commands=['code'])
def send_code(message):
    if message.chat.id in AUTHORIZED_USERS:
        code = generate_totp()
        bot.reply_to(message, f"Ваш код: {code}")
    else:
        bot.reply_to(message, "У вас нет доступа к этой команде.")

# Запуск бота
print("Бот запущен...")
bot.polling()