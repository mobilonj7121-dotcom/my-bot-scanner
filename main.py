import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Твой токен
API_TOKEN = '8560393413:AAFlrX__ZmtosyREdfN0cjDr6MIeF5xPUuY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Временная база (работает пока бот запущен)
db = {}

async def set_bio(count):
    """Быстрое обновление раздела 'О себе' в профиле бота"""
    try:
        await bot.set_my_description(f"⛏ Лучшая ферма\n👥 Хакеров в сети: {count}\n💰 Начни зарабатывать прямо сейчас!")
    except: 
        pass

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    uid = m.from_user.id
    # Регистрация игрока
    if uid not in db:
        db[uid] = {"bal": 0.0, "lvl": 1}
    
    # Обновляем счетчик в профиле бота
    await set_bio(len(db))
    
    await m.answer(
        f"🌐 **ТЕРМИНАЛ v1.0**\n"
        f"━━━━━━━━━━━━━━\n"
        f"🕹 **КОМАНДЫ:**\n"
        f"┣ `/mine` — Майнинг ресурсов\n"
        f"┣ `/hack` — Взлом системы (риск)\n"
        f"┗ `/wallet` — Твой баланс\n"
        f"━━━━━━━━━━━━━━\n"
        f"👥 Всего игроков: {len(db)}"
    )

@dp.message(Command("mine"))
async def cmd_mine(m: types.Message):
    user = db.get(m.from_user.id, {"bal": 0.0, "lvl": 1})
    st = await m.answer("⛏ **Подключение к пулу...**")
    await asyncio.sleep(2)
    
    profit = random.uniform(0.001, 0.005)
    user["bal"] += profit
    db[m.from_user.id] = user
    
    await st.edit_text(f"✅ Добыто: `+{profit:.5f} XMR`")

@dp.message(Command("hack"))
async def cmd_hack(m: types.Message):
    user = db.get(m.from_user.id, {"bal": 0.0, "lvl": 1})
    msg = await m.answer("📡 **Взлом протоколов...**")
    await asyncio.sleep(2)
    
    if random.random() > 0.5:
        loot = random.uniform(0.01, 0.03)
        user["bal"] += loot
        await msg.edit_text(f"💀 **УСПЕХ!** Выкрадено: `{loot:.5f} XMR`")
    else:
        await msg.edit_text("🚨 **ПРОВАЛ!** Тебя заметили, связь разорвана.")
    
    db[m.from_user.id] = user

@dp.message(Command("wallet"))
async def cmd_wallet(m: types.Message):
    user = db.get(m.from_user.id, {"bal": 0.0, "lvl": 1})
    await m.answer(f"💳 **ВАШ БАЛАНС:** `{user['bal']:.6f} XMR`")

async def main():
    # Удаляем старые команды, чтобы бот не «глючил»
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
