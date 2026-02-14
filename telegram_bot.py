import os
import telebot
from groq import Groq

# 🔑 Токены
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
groq = Groq(api_key=GROQ_API_KEY)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Привет! 👋\nЯ AI-бот. Напиши любой вопрос — я отвечу."
    )

@bot.message_handler(func=lambda message: True)
def reply(message):
    user_text = message.text.strip()

    if not user_text:
        bot.reply_to(message, "Напиши текст 🙂")
        return

    try:
        response = groq.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Reply briefly."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=200,
            temperature=0.7
        )

        answer = response.choices[0].message.content
        bot.reply_to(message, answer)

    except Exception as e:
        print("GROQ ERROR:", e)
        bot.reply_to(message, "Ошибка 😕 Попробуй позже.")
