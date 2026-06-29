import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

# Імпортуємо нашу функцію з файлу Scaner.py
from Scaner import fetch_data 

# Завантажуємо токен з прихованого файлу .env
load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

# Налаштовуємо логування
logging.basicConfig(level=logging.INFO)

# Ініціалізуємо бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    text = (
        "Привіт! 👋 Я твій Бот-Сканер.\n\n"
        "Надішли мені команду у форматі:\n"
        "`/scan [посилання]`\n\n"
        "Приклад: `/scan https://google.com`"
    )
    await message.reply(text, parse_mode="Markdown")

@dp.message_handler(commands=['scan'])
async def scan_website(message: types.Message):
    # Отримуємо посилання, яке користувач написав після /scan
    url = message.get_args()
    
    if not url:
        await message.reply("⚠️ Ти забув додати посилання! Напиши, наприклад: `/scan https://google.com`", parse_mode="Markdown")
        return
    
    await message.reply("🔍 Сканую сайт, зачекай секунду...")
    
    # Викликаємо логіку з Scaner.py
    result = fetch_data(url)
    
    # Відправляємо результат назад у Telegram
    await message.reply(result)

if __name__ == '__main__':
    print("Бот запущений і готовий до роботи!")
    executor.start_polling(dp, skip_updates=True)
    
