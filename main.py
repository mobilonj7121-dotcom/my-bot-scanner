import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt9okmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Розширена база даних у пам'яті
db = {
    "balance": 0.0,
    "gpu_level": 1,
    "xp": 0,
    "hacks_done": 0,
    "is_mining": False,
    "inventory": []
}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "⚡ **WELCOME TO NEURAL TERMINAL v10.0**\n"
        "━━━━━━━━━━━━━━\n"
        "🌐 **МЕРЕЖЕВІ КОМАНДИ:**\n"
        "┣ `/mine` — запуск майнінгу\n"
        "┣ `/hack` — злам випадкового сервера\n"
        "┣ `/scan` — пошук вразливостей в мережі\n\n"
        "🛠 **УПРАВЛІННЯ СИСТЕМОЮ:**\n"
        "┣ `/upgrade` — апгрейд заліза\n"
        "┣ `/status` — моніторинг ресурсів\n"
        "┣ `/wallet` — гаманець та XP\n\n"
        "🛒 **ДАРКНЕТ:**\n"
        "┗ `/market` — купити нелегальний софт\n"
        "━━━━━━━━━━━━━━\n"
        "Введите команду для начала работы."
    )

@dp.message(Command("mine"))
async def cmd_mine(message: types.Message):
    if db["is_mining"]:
        await message.reply("🚫 **ERROR:** Mining thread is busy.")
        return
    db["is_mining"] = True
    status = await message.answer("🛠 **CONNECTING TO BLOCKCHAIN...**")
    for i in range(5):
        profit = (random.uniform(0.0002, 0.0005)) * db["gpu_level"]
        db["balance"] += profit
        db["xp"] += 15
        bar = "■" * (i + 1) + "□" * (4 - i)
        await status.edit_text(f"⛏ **MINING...**\n`[{bar}]`\n💰 Profit: +{profit:.6f} XMR")
        await asyncio.sleep(2)
    db["is_mining"] = False
    await message.answer("✅ **SUCCESS.** Обчислення блоку завершено.")

@dp.message(Command("hack"))
async def cmd_hack(message: types.Message):
    targets = ["NASA_DB", "Pentagon_Mainframe", "Binance_Hot_Wallet", "Local_Bank_SQL"]
    target = random.choice(targets)
    msg = await message.answer(f"📡 **ATTACKING:** {target}...")
    await asyncio.sleep(2)
    
    if random.random() > 0.4: # 60% шанс успіху
        loot = random.uniform(0.001, 0.005)
        db["balance"] += loot
        db["hacks_done"] += 1
        db["xp"] += 50
        await msg.edit_text(f"💀 **HACK SUCCESS!**\nВикрадено: {loot:.5f} XMR з {target}.\nXP: +50")
    else:
        await msg.edit_text(f"🚨 **HACK FAILED!**\nАдміністратор {target} помітив активність. З'єднання розірвано.")

@dp.message(Command("market"))
async def cmd_market(message: types.Message):
    await message.answer(
        "🕳 **WELCOME TO SHADOW MARKET**\n"
        "━━━━━━━━━━━━━━\n"
        "1. `Antivirus Bypass` — 0.02 XMR\n"
        "2. `SQL Injector Pro` — 0.05 XMR\n"
        "3. `Quantum CPU` — 0.1 XMR\n"
        "━━━━━━━━━━━━━━\n"
        "(Функція в розробці, збирай кеш!)"
    )

@dp.message(Command("wallet"))
async def cmd_wallet(message: types.Message):
    await message.answer(
        f"💳 **CENTRAL WALLET**\n"
        f"💰 Balance: {db['balance']:.6f} XMR\n"
        f"🌟 Total XP: {db['xp']}\n"
        f"🏴‍☠️ Successful Hacks: {db['hacks_done']}"
    )

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    await message.answer(
        f"🖥 **OS MONITOR**\n"
        f"⚙️ CPU Level: {db['gpu_level']}\n"
        f"🌡 Temp: {random.randint(45, 70)}°C\n"
        f"📡 Proxy: Active (Tor Network)\n"
        f"🛠 Uptime: {random.randint(100, 999)} hours"
    )

@dp.message(Command("upgrade"))
async def cmd_upgrade(message: types.Message):
    cost = db["gpu_level"] * 0.01
    if db["balance"] >= cost:
        db["balance"] -= cost
        db["gpu_level"] += 1
        await message.answer(f"🔥 **UPGRADE:** Новий рівень CPU: {db['gpu_level']}!")
    else:
        await message.answer(f"❌ **FAIL:** Недостатньо коштів ({cost:.4f} XMR)")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
