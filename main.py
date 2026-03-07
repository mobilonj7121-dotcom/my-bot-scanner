import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Твій токен (переконайся, що він правильний)
API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt9okmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# База даних у пам'яті (скидається при перезапуску сервера)
db = {
    "balance": 0.0,
    "gpu_level": 1,
    "xp": 0,
    "hacks_done": 0,
    "is_mining": False,
    "coin": "XMR"
}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🚀 **SYSTEM BOOTED: HACKER OS v11.0**\n"
        "━━━━━━━━━━━━━━\n"
        "Вітаю у терміналі. Твій поточний рівень: **" + str(db["gpu_level"]) + "**\n\n"
        "💻 **ОСНОВНІ КОМАНДИ:**\n"
        "┣ `/mine` — Почати видобуток крипти\n"
        "┣ `/hack` — Спробувати зламати сервер\n"
        "┣ `/upgrade` — Покращити залізо (ціна: " + f"{(db['gpu_level'] * 0.01):.3f}" + ")\n"
        "┣ `/wallet` — Баланс та статистика\n"
        "┣ `/status` — Технічний стан системи\n"
        "┗ `/info` — Довідка по командам\n"
        "━━━━━━━━━━━━━━\n"
        "Чекаю на ввід даних..."
    )

@dp.message(Command("mine"))
async def cmd_mine(message: types.Message):
    if db["is_mining"]:
        await message.reply("⚠️ **ERROR:** Mining thread is busy. Wait for completion.")
        return
    
    db["is_mining"] = True
    status = await message.answer("🛠 **INITIALIZING HASHING...**")
    
    for i in range(5):
        # Дохід залежить від рівня GPU
        profit = (random.uniform(0.0002, 0.0006)) * db["gpu_level"]
        db["balance"] += profit
        db["xp"] += 10
        
        progress = "■" * (i + 1) + "□" * (4 - i)
        await status.edit_text(
            f"⛏ **MINING IN PROGRESS**\n"
            f"`[{progress}]` {20*(i+1)}%\n"
            f"💰 Profit: +{profit:.6f} {db['coin']}\n"
            f"📊 Power: {db['gpu_level'] * 120} MH/s"
        )
        await asyncio.sleep(2.5)
    
    db["is_mining"] = False
    await message.answer("✅ **BLOCK MINED.** Кошти зараховано.")

@dp.message(Command("hack"))
async def cmd_hack(message: types.Message):
    targets = ["Apple_Mainframe", "FBI_Database", "Crypto_Exchange", "Social_Network"]
    target = random.choice(targets)
    msg = await message.answer(f"📡 **ATTACKING:** `{target}`...")
    await asyncio.sleep(2)
    
    # 50% шанс успіху
    if random.random() > 0.5:
        loot = random.uniform(0.002, 0.01)
        db["balance"] += loot
        db["hacks_done"] += 1
        db["xp"] += 40
        await msg.edit_text(f"💀 **SUCCESS!** {target} зламано.\n💎 Здобич: {loot:.5f} XMR\n🌟 XP: +40")
    else:
        await msg.edit_text(f"🚨 **FAILURE!** Тебе вирахували по IP. З'єднання скинуто.")

@dp.message(Command("upgrade"))
async def cmd_upgrade(message: types.Message):
    cost = db["gpu_level"] * 0.01
    if db["balance"] >= cost:
        db["balance"] -= cost
        db["gpu_level"] += 1
        await message.answer(f"🔥 **HARDWARE UPGRADED!** Рівень CPU/GPU тепер: **{db['gpu_level']}**")
    else:
        await message.answer(f"❌ **NOT ENOUGH FUNDS.** Потрібно: {cost:.4f} XMR")

@dp.message(Command("wallet"))
async def cmd_wallet(message: types.Message):
    await message.answer(
        f"💳 **CENTRAL WALLET**\n"
        f"━━━━━━━━━━━━━━\n"
        f"💰 Баланс: {db['balance']:.6f} {db['coin']}\n"
        f"💵 USD: ${(db['balance'] * 164.5):.2f}\n"
        f"🌟 Досвід: {db['xp']} XP\n"
        f"🏴‍☠️ Вдалих зламів: {db['hacks_done']}"
    )

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    await message.answer(
        f"🖥 **OS MONITOR**\n"
        f"━━━━━━━━━━━━━━\n"
        f"⚙️ Level: {db['gpu_level']}\n"
        f"🌡 Temp: {random.randint(40, 68)}°C\n"
        f"🌪 Fans: {random.randint(1500, 4000)} RPM\n"
        f"📡 Connection: Encrypted (AES-256)"
    )

@dp.message(Command("info"))
async def cmd_info(message: types.Message):
    await message.answer("🆘 **ДОПОМОГА:**\nЗаробляй крипту через `/mine` або `/hack`. Витрачай її в `/upgrade`, щоб заробляти ще швидше. Твоя мета — стати хакером 100 рівня!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
