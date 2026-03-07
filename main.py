import asyncio
import random
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Налаштування логів (щоб бачити помилки в панелі Render)
logging.basicConfig(level=logging.INFO)

API_TOKEN = '8560393413:AAFlrX__ZmtosyREdfN0cjDr6MIeF5xPUuY'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# База гравців (у пам'яті)
db = {}

async def update_bio(count):
    """Оновлення профілю бота (працює з затримкою від самого Telegram)"""
    try:
        await bot.set_my_description(f"⛏ Хакерская Ферма v1.0\n👥 Игроков в сети: {count}\n💰 Начни майнить XMR!")
    except Exception as e:
        logging.error(f"Ошибка Bio: {e}")

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    uid = m.from_user.id
    if uid not in db:
        db[uid] = {"bal": 0.0}
    
    await update_bio(len(db))
    await m.answer(
        f"🌐 **ТЕРМИНАЛ АКТИВИРОВАН**\n"
        f"━━━━━━━━━━━━━━\n"
        f"🕹 **КОМАНДЫ:**\n"
        f"┣ `/mine` — Майнинг\n"
        f"┣ `/hack` — Взлом\n"
        f"┗ `/wallet` — Баланс\n"
        f"━━━━━━━━━━━━━━\n"
        f"👥 Игроков в базе: {len(db)}"
    )

@dp.message(Command("mine"))
async def cmd_mine(m: types.Message):
    uid = m.from_user.id
    if uid not in db: db[uid] = {"bal": 0.0}
    
    status = await m.answer("⛏ **Майнинг...**")
    await asyncio.sleep(1.5)
    
    profit = random.uniform(0.001, 0.005)
    db[uid]["bal"] += profit
    await status.edit_text(f"✅ Получено: `+{profit:.5f} XMR`")

@dp.message(Command("hack"))
async def cmd_hack(m: types.Message):
    uid = m.from_user.id
    if uid not in db: db[uid] = {"bal": 0.0}
    
    status = await m.answer("📡 **Взлом...**")
    await asyncio.sleep(1.5)
    
    if random.random() > 0.5:
        loot = random.uniform(0.01, 0.03)
        db[uid]["bal"] += loot
        await status.edit_text(f"💀 **УСПЕХ!** Вы украли: `{loot:.5f} XMR`")
    else:
        await status.edit_text("🚨 **ПРОВАЛ!** Система защиты вас выкинула.")

@dp.message(Command("wallet"))
async def cmd_wallet(m: types.Message):
    user = db.get(m.from_user.id, {"bal": 0.0})
    await m.answer(f"💳 **БАЛАНС:** `{user['bal']:.6f} XMR`")

async def main():
    logging.info("Бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
