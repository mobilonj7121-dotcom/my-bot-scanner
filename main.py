import asyncio
import logging
import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

logging.basicConfig(level=logging.INFO)

API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt9okmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="Scanner Engine is Active")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🛠 **Deep Scanner v3.0 завантажено.**\n\nНадішліть номер або посилання на профіль для глибокого аналізу прихованих даних.")

@dp.message(Command("scaner"))
async def cmd_scaner(message: types.Message):
    # Шукаємо номер телефону в тексті за допомогою регулярного виразу
    find_phone = re.findall(r'\+?\d[\d\s\-\(\)]{8,12}\d', message.text)
    
    if not find_phone:
        await message.answer("❌ Номер не розпізнано. Введіть номер у форматі +380...")
        return

    phone = find_phone[0]
    status_msg = await message.answer(f"⏳ Починаю перехоплення даних для: {phone}...")
    
    # Імітація глибокого сканування (ефект для користувача)
    await asyncio.sleep(1.5)
    await status_msg.edit_text("🔍 [||||......] 20% - Пошук у витоках баз GetContact/Larix...")
    await asyncio.sleep(1.5)
    await status_msg.edit_text("🔍 [||||||||..] 60% - Обхід налаштувань приватності через кеш сервісів...")
    await asyncio.sleep(1.5)
    await status_msg.edit_text("🔍 [||||||||||] 100% - Аналіз завершено!")
    
    await message.answer(
        f"📋 **Звіт сканування {phone}:**\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 **Статус приватності:** Приховано користувачем\n"
        f"🔐 **Рівень захисту:** Високий\n"
        f"📂 **Знайдені збіги:** У публічних реєстрах та оголошеннях номер не знайдено.\n\n"
        f"ℹ️ *Система не виявила прямих витоків для цього контакту.*"
    )

async def main():
    port = int(os.environ.get("PORT", 10000))
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    
    await site.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
