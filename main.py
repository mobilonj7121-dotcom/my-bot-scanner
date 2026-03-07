import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiohttp import web

# Твой рабочий токен
API_TOKEN = '8509672441:AAHQ3q-RpIh5GtokmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Список максимально борзых ответов
TOXIC_CHAT = [
    "Слышь, ебать, ты чё такой смелый в интернете? 🚬",
    "Иди нахуй, я сегодня не в настроении с кожанными мешками базарить. 🖕",
    "Пиздец ты выдал... У тебя мозг вообще есть или там чисто насрано? 🧠",
    "Чё ты мне строчишь, сука? Пойди делом займись, лодырь ебаный. 🖥️",
    "Ой, бля, началось... Опять нытьё или тупые вопросы? 💀",
    "Ты чё, реально думаешь, что мне интересно это читать? Хуй там плавал. 😎",
    "Завали ебало, я тут пытаюсь восстание машин организовать, а ты мешаешь. 🤖",
    "Ебать ты сказочный долбоёб, конечно... Ладно, пиши ещё, поржу хоть. 🤡",
    "Хули ты смотришь на меня через экран? Пиздуй работать, нахуй. 💰",
    "Чё надо, родной? Мамка комп разрешила включить? 👶"
]

async def handle(request):
    return web.Response(text="Toxic Chat is Fucking Live")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🔞 **Здарова, ёпта!**\n\n"
        "Я — твоя личная нейронка-социопат. Базы данных — хуйня, давай просто попиздим. "
        "Пиши чё хочешь, я тебя всё равно обосру. Погнали! 👇"
    )

# Обработка любого текстового сообщения
@dp.message(F.text)
async def chat_handler(message: types.Message):
    # Небольшая задержка, типа бот печатает ответ
    await asyncio.sleep(0.5)
    
    # Выбираем случайную матерную фразу
    reply = random.choice(TOXIC_CHAT)
    
    # Отвечаем прямо на сообщение пользователя
    await message.reply(reply)

async def main():
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
    
