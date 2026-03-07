import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Твій новий токен
API_TOKEN = '8560393413:AAFlrX__ZmtosyREdfN0cjDr6MIeF5xPUuY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Глобальна база даних сесії
db = {
    "balance": 0.0,
    "level": 1,
    "xp": 0,
    "hacks": 0,
    "mining": False
}

def get_rank(lvl):
    if lvl >= 100: return "ARCHITECT 🌌"
    if lvl >= 50: return "GOD MODE ⚡"
    if lvl >= 20: return "CYBER LORD 💀"
    if lvl >= 10: return "NETRUNNER 🖥️"
    return "SCRIPT KIDDIE 🐣"

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    rank = get_rank(db["level"])
    await m.answer(
        f"🌐 **NEURAL TERMINAL v14.0 ONLINE**\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 User: `{m.from_user.first_name}`\n"
        f"🏆 Rank: **{rank}**\n"
        f"⚙️ System Level: `{db['level']}`\n"
        f"💰 Balance: `{db['balance']:.6f} XMR`\n"
        f"━━━━━━━━━━━━━━\n"
        f"🕹 **AVAILABLE MODULES:**\n"
        f"┣ `/mine` — Start crypto extraction\n"
        f"┣ `/hack` — Execute network breach\n"
        f"┣ `/upgrade` — Buy hardware (Cost: {(db['level']*0.015):.3f})\n"
        f"┣ `/wallet` — View assets and XP\n"
        f"┗ `/status` — System diagnostics"
    )

@dp.message(Command("mine"))
async def cmd_mine(m: types.Message):
    if db["mining"]:
        await m.reply("🚫 **ERROR:** Multithreading restricted. Process active.")
        return
    
    db["mining"] = True
    st = await m.answer("🔌 **CONNECTING TO HASH-POOL...**")
    
    for i in range(5):
        profit = (random.uniform(0.0005, 0.0015)) * db["level"]
        db["balance"] += profit
        db["xp"] += 12
        bar = "■" * (i + 1) + "□" * (4 - i)
        await st.edit_text(f"⛏ **MINING CORE**\n`[{bar}]` {2
      
