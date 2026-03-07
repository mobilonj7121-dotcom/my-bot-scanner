import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Твій токен
API_TOKEN = '8560393413:AAFlrX__ZmtosyREdfN0cjDr6MIeF5xPUuY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Тимчасова база (працює поки бот в мережі)
db = {}

async def set_bio(count):
    """Швидке оновлення про себе"""
    try:
        await bot.set_my_description(f"⛏ Найкраща ферма\n👥 Хакерів: {count}\n💰 Почни заробляти зараз!")
    except: pass

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    uid = m.from_user.id
    if uid not in db:
        db[uid] = {"bal": 0.0, "lvl": 1}
    
    await set_bio(len(db))
    await m.answer(
        f"🌐 **TERMINAL v1.0**\n"
        f"━━━━━━━━━━━━━━\n"
        f"🕹 Команди:\n"
        f"┣ `/mine` — Майнінг\n"
        f"┣ `/hack` — Злам системи\n"
        f"┗ `/wallet` — Твій баланс\n"
        f"━━━━━━━━━━━━━━\n"
        f"👥 В системі: {len(db)} гравців"
    )

@dp.message(Command("mine"))
async def cmd_mine(m: types.Message):
    user = db.get(m.from_user.id, {"bal": 0.0, "lvl": 1})
    st = await m.answer("⛏ **Майнінг...**")
    await asyncio.sleep(2)
    profit = random.uniform(0.001, 0.005)
    user["bal"] += profit
    db[m.from_user.id] = user
    await st.edit_text(f"✅ Здобуто: `+{profit:.5f} XMR`")

@dp.message(Command("hack"))
async def cmd_hack(m: types.Message):
    user = db.get(m.from_user.id, {"bal": 0.0, "lvl": 1})
    msg = await m.answer("📡 **Злам...**")
    await asyncio.sleep(2)
    if random.random() > 0.5:
        loot = random.uniform(0.01, 0.03)
        user["bal"] += loot
        await msg.edit_text(f"💀 **Успіх!** Викрадено: `{loot:.5f} XMR`")
    else:
        await msg.edit_text("🚨 **Провал!** Тебе помітили.")
    db[m.from_user.id] = user

@dp.message(Command("wallet"))
async def cmd_wallet(m: types.Message):
    user = db.get(m.from_user.id, {"bal": 0.0, "lvl": 1})
    await m.answer(f"💳 **БАЛАНС:** `{user['bal']:.6f} XMR`")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
