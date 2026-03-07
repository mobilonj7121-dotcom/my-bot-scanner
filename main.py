import asyncio
import os
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# Твій токен
API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt9okmDqDrwzvDMwqOjO8is'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Рандомні хакерські фрази для чату
SCARY_MESSAGES = [
    "💉 Впровадження вірусу в ядро системи... Done.",
    "📸 Фронтальна камера активована. Ну й харя у тебе, звичайно. 😂",
    "💾 Копіюю папку 'Private'... Ого, які цікаві відео у тебе збережені.",
    "🔓 Пароль від твого банку підібрано. Дякую за донат, лох. 💰",
    "📡 Твій IP: 178.214.{r1}.{r2}. Я вже виїхав, чекай. 👊",
    "🕵️‍♂️ Твоя колишня зараз читає твої переписки. Я допоміг."
]

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "💀 **SYSTEM CRITICAL ERROR** 💀\n\n"
        "Ти тільки що активував протокол самознищення конфіденційності. "
        "Твій телефон тепер належить мені. Пиши щось, якщо не сциш, або кидай контакт жертви. 👇"
    )

# Реакція на будь-який текст
@dp.message(F.text)
async def hack_text(message: types.Message):
    # Кожна відповідь — це випадковий "етап зламу"
    msg = random.choice(SCARY_MESSAGES).format(
        r1=random.randint(10, 255), 
        r2=random.randint(10, 255)
    )
    await message.reply(f"⚠️ **[HACK_LOG]:** {msg}")

# Реакція на контакт (повний звіт про злам)
@dp.message(F.contact)
async def hack_contact(message: types.Message):
    contact = message.contact
    
    # Етап залякування
    status = await message.answer(f"🎯 Ціль: {contact.first_name}. Починаю розтин пристрою...")
    await asyncio.sleep(2)
    
    await status.edit_text("📡 Підключення до iCloud/Google Drive... Успішно.")
    await asyncio.sleep(2)
    
    await message.answer(
        f"✅ **ЗЛАМ ОБ'ЄКТА +{contact.phone_number} ЗАВЕРШЕНО:**\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 **Жертва:** {contact.first_name} {contact.last_name or ''}\n"
        f"💳 **Банківські карти:** Дані злито в даркнет.\n"
        f"💬 **Останні діалоги:** Перехоплено.\n"
        f"📸 **Галерея:** 1.2 ГБ компромату завантажено.\n"
        f"🎧 **Мікрофон:** Прослуховування активовано.\n"
        f"━━━━━━━━━━━━━━\n"
        f"🤡 *Передай йому привіт. Його життя тепер у моїх руках.*"
    )

async def main():
    # Видаляємо вебхуки для стабільності на Free тарифі
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
