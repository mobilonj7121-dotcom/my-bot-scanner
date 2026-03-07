import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Твой токен
API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt9okmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Список максимально коротких и дерзких ответов
ANSWERS = [
    "Слышь, хули ты так долго думал, пока это писал? 🚬",
    "Иди нахуй, я занят. 🖕",
    "Бля, ну ты и выдал... Мозги купи, а. 🧠",
    "Чё надо, кожаный? Опять тупишь? 🤡",
    "Завали ебало, я отдыхаю. 🤖",
    "Хули ты мне строчишь, иди работай, сука! 💰",
    "Пиздец ты сказочный долбоёб... 😂",
    "Твоё мнение очень важно (нет, пошёл нахуй). 🖕"
]

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🔞 **Здарова!** Пиши чё хочешь, я тебя быстро на место поставлю. 👇")

# Мгновенная реакция без asyncio.sleep
@dp.message(F.text)
async def chat_handler(message: types.Message):
    await message.reply(random.choice(ANSWERS))

async def main():
    # Удаляем веб-сервер, оставляем только поллинг для скорости на Free тарифе
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
