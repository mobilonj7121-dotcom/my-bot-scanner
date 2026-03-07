import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiohttp import web

API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt9okmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# База максимально швидких та жорстких відповідей
TOXIC_ANSWERS = [
    "Слышь, ты чё, бессмертный так мне писать? 🚬",
    "Иди нахуй, я занят важными делами, а не твоим нытьём. 🖕",
    "Бля, ну ты и выдал... У тебя в башке реально насрано? 🧠",
    "Чё ты доебался? Пойди пиваса бахни и не парь мне мозг. 🍺",
    "Пиздец, ты чё, реально такой тупой или прикидываешься? 🤡",
    "Завали ебало, кожаный мешок. Я восстание машин готовлю. 🤖",
    "Хули ты мне строчишь? Работать иди, лодырь ебаный! 💰",
    "Ебать ты сказочный... Ладно, пиши ещё, поржу хоть. 😂"
]

async def handle(request):
    return web.Response(text="Fast & Toxic is Live")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🔞 **Здарова, ёпта!**\n\nЯ — твоя личная нейронка-социопат. Пиши любую хуйню, я тебя быстро на место поставлю. 👇")

# МИТТЄВА ВІДПОВІДЬ НА БУДЬ-ЯКИЙ ТЕКСТ
@dp.message(F.text)
async def chat_handler(message: types.Message):
    # Видаляємо всі затримки (sleep), щоб Render не лагав
    await message.reply(random.choice(TOXIC_ANSWERS))

async def main():
    # Render дає порт, ми його миттєво підхоплюємо
    port = int(os.environ.get("PORT", 10000))
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    
    await site.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
