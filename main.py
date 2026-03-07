import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Твій токен
API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt9okmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Початок сесії майнінгу
    status = await message.answer(
        "🖥 **MINING SESSION INITIALIZED**\n"
        "━━━━━━━━━━━━━━\n"
        "⚙️ Hardware: Virtualized CPU Thread\n"
        "🌐 Pool: XMR-Mainnet-Node-01\n"
        "⏳ Статус: Синхронізація..."
    )
    await asyncio.sleep(2)
    
    current_balance = 0.0
    # Цикл симуляції на 15 кроків
    for _ in range(15):
        # Реалістичне нарахування валюти
        income = random.uniform(0.00005, 0.00015)
        current_balance += income
        
        # Технічні показники
        hashrate = random.randint(450, 520)
        temp = random.uniform(42.5, 55.0)
        
        await status.edit_text(
            f"⛏ **MINING CORE ACTIVE**\n"
            f"━━━━━━━━━━━━━━\n"
            f"💰 **Поточний баланс:** {current_balance:.6f} XMR\n"
            f"💵 **Еквівалент USD:** ${(current_balance * 162.45):.4f}\n"
            f"🚀 **Hashrate:** {hashrate} H/s\n"
            f"🌡 **CPU Temp:** {temp:.1f}°C\n"
            f"📊 **Uptime:** Active Session\n"
            f"━━━━━━━━━━━━━━\n"
            f"📡 Статус мережі: Стабільно"
        )
        # Затримка між оновленнями для реалізму
        await asyncio.sleep(3)

    await message.answer(
        f"✅ **СЕСІЮ ЗАВЕРШЕНО УСПІШНО**\n\n"
        f"💎 Всього видобуто: **{current_balance:.6f} XMR**\n"
        f"📥 Кошти збережено у внутрішній буфер.\n"
        f"🔌 Обладнання переведено в режим очікування."
    )

@dp.message(F.text)
async def process_locked(message: types.Message):
    # Технічне сповіщення про зайнятість процесу
    await message.reply("⚠️ **SYSTEM BUSY:** Обчислення блоку триває. Будь ласка, зачекайте завершення сесії.")

async def main():
    # Очищення старих запитів та запуск на Render
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
