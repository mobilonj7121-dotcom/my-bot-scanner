import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Твій новий токен
API_TOKEN = '8560393413:AAFlrX__ZmtosyREdfN0cjDr6MIeF5xPUuY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

db = {"balance": 0.0, "level": 1, "xp": 0, "hacks": 0, "mining": False}

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    await m.answer(
        f"🌐 **NEURAL TERMINAL v14.0**\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 Користувач: {m.from_user.first_name}\n"
        f"⚙️ Рівень: {db['level']}\n"
        f"💰 Баланс: {db['balance']:.6f} XMR\n"
        f"━━━━━━━━━━━━━━\n"
        f"Команди: /mine, /hack, /upgrade, /wallet, /status"
    )

@dp.message(Command("mine"))
async def cmd_mine(m: types.Message):
    if db["mining"]: return
    db["mining"] = True
    st = await m.answer("🔌 Підключення...")
    for i in range(5):
        p = (random.uniform(0.0005, 0.0015)) * db["level"]
        db["balance"] += p
        await st.edit_text(f"⛏ Майнінг... {20*(i+1)}%\nДохід: +{p:.6f}")
        await asyncio.sleep(2)
    db["mining"] = False
    await m.answer("✅ Готово.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
