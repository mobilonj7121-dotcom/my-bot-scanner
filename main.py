import asyncio
import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# Твій перевірений токен
API_TOKEN = '8509672441:AAHQ3q-RpIh5GtokmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="Scanner Active")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🛠 **Deep Scanner v3.0 активовано.**\n\nНадішліть номер для пошуку прихованих даних та обходу приватності.")

@dp.message(Command("scaner"))
async def cmd_scaner(message: types.Message):
    # Шукаємо будь-які цифри (номер) у повідомленні
    find_phone = re.findall(r'\+?\d[\d\s\-\(\)]{8,12}\d', message.text)
    
    if not find_phone:
        await message.answer("⚠️ Введіть номер телефону після команди /scaner")
        return

    phone = find_phone[0]
    status_msg = await message.answer(f"📡 З'єднання з сервером... Обробка {phone}")
    
    # Ефект обходу приватності
    await asyncio.sleep(1)
    await status_msg.edit_text("🔍 [||||......] 30% - Обхід налаштувань Telegram Privacy...")
    await asyncio.sleep(1)
    await status_msg.edit_text("📡 [||||||||..] 70% - Пошук у кеші GetContact та витоках баз...")
    await asyncio.sleep(1)
    await status_msg.edit_text("✅ [||||||||||] 100% - Дані отримано!")
    
    await message.answer(
        f"📋 **Звіт для {phone}:**\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 **Власник:** Приховано (Deep Stealth Mode)\n"
        f"🔒 **Приватність:** Обхід виконано через цифрові сліди\n"
        f"📂 **Знайдені записи:** Номер активний, але прямих збігів у злитих реєстрах не виявлено.\n\n"
        f"💡 *Порада: Спробуйте просканувати посилання на профіль.*"
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
    
