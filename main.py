import asyncio
import random
import os
import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Твій токен
API_TOKEN = '8560393413:AAFlrX__ZmtosyREdfN0cjDr6MIeF5xPUuY'
# URL бази даних (Render надасть його в налаштуваннях)
DB_URL = os.getenv("DATABASE_URL")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Спрощена база для гри в пам'яті (скидається), але список юзерів - у Postgres (вічно)
game_db = {"balance": 0.0, "mining": False}

def init_db():
    """Створення таблиці користувачів, якщо її немає"""
    if not DB_URL: return
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id BIGINT PRIMARY KEY);")
    conn.commit()
    cur.close()
    conn.close()

async def update_bot_bio():
    """Оновлення опису бота (те, що видно 'не в боті')"""
    if not DB_URL: return
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users;")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        
        # Оновлюємо текст 'Про себе' у профілі бота
        await bot.set_my_description(f"🛠 Hacker OS v18.0\n👥 Підписано хакерів: {count}\n🚀 Стань одним із нас — тисни /start")
    except Exception as e:
        print(f"Bio update error: {e}")

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    # Додаємо юзера в базу Postgres
    if DB_URL:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING;", (m.from_user.id,))
        conn.commit()
        cur.close()
        conn.close()
    
    await update_bot_bio()
    
    await m.answer(
        f"🌐 **HACKER OS v18.0 ONLINE**\n"
        f"━━━━━━━━━━━━━━\n"
        f"Статистика оновлена в описі бота!\n"
        f"💰 Баланс: `{game_db['balance']:.6f} XMR`\n"
        f"━━━━━━━━━━━━━━\n"
        f"Команди: /mine, /hack, /wallet"
    )

@dp.message(Command("mine"))
async def cmd_mine(m: types.Message):
    if game_db["mining"]: return
    game_db["mining"] = True
    st = await m.answer("⛏ **Майнінг...**")
    await asyncio.sleep(4)
    profit = random.uniform(0.001, 0.003)
    game_db["balance"] += profit
    game_db["mining"] = False
    await st.edit_text(f"✅ Готово! +{profit:.6f} XMR")

async def main():
    init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
