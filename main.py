import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Твій токен
API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt9okmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# База даних у пам'яті (скидається при перезапуску Render)
db = {
    "balance": 0.0,
    "level": 1,
    "xp": 0,
    "hacks": 0,
    "mining": False,
    "rank": "Новачок 🐣"
}

def update_rank():
    if db["level"] >= 50: db["rank"] = "GOD MODE ⚡"
    elif db["level"] >= 20: db["rank"] = "Елітний Хакер 💀"
    elif db["level"] >= 10: db["rank"] = "Спеціаліст 🖥️"
    elif db["level"] >= 5: db["rank"] = "Просунутий 🔍"

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    update_rank()
    await m.answer(
        f"🖥 **TERMINAL OS v12.0**\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 Користувач: {m.from_user.first_name}\n"
        f"🏆 Ранг: {db['rank']}\n"
        f"⚙️ Рівень заліза: {db['level']}\n"
        f"💰 Баланс: {db['balance']:.6f} XMR\n"
        f"━━━━━━━━━━━━━━\n"
        f"🕹 **КОМАНДИ:**\n"
        f"┣ `/mine` — Майнінг (заробіток)\n"
        f"┣ `/hack` — Злам (ризик/великий дохід)\n"
        f"┣ `/upgrade` — Качати залізо (ціна: {(db['level']*0.01):.3f})\n"
        f"┣ `/wallet` — Гаманець та XP\n"
        f"┗ `/status` — Дані системи"
    )

@dp.message(Command("mine"))
async def cmd_mine(m: types.Message):
    if db["mining"]: return
    db["mining"] = True
    st = await m.answer("🔌 **Підключення до пулу...**")
    
    for i in range(6):
        profit = (random.uniform(0.0003, 0.0008)) * db["level"]
        db["balance"] += profit
        db["xp"] += 5
        bar = "■" * (i + 1) + "□" * (5 - i)
        await st.edit_text(f"⛏ **MINING ACTIVE**\n`[{bar}]` {16*(i+1)}%\n💎 Дохід: +{profit:.6f} XMR")
        await asyncio.sleep(2.5)
    
    db["mining"] = False
    update_rank()
    await m.answer("✅ Блок знайдено. Транзакція підтверджена.")

@dp.message(Command("hack"))
async def cmd_hack(m: types.Message):
    targets = [
        {"n": "🏦 Приватний банк", "p": 0.6, "l": 0.005},
        {"n": "🛰️ Сервер НАСА", "p": 0.4, "l": 0.015},
        {"n": "💎 Біржа Binance", "p": 0.2, "l": 0.05}
    ]
    t = random.choice(targets)
    msg = await m.answer(f"📡 **АТАКА НА:** {t['n']}...")
    await asyncio.sleep(3)
    
    if random.random() < t['p']:
        db["balance"] += t['l']
        db["hacks"] += 1
        db["xp"] += 50
        await msg.edit_text(f"💀 **SUCCESS!** {t['n']} зламано!\n💰 Здобич: {t['l']:.5f} XMR\n🌟 XP: +50")
    else:
        await msg.edit_text(f"🚨 **ALARM!** Системи безпеки {t['n']} заблокували атаку.")

@dp.message(Command("upgrade"))
async def cmd_up(m: types.Message):
    cost = db["level"] * 0.01
    if db["balance"] >= cost:
        db["balance"] -= cost
        db["level"] += 1
        update_rank()
        await m.answer(f"🔥 **UPGRADE!** Рівень заліза підвищено до {db['level']}.\nШвидкість майнінгу зросла!")
    else:
        await m.answer(f"❌ Недостатньо XMR. Треба: {cost:.3f}")

@dp.message(Command("wallet"))
async def cmd_wallet(m: types.Message):
    await m.answer(
        f"💳 **CENTRAL WALLET**\n"
        f"━━━━━━━━━━━━━━\n"
        f"💰 Баланс: {db['balance']:.6f} XMR\n"
        f"💵 У доларах: ${(db['balance'] * 168):.2f}\n"
        f"🌟 Досвід: {db['xp']} XP\n"
        f"🏴‍☠️ Вдалих атак: {db['hacks']}"
    )

@dp.message(Command("status"))
async def cmd_status(m: types.Message):
    await m.answer(
        f"📊 **SYSTEM DIAGNOSTICS**\n"
        f"━━━━━━━━━━━━━━\n"
        f"🌡 Температура: {random.randint(45, 70)}°C\n"
        f"🌪 Оберти кулерів: {random.randint(2800, 5000)} RPM\n"
        f"🛰 Провідний сервер: Frankfurt-DE\n"
        f"🛡 Захист: Активний"
    )

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
