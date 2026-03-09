import os
import telebot
from groq import Groq
from flask import Flask
from threading import Thread

# Flask (Render အတွက် လိုအပ်သည်)
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

# API Keys များကို Environment Variable မှ ဖတ်ယူခြင်း
bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])
client = Groq(api_key=os.environ['GROQ_API_KEY'])

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": message.text}],
            model="llama3-8b-8192",
        )
        bot.reply_to(message, chat_completion.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

def run_bot(): bot.infinity_polling()
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_bot()
