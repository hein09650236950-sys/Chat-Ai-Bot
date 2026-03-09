import os, telebot, threading
from flask import Flask
from openai import OpenAI

# 1. Flask Web Service
app = Flask('')
@app.route('/')
def home(): return "Bot is live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))).start()

# 2. AI & Bot Setup
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

# 3. AI အလုပ်လုပ်ပုံ
@bot.message_handler(func=lambda m: True)
def chat(m):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": m.text}]
    )
    bot.reply_to(m, response.choices[0].message.content)

bot.infinity_polling()
