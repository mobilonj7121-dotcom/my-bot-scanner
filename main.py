import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Твій унікальний токен
API_TOKEN = '8560393413:AAFlrX__ZmtosyREdfN0cjDr6MIeF5xPUuY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Глобальна база всіх гравців
db = {}

async def update_bot_bio():
    """Автоматично оновлює опис бота в Telegram (цифри, які бачать усі)"""
    count = len(db)
    try:
        # Текст перед стартом бота
        await bot.set_my_short_description(f"🔥 Найкраща хакерська ферма! Гравців у грі: {count}. Тисни /start")
        # Текст у профілі бота (Bio)
        await bot.set_my_description(f"💻 TERMINAL OS v20.0\n👥 Хакерів у мережі: {count}\n💰 Заробляй крипту, ламай сервери, стань №1!")
    except Exception as e:
        print(f"Помилка оновлення Bio: {e}")

def get_rank(lvl):
    if lvl >= 100: return "Кібер-Бог 👑"
    if lvl >= 50: return "Елітний Хакер 💀"
    if lvl >= 20: return "Профі 💻"
    return "Новачок 🐣"

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    uid = m.from_user.id
    # Реєстрація нового гравця
    if uid not in db:
        db[uid] = {
            "name": m.from_user.first_name, 
            "bal": 0.0, 
            "lvl": 1, 
            "hacks": 0, 
            "mining": False,
            "items": []
        }
        await update_bot_bio() # Оновлюємо цифри у профілі бота

    await m.answer(
        f"🌐 **СИСТЕМА АКТИВОВАНА**\n"
        f"━━━━━━━━━━━━━━\n"
        f"Вітаю, `{m.from_user.first_name}`! Ти в головному терміналі.\n"
        f"👥 Всього хакерів у базі: **{len(db)}**\n\n"
        f"📜 **ВСІ КОМАНДИ СИСТЕМИ:**\n"
        f"⛏ `/mine` — Безпечний майнінг XMR\n"
        f"💀 `/hack` — Ризикований злам (великий куш)\n"
        f"⬆️ `/upgrade` — Покращити залізо\n"
        f"💳 `/wallet` — Баланс гаманця\n"
        f"👤 `/profile` — Твій хакерський паспорт\n"
        f"🏆 `/top` — Рейтинг найбагатших\n"
        f"🛒 `/market` — Чорний ринок\n"
        f"📊 `/status` — Стан серверів"
    )

@dp.message(Command("mine"))
async def cmd_mine(m: types.Message):
    user = db.get(m.from_user.id)
    if not user: return await m.answer("⚠️ Напиши /start для реєстрації!")
    if user["mining"]: return await m.answer("🚫 Ти вже майниш! Дочекайся завершення.")
    
    user["mining"] = True
    st = await m.answer("🔌 **Підключення до пулу...**")
    
    for i in range(4):
        p = (random.uniform(0.001, 0.003)) * user["lvl"]
        user["bal"] += p
        bar = "█" * (i + 1) + "░" * (3 - i)
        await st.edit_text(f"⛏ **МАЙНІНГ АКТИВНИЙ**\n`[{bar}]` {33*(i+1)}%\n💎 Здобуто: `+{p:.5f} XMR`")
        await asyncio.sleep(2)
        
    user["mining"] = False
    await m.answer(f"✅ Майнінг завершено! Твій баланс: `{user['bal']:.5f} XMR`")

@dp.message(Command("hack"))
async def cmd_hack(m: types.Message):
    user = db.get(m.from_user.id)
    if not user: return
    
    msg = await m.answer("📡 **Обхід фаєрволу Пентагону...**")
    await asyncio.sleep(2.5)
    
    # 50% шанс на успіх. Якщо є VPN, шанс вищий!
    chance = 0.7 if "VPN" in user["items"] else 0.5
    
    if random.random() < chance:
        loot = random.uniform(0.01, 0.05) * user["lvl"]
        user["bal"] += loot
        user["hacks"] += 1
        await msg.edit_text(f"💀 **ЗЛАМ УСПІШНИЙ!**\nТи викрав: `{loot:.5f} XMR`\nВсього вдалих зламів: `{user['hacks']}`")
    else:
        penalty = random.uniform(0.001, 0.005)
        user["bal"] = max(0, user["bal"] - penalty)
        await msg.edit_text(f"🚨 **ТРИВОГА!** Тебе помітили. Штраф: `{penalty:.5f} XMR`")

@dp.message(Command("upgrade"))
async def cmd_up(m: types.Message):
    user = db.get(m.from_user.id)
    if not user: return
    
    cost = user["lvl"] * 0.05
    if user["bal"] >= cost:
        user["bal"] -= cost
        user["lvl"] += 1
        await m.answer(f"🔥 **АПГРЕЙД УСПІШНИЙ!** Твій новий рівень: `{user['lvl']}`.\nТепер ти заробляєш більше!")
    else:
        await m.answer(f"❌ **Недостатньо коштів!** Потрібно: `{cost:.5f} XMR`")

@dp.message(Command("market"))
async def cmd_market(m: types.Message):
    await m.answer(
        f"🛒 **ЧОРНИЙ РИНОК**\n"
        f"━━━━━━━━━━━━━━\n"
        f"1️⃣ 🛡 VPN (Збільшує шанс зламу) — `0.5 XMR`\n"
        f"Щоб купити, напиши: `/buy vpn`"
    )

@dp.message(Command("buy"))
async def cmd_buy(m: types.Message):
    user = db.get(m.from_user.id)
    if not user: return
    
    item = m.text.replace("/buy ", "").strip().lower()
    if item == "vpn":
        if "VPN" in user["items"]: return await m.answer("❌ У тебе вже є VPN!")
        if user["bal"] >= 0.5:
            user["bal"] -= 0.5
            user["items"].append("VPN")
            await m.answer("✅ **Ти успішно купив VPN!** Шанс зламу збільшено.")
        else:
            await m.answer("❌ Не вистачає XMR!")
    else:
        await m.answer("❓ Товар не знайдено. Дивись /market")

@dp.message(Command("profile"))
async def cmd_profile(m: types.Message):
    user = db.get(m.from_user.id)
    if not user: return
    
    rank = get_rank(user['lvl'])
    items = ", ".join(user['items']) if user['items'] else "Порожньо"
    
    await m.answer(
        f"👤 **ПАСПОРТ ХАКЕРА**\n"
        f"━━━━━━━━━━━━━━\n"
        f"Ім'я: `{user['name']}`\n"
        f"Ранг: **{rank}**\n"
        f"Рівень: `{user['lvl']}`\n"
        f"Інвентар: `{items}`\n"
        f"Вдалих зламів: `{user['hacks']}`"
    )

@dp.message(Command("top"))
async def cmd_top(m: types.Message):
    if not db: return await m.answer("База порожня!")
    
    # Сортуємо гравців за балансом
    sorted_users = sorted(db.values(), key=lambda x: x["bal"], reverse=True)[:5]
    text = "🏆 **ТОП-5 ХАКЕРІВ СЕРВЕРА:**\n━━━━━━━━━━━━━━\n"
    for i, u in enumerate(sorted_users, 1):
        text += f"{i}. {u['name']} — `{u['bal']:.4f} XMR` (Рівень {u['lvl']})\n"
    
    await m.answer(text)

@dp.message(Command("wallet"))
async def cmd_wallet(m: types.Message):
    user = db.get(m.from_user.id)
    if not user: return
    await m.answer(f"💳 **ГАМАНЕЦЬ**\n💰 Баланс: `{user['bal']:.6f} XMR`\n💵 В USD: `${(user['bal'] * 150):.2f}`")

@dp.message(Command("status"))
async def cmd_status(m: types.Message):
    await m.answer(f"📊 **СЕРВЕРИ СИСТЕМИ**\n🟢 Ping: `{random.randint(10, 45)} ms`\n🔥 Навантаження: `{random.randint(40, 95)}%`\n👥 Онлайн: `{len(db)}`")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
