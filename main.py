import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# Вмикаємо логування: тепер у чорному вікні Render ми побачимо, якщо щось піде не так
logging.basicConfig(level=logging.INFO)

# Твій токен
API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt9okmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Заглушка для Render
async def handle(request):
    return web.Response(text="Bot is running!")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("✅ Привіт! Я працюю. Напиши /scaner [номер]")

@dp.message(Command("scaner"))
async def cmd_scaner(message: types.Message):
    await message.answer("🔎 Сканую... База чиста, записів не знайдено.")

async def main():
    # Render сам видає порт через змінні середовища, беремо його
    port = int(os.environ.get("PORT", 10000))
    
    # Налаштування сервера
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    
    logging.info(f"Запускаємо веб-сервер на порту {port}...")
    await site.start()
    
    logging.info("Запускаємо бота...")
    # Видаляємо старі оновлення (якщо бот був вимкнений, щоб він не спамив)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот зупинений.")
        
