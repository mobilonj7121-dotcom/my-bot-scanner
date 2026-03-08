import asyncio
import random
import logging
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# Настройка логов
logging.basicConfig(level=logging.INFO)

API_TOKEN = '8560393413:AAFlrX__ZmtosyREdfN0cjDr6MIeF5xPUuY'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- РАБОТА С ДАННЫМИ (БАЗА) ---
DB_FILE = 'users.json'

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_db():
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

db = load_db()

# --- ВЕБ-СЕРВЕР ДЛЯ ПОДДЕРЖКИ 24/7 ---
async def handle(request):
    return web.Response(text="TERMINAL v2.0 IS RUNNING 24/7")

async def start_webserver():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()

# --- УДАЛЕНИЕ СООБЩЕНИЙ ---
async def delete_later(message: types.Message, delay: int = 15):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass

# --- КОМАНДЫ БОТА ---

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    uid = str(m.from_user.id)
    if uid not in db:
        db[uid] = {"bal": 0.0, "name": m.from_user.first_name}
        save_db()
    
    # Анонс обновления (показывается всегда при /start)
    upd = await m.answer(
        "✨ **ОБНОВЛЕНИЕ v2.0 УСТАНОВЛЕНО!**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "● Режим скрытности: **АКТИВЕН**\n"
        "● База данных: **ПОДКЛЮЧЕНА**\n"
        "● Статус сервера: **24/7 ONLINE**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📥 *Лог обновления исчезнет через 15 сек...*"
    )
    asyncio.create_task(delete_later(upd, 15))

    menu = await m.answer(
        f"🌐 **TERMINAL OS v2.0**\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 Хакер: `{db[uid]['name']}`\n"
        f"💰 Баланс: `{db[uid]['bal']:.5f} XMR`\n\n"
        f"🕹 **КОМАНДЫ:**\n"
        f"┣ `/mine` — Добыча криптовалюты\n"
        f"┣ `/hack` — Взлом (большой куш)\n"
        f"┗ `/wallet` — Проверить кошелек\n"
        f"━━━━━━━━━━━━━━"
    )
    asyncio.create_task(delete_later(menu, 30))
    asyncio.create_task(delete_later(m, 5))

@dp.message(Command("mine"))
async def cmd_mine(m: types.Message):
    uid = str(m.from_user.id)
    st = await m.answer("🔌 **Майнинг запущен...**")
    await asyncio.sleep(2)
    
    profit = random.uniform(0.001, 0.005)
    db[uid]["bal"] += profit
    save_db() # Сохраняем прогресс
    
    res = await st.edit_text(f"✅ **ДОБЫТО:** `+{profit:.5f} XMR`\n🗑 *Очистка через 10 сек...*")
    asyncio.create_task(delete_later(res, 10))
    asyncio.create_task(delete_later(m, 5))

@dp.message(Command("hack"))
async def cmd_hack(m: types.Message):
    uid = str(m.from_user.id)
    msg = await m.answer("📡 **Взлом протоколов...**")
    await asyncio.sleep(2)
    
    if random.random() > 0.5:
        loot = random.uniform(0.01, 0.04)
        db[uid]["bal"] += loot
        save_db()
        res = await msg.edit_text(f"💀 **УСПЕХ!** Украдено: `{loot:.5f} XMR`\n🗑 *Скрытие лога...*")
    else:
        res = await msg.edit_text("🚨 **ПРОВАЛ!** Следы стерты, вы не обнаружены.")
    
    asyncio.create_task(delete_later(res, 10))
    asyncio.create_task(delete_later(m, 5))

@dp.message(Command("wallet"))
async def cmd_wallet(m: types.Message):
    uid = str(m.from_user.id)
    bal = db.get(uid, {"bal": 0.0})["bal"]
    res = await m.answer(f"💳 **БАЛАНС:** `{bal:.6f} XMR`\n🗑 *Удаление через 15 сек...*")
    asyncio.create_task(delete_later(res, 15))
    asyncio.create_task(delete_later(m, 5))

async def main():
    asyncio.create_task(start_webserver())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
