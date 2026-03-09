import os
import telebot
from openai import OpenAI
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

# Key များကို Environment Variable ကနေ ဖတ်ယူခြင်း
bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

@bot.message_handler(func=lambda message: True)
def chat(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message.text}]
    )
    bot.reply_to(message, response.choices[0].message.content)

def run_bot(): bot.polling()
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_bot()
