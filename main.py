import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# Твій токен
API_TOKEN = '8509672441:AAHQ3q-RpIh5Gt78vU8m-62M2-S-N0w0W_A'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="Bot is Live!")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("✅ Бот працює!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    
    await asyncio.gather(site.start(), dp.start_polling(bot))

if __name__ == "__main__":
    asyncio.run(main())
    
