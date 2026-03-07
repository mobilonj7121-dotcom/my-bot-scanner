import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# ТВІЙ ТОКЕН
API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt78vU8m-62M2-S-N0w0W_A'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Ця функція потрібна, щоб Render бачив, що бот працює
async def handle(request):
    return web.Response(text="Bot is Live!")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привіт! Я твій бот-сканер. Напиши /scaner [номер], щоб почати.")

@dp.message(Command("scaner"))
async def cmd_scaner(message: types.Message):
    await message.answer("🔎 Починаю сканування... Записів не знайдено.")

async def main():
    # Налаштування веб-сервера для Render (порт 10000)
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    
    # Запуск сервера та бота одночасно
    await asyncio.gather(
        site.start(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
  
