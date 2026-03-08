import asyncio
import random
import logging
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# Логирование
logging.basicConfig(level=logging.INFO)

API_TOKEN = '8560393413:AAFlrX__ZmtosyREdfN0cjDr6MIeF5xPUuY'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- РАБОТА С БАЗОЙ ДАННЫХ ---
DB_FILE = 'users.json'

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_db():
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

db = load_db()

# --- ВЕБ-СЕРВЕР (ДЛЯ РАБОТЫ 24/7) ---
async def handle(request):
    return web.Response(text="TERMINAL v2.0 ONLINE 24/7")

async def start_webserver():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()

# --- КОМАНДЫ БОТА ---

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    uid = str(m.from_user.id)
    if uid not in db:
        db[uid] = {"bal": 0.0, "name": m.from_user.first_name}
        save_db()
    
    # Сообщение об обновлении (теперь не удаляется)
    await m.answer(
        "✨ **ИНФОРМАЦИЯ ОБ ОБНОВЛЕНИИ v2.0**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ База данных активирована (сохранение прогресса)\n"
        "✅ Режим работы: Постоянный (24/7)\n"
        "✅ Удаление сообщений отключено по просьбе админа\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )

    await m.answer(
        f"🌐 **TERMINAL OS v2.0**\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 Хакер: `{db[uid]['name']}`\n"
        f"💰 Твой баланс: `{db[uid]['bal']:.5f} XMR`\n\n"
        f"🕹 **ДОСТУПНЫЕ КОМАНДЫ:**\n"
        f"┣ `/mine` — Майнить криптовалюту\n"
        f"┣ `/hack` — Попробовать взлом\n"
        f"┗ `/wallet` — Посмотреть кошелек\n"
        f"━━━━━━━━━━━━━━"
    )

@dp.message(Command("mine"))
async def cmd_mine(m: types.Message):
    uid = str(m.from_user.id)
    if uid not in db: db[uid] = {"bal": 0.0, "name": m.from_user.first_name}
    
    status = await m.answer("⛏ **Майнинг в процессе...**")
    await asyncio.sleep(2)
    
    profit = random.uniform(0.001, 0.005)
    db[uid]["bal"] += profit
    save_db()
    
    await status.edit_text(f"✅ **ГОТОВО!**\n💎 Вы добыли: `+{profit:.5f} XMR` (Всего: `{db[uid]['bal']:.5f}`)")

@dp.message(Command("hack"))
async def cmd_hack(m: types.Message):
    uid = str(m.from_user.id)
    if uid not in db: db[uid] = {"bal": 0.0, "name": m.from_user.first_name}
    
    status = await m.answer("📡 **Попытка взлома...**")
    await asyncio.sleep(2)
    
    if random.random() > 0.5:
        loot = random.uniform(0.01, 0.04)
        db[uid]["bal"] += loot
        save_db()
        await status.edit_text(f"💀 **УСПЕШНО!**\n💰 Вы украли: `{loot:.5f} XMR`")
    else:
        await status.edit_text("🚨 **ОШИБКА!** Фаервол заблокировал атаку. Попробуйте позже.")

@dp.message(Command("wallet"))
async def cmd_wallet(m: types.Message):
    uid = str(m.from_user.id)
    bal = db.get(uid, {"bal": 0.0})["bal"]
    await m.answer(f"💳 **ВАШ КОШЕЛЕК:**\n💰 Баланс: `{bal:.6f} XMR`\n💵 Примерно: `${(bal * 160):.2f}`")

async def main():
    # Запуск сервера, чтобы бот не спал
    asyncio.create_task(start_webserver())
    
    logging.info("Бот v2.0 запущен без удаления сообщений!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
