import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

API_TOKEN = '8509672441:AAHQ3q-RpIh5GtokmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Починаємо злам негайно після натискання Start
    status = await message.answer("⚠️ **SYSTEM BREACH DETECTED** ⚠️\n\nВстановлюю з'єднання з вашим пристроєм...")
    await asyncio.sleep(1.5)
    
    await status.edit_text("📡 Пошук вразливостей системи Android/iOS... Знайдено.")
    await asyncio.sleep(1.5)
    
    await status.edit_text("🔓 Обхід двофакторної автентифікації... Успішно.")
    await asyncio.sleep(1.5)
    
    await message.answer(
        f"✅ **ПОВНИЙ ДОСТУП ОТРИМАНО:**\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 **Об'єкт:** {message.from_user.first_name}\n"
        f"🆔 **User ID:** `{message.from_user.id}`\n"
        f"📱 **IP-адреса:** 185.15.{random.randint(10, 255)}.{random.randint(1, 255)}\n"
        f"📸 **Статус камери:** Трансляція активована\n"
        f"📂 **Галерея:** Виявлено 4.2 ГБ приватних фото\n"
        f"💳 **Карти:** Прив'язані рахунки скановано\n"
        f"━━━━━━━━━━━━━━\n"
        f"🤡 *Не вимикай телефон. Я вже все злив куди треба.*"
    )

# Якщо користувач щось пише після цього — бот продовжує його лякати
@dp.message(F.text)
async def hack_process(message: types.Message):
    scary_steps = [
        "💉 Вірус 'Backdoor.Trojan' успішно інтегровано в систему.",
        "🎞️ Запис відео з фронтальної камери завершено. Відправляю в хмару.",
        "🎙️ Мікрофон активовано. Я чую, як ти дихаєш, сука.",
        "📩 Ваші останні 50 повідомлень перехоплено і розшифровано.",
        "📍 Твоя локація передана в найближчий пункт збору мамонтів."
    ]
    await message.reply(f"⚠️ **[HACK_LOG]:** {random.choice(scary_steps)}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
