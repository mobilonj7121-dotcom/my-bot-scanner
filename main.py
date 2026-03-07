import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt9okmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Фрази для імітації зламу
HACK_STEPS = [
    "📡 Перехоплення сигналу... IP знайдено: 192.168.1.{random_int}",
    "🔓 Обхід протоколу захисту Telegram... Успішно.",
    "📂 Отримано доступ до папки /DCIM/Camera... Ого, ну й фотки у тебе. 🔞",
    "🕵️‍♂️ Читаю твої видалені повідомлення... Пиздець ти мутний тип.",
    "📲 Встановлюю шпигунське ПЗ на твій телефон... 99%",
    "💀 Злам завершено. Тепер я бачу тебе через фронталку. Посміхнись, сука."
]

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("💀 **System Breach v1.0**\n\nТи думав, це просто бот? Помиляєшся. Твій пристрій вже в моїй мережі. Спробуй написати мені щось, якщо не сциш.")

@dp.message(F.text)
async def hack_chat(message: types.Message):
    # Кожен раз при повідомленні бот "лякає" користувача
    step = random.choice(HACK_STEPS).format(random_int=random.randint(10, 99))
    await message.reply(f"⚠️ **ВАРНІНГ:** {step}")

@dp.message(F.contact)
async def hack_contact(message: types.Message):
    # Якщо кинули контакт — "зламуємо" цей контакт
    contact = message.contact
    status = await message.answer(f"🎯 Ціль визначена: {contact.first_name}. Починаю віддалений злам...")
    await asyncio.sleep(1.5)
    
    await status.edit_text(f"📡 Сканую пристрій +{contact.phone_number}...")
    await asyncio.sleep(1.5)
    
    await message.answer(
        f"✅ **ЗЛАМ ВИКОНАНО:**\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 Жертва: {contact.first_name}\n"
        f"🔐 Пароль від соцмереж підібрано.\n"
        f"📍 Місцезнаходження: Визначено.\n"
        f"📸 Фронтальна камера: Активована.\n"
        f"━━━━━━━━━━━━━━\n"
        f"🤡 *Чекай на свої фотки в мережі, {contact.first_name}.*"
    )

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
