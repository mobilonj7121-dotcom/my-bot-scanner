import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt9okmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# База даних у пам'яті (скидається при перезавантаженні на Render)
db = {
    "balance": 0.0,
    "gpu_level": 1,
    "xp": 0,
    "coin": "XMR",
    "is_mining": False
}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "⚡ **NEURAL TERMINAL v9.0 ONLINE**\n"
        "━━━━━━━━━━━━━━\n"
        "Вітаю, хакер. Система готова до експлуатації.\n\n"
        "🕹 **ОСНОВНІ КОМАНДИ:**\n"
        "┣ `/mine` — запуск циклу видобутку\n"
        "┣ `/upgrade` — прокачка заліза (відеокарт)\n"
        "┣ `/wallet` — стан рахунку та валюта\n"
        "┣ `/status` — моніторинг системи\n"
        "┣ `/scan` — імітація пошуку вразливостей\n"
        "┗ `/top` — глобальний рейтинг (імітація)\n"
        "━━━━━━━━━━━━━━\n"
        "⚠️ *Попередження: Система працює на пікових частотах.*"
    )

@dp.message(Command("mine"))
async def cmd_mine(message: types.Message):
    if db["is_mining"]:
        await message.reply("🚫 **CRITICAL:** Потік вже зайнятий обчисленнями!")
        return

    db["is_mining"] = True
    status = await message.answer("🛠 **CONNECTING TO POOL...**")
    
    # Швидкість залежить від рівня прокачки
    steps = 5
    for i in range(steps):
        profit = (random.uniform(0.0001, 0.0003)) * db["gpu_level"]
        db["balance"] += profit
        db["xp"] += 10
        
        bar = "■" * (i + 1) + "□" * (steps - i - 1)
        await status.edit_text(
            f"⛏ **MINING {db['coin']}...**\n"
            f"━━━━━━━━━━━━━━\n"
            f"📊 Потужність: {db['gpu_level'] * 450} H/s\n"
            f"📈 Прогрес: [{bar}]\n"
            f"💰 Дохід: +{profit:.6f}\n"
            f"━━━━━━━━━━━━━━"
        )
        await asyncio.sleep(2)
    
    db["is_mining"] = False
    await message.answer("✅ **CYCLE COMPLETE.** Кошти додано до гаманця.")

@dp.message(Command("upgrade"))
async def cmd_upgrade(message: types.Message):
    cost = db["gpu_level"] * 0.005
    if db["balance"] >= cost:
        db["balance"] -= cost
        db["gpu_level"] += 1
        await message.answer(f"🔥 **UPGRADE SUCCESS!** Ваше залізо тепер {db['gpu_level']} рівня. Швидкість майнінгу зросла!")
    else:
        await message.answer(f"❌ **LOW FUNDS.** Для апгрейду треба {cost:.4f} {db['coin']}. Майни далі, мамонт.")

@dp.message(Command("wallet"))
async def cmd_wallet(message: types.Message):
    await message.answer(
        f"💳 **CENTRAL WALLET**\n"
        f"━━━━━━━━━━━━━━\n"
        f"💰 Баланс: {db['balance']:.6f} {db['coin']}\n"
        f"🌟 Рівень досвіду: {db['xp']} XP\n"
        f"💹 Курс: 1 {db['coin']} = $164.20\n"
        f"━━━━━━━━━━━━━━"
    )

@dp.message(Command("scan"))
async def cmd_scan(message: types.Message):
    await message.answer("🔍 **SCANNING NETWORK...**")
    await asyncio.sleep(1.5)
    await message.answer(
        f"📡 **Знайдено вразливість:** `IP: {random.randint(100,255)}.45.12.{random.randint(1,255)}`\n"
        "🔓 Доступ до бази даних отримано. Копіюю паролі... 80%"
    )

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    await message.answer(
        f"🖥 **SYSTEM REPORT**\n"
        f"━━━━━━━━━━━━━━\n"
        f"🌡 Temp: {random.randint(40, 65)}°C\n"
        f"🌪 Fans: {random.randint(2000, 4500)} RPM\n"
        f"⚡ Power: {random.uniform(150.0, 350.0):.1f}W\n"
        f"🔗 Peer: Cloud_Server_Frankfurt\n"
        f"━━━━━━━━━━━━━━"
    )

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
