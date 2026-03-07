import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Твой токен (уже вставлен)
API_TOKEN = '8560393413:AAFlrX__ZmtosyREdfN0cjDr6MIeF5xPUuY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# База данных игроков в памяти (сбрасывается при перезагрузке)
db = {}

async def set_bio(count):
    """Обновление описания в профиле бота"""
    try:
        await bot.set_my_description(f"⛏ Хакерская ферма v1.0\n👥 Игроков: {count}\n💰 Начни майнить прямо сейчас!")
    except: 
        pass

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    uid = m.from_user.id
    if uid not in db:
        db[uid] = {"bal": 0.0}
    
    # Обновляем инфо в профиле бота
    await set_bio(len(db))
    
    await m.answer(
        f"🌐 **TERMINAL v1.0**\n"
        f"━━━━━━━━━━━━━━\n"
        f"🕹 **КОМАНДЫ:**\n"
        f"┣ `/mine` — Майнинг ресурсов\n"
        f"┣ `/hack` — Взлом системы\n"
        f"┗ `/wallet` — Твой баланс\n"
        f"━━━━━━━━━━━━━━\n"
        f"👥 Всего хакеров: {len(db)}"
    )

@dp.message(Command("mine"))
async def cmd_mine(m: types.Message):
    uid = m.from_user.id
    if uid not in db: db[uid] = {"bal": 0.0}
    
    st = await m.answer("⛏ **Майним XMR...**")
    await asyncio.sleep(2) # Имитация работы
    
    profit = random.uniform(0.001, 0.005)
    db[uid]["bal"] += profit
    
    await st.edit_text(f"✅ Добыто: `+{profit:.5f} XMR`")

@dp.message(Command("hack"))
async def cmd_hack(m: types.Message):
    uid = m.from_user.id
    if uid not in db: db[uid] = {"bal": 0.0}
    
    msg = await m.answer("📡 **Взламываем протоколы...**")
    await asyncio.sleep(2)
    
    if random.random() > 0.5:
        loot = random.uniform(0.01, 0.03)
        db[uid]["bal"] += loot
        await msg.edit_text(f"💀 **УСПЕХ!** Выкрадено: `{loot:.5f} XMR`")
    else:
        await msg.edit_text("🚨 **ПРОВАЛ!** Тебя заметили.")

@dp.message(Command("wallet"))
async def cmd_wallet(m: types.Message):
    user = db.get(m.from_user.id, {"bal": 0.0})
    await m.answer(f"💳 **БАЛАНС:** `{user['bal']:.6f} XMR`")

async def main():
    # Чистим старые сообщения
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
