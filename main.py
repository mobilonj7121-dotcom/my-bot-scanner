import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Твій актуальний токен
API_TOKEN = '8560393413:AAFlrX__ZmtosyREdfN0cjDr6MIeF5xPUuY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# База даних сесії
db = {"bal": 0.0, "lvl": 1, "hacks": 0, "mining": False}

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    await m.answer(
        f"🌐 **HACKER OS v15.0 ONLINE**\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 Користувач: `{m.from_user.first_name}`\n"
        f"⚙️ Рівень: `{db['lvl']}`\n"
        f"💰 Баланс: `{db['bal']:.6f} XMR`\n"
        f"━━━━━━━━━━━━━━\n"
        f"🕹 **КОМАНДИ:**\n"
        f"┣ `/mine` — Майнінг\n"
        f"┣ `/hack` — Злам\n"
        f"┣ `/upgrade` — Покращення\n"
        f"┗ `/wallet` — Гаманець"
    )

@dp.message(Command("mine"))
async def cmd_mine(m: types.Message):
    if db["mining"]: return
    db["mining"] = True
    st = await m.answer("⛏ **Запуск обчислень...**")
    for i in range(5):
        p = (random.uniform(0.0006, 0.0018)) * db["lvl"]
        db["bal"] += p
        bar = "■" * (i + 1) + "□" * (4 - i)
        await st.edit_text(f"⛏ **MINING**\n`[{bar}]` {20*(i+1)}%\n💎 Дохід: `+{p:.6f}`")
        await asyncio.sleep(2)
    db["mining"] = False
    await m.answer("✅ Блок знайдено.")

@dp.message(Command("hack"))
async def cmd_hack(m: types.Message):
    msg = await m.answer("📡 **Взлом системи...**")
    await asyncio.sleep(2)
    if random.random() > 0.5:
        loot = random.uniform(0.005, 0.02)
        db["bal"] += loot
        db["hacks"] += 1
        await msg.edit_text(f"💀 **УСПІХ!**\nВикрадено: `{loot:.5f} XMR`")
    else:
        await msg.edit_text("🚨 **ПОМИЛКА!** Тебе помітили.")

@dp.message(Command("upgrade"))
async def cmd_up(m: types.Message):
    cost = db["lvl"] * 0.02
    if db["bal"] >= cost:
        db["bal"] -= cost
        db["lvl"] += 1
        await m.answer(f"🔥 **UPGRADE!** Рівень заліза: `{db['lvl']}`")
    else:
        await m.answer(f"❌ Треба `{cost:.3f} XMR`")

@dp.message(Command("wallet"))
async def cmd_wallet(m: types.Message):
    await m.answer(f"💳 **WALLET**\n💰 Баланс: `{db['bal']:.6f} XMR`\n🏴‍☠️ Зламів: `{db['hacks']}`")

async def main():
    # Це видалить старі конфлікти з Telegram
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
