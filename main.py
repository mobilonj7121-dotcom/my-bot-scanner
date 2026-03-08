import asyncio
import random
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web # Добавили для веб-сервера

logging.basicConfig(level=logging.INFO)

API_TOKEN = '8560393413:AAFlrX__ZmtosyREdfN0cjDr6MIeF5xPUuY'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
db = {}

# --- СЕКЦИЯ ДЛЯ ПОДДЕРЖКИ СЕРВЕРА 24/7 ---
async def handle(request):
    return web.Response(text="Бот активен 24/7")

async def start_webserver():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000) # Render использует порт 10000
    await site.start()
# ----------------------------------------

async def update_bio(count):
    try:
        await bot.set_my_description(f"⛏ Хакерская Ферма v1.0\n👥 Игроков в сети: {count}\n💰 Начни майнить XMR!")
    except: pass

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    uid = m.from_user.id
    if uid not in db: db[uid] = {"bal": 0.0}
    await update_bio(len(db))
    await m.answer(f"🌐 **ТЕРМИНАЛ v1.0**\n━━━━━━━━━━━━━━\n🕹 Команды:\n┣ `/mine` — Майнинг\n┣ `/hack` — Взлом\n┗ `/wallet` — Баланс")

@dp.message(Command("mine"))
async def cmd_mine(m: types.Message):
    status = await m.answer("⛏ **Майнинг...**")
    await asyncio.sleep(1.5)
    profit = random.uniform(0.001, 0.005)
    db[m.from_user.id]["bal"] = db.get(m.from_user.id, {"bal":0.0})["bal"] + profit
    await status.edit_text(f"✅ Получено: `+{profit:.5f} XMR`")

@dp.message(Command("wallet"))
async def cmd_wallet(m: types.Message):
    user = db.get(m.from_user.id, {"bal": 0.0})
    await m.answer(f"💳 **БАЛАНС:** `{user['bal']:.6f} XMR`")

async def main():
    # Запускаем веб-сервер, чтобы Render видел активность
    asyncio.create_task(start_webserver())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
