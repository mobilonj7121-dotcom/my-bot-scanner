import asyncio
import re
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# ЗАМІНИ ЦЕ НА СВІЙ ТОКЕН ВІД BOTFATHER
API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt9okmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функція для "анти-сну" Render
async def handle(request):
    return web.Response(text="Bot is running")

PHONE_PATTERN = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}'

@dp.message(Command("scaner"))
async def scan_command(message: types.Message):
    args = message.text.replace("/scaner", "").strip()
    phones = re.findall(PHONE_PATTERN, args)
    if phones:
        clean_phones = "\n".join(list(set([p.strip() for p in phones])))
        await message.reply(f"✅ Знайдено номер(и):\n{clean_phones}")
    else:
        await message.reply("❌ Номерів не знайдено.")

async def main():
    # Запуск веб-сервера для Render
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    asyncio.create_task(site.start())
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
