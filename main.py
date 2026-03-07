import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt9okmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Глобальні змінні для симуляції (у пам'яті бота)
user_data = {
    "balance": 0.0,
    "coin": "XMR",
    "is_mining": False
}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🖥 **CRYPTO TERMINAL v4.2**\n"
        "━━━━━━━━━━━━━━\n"
        "Доступні команди для управління:\n"
        "🔹 `/mine` — Запустити сесію видобутку\n"
        "🔹 `/status` — Перевірити стан обладнання\n"
        "🔹 `/wallet` — Переглянути накопичений баланс\n"
        "🔹 `/config` — Змінити активну валюту\n"
        "━━━━━━━━━━━━━━\n"
        "Система готова до роботи. Введіть команду."
    )

@dp.message(Command("mine"))
async def cmd_mine(message: types.Message):
    if user_data["is_mining"]:
        await message.reply("⚠️ **ERROR:** Mining session is already active.")
        return

    user_data["is_mining"] = True
    status = await message.answer("🛠 **INITIALIZING NODES...**")
    await asyncio.sleep(1.5)
    
    # Симуляція циклу майнінгу
    for i in range(5):
        income = random.uniform(0.0001, 0.0003)
        user_data["balance"] += income
        
        await status.edit_text(
            f"⛏ **MINING {user_data['coin']}...**\n"
            f"━━━━━━━━━━━━━━\n"
            f"📈 Progress: [{'■' * (i+1)}{'□' * (4-i)}]\n"
            f"💰 Session Profit: +{income:.6f} {user_data['coin']}\n"
            f"🌡 Temp: {random.randint(45, 60)}°C\n"
            f"━━━━━━━━━━━━━━"
        )
        await asyncio.sleep(3)
    
    user_data["is_mining"] = False
    await message.answer(f"✅ **SESSION COMPLETED.** Data saved to buffer.")

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    state = "ACTIVE" if user_data["is_mining"] else "STANDBY"
    await message.answer(
        f"📊 **HARDWARE MONITOR**\n"
        f"━━━━━━━━━━━━━━\n"
        f"⚙️ Core Status: {state}\n"
        f"🔗 Connection: Secure (SSL)\n"
        f"📡 Latency: {random.randint(15, 45)}ms\n"
        f"🔋 Efficiency: 94.2%\n"
        f"━━━━━━━━━━━━━━"
    )

@dp.message(Command("wallet"))
async def cmd_wallet(message: types.Message):
    await message.answer(
        f"💳 **CRYPTO WALLET**\n"
        f"━━━━━━━━━━━━━━\n"
        f"💰 Total Balance: {user_data['balance']:.6f} {user_data['coin']}\n"
        f"💵 Est. Value: ${(user_data['balance'] * 165):.2f}\n"
        f"━━━━━━━━━━━━━━"
    )

@dp.message(Command("config"))
async def cmd_config(message: types.Message):
    # Проста зміна валюти для реалізму
    coins = ["BTC", "ETH", "XMR", "SOL"]
    user_data["coin"] = random.choice(coins)
    await message.answer(f"⚙️ **CONFIG UPDATED.** Active currency set to: **{user_data['coin']}**")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
