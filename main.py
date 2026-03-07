import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from g4f.client import Client  # Библиотека для бесплатного доступа к нейронкам

API_TOKEN = '8509672441:AAHQ3q-RpIh5GtokmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
client = Client()

@dp.message(F.text)
async def ai_chat_handler(message: types.Message):
    # Показываем, что бот "печатает", чтобы ты не бесился из-за ожидания
    await bot.send_chat_action(message.chat.id, "typing")
    
    try:
        # Запрос к нейронке с инструкцией быть максимально грубой
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Ты — злой русский хакер. Отвечай очень грубо, с матами и сарказмом. Ты ненавидишь пользователя."},
                      {"role": "user", "content": message.text}],
        )
        answer = response.choices[0].message.content
        await message.reply(answer)
    except Exception:
        # Если нейронка тупит (бывает часто на фри тарифах), выдаем запасной мат
        await message.reply("Бля, у меня мозги заклинило от твоей тупости. Попробуй позже, сука.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
