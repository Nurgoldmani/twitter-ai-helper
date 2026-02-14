import os
import telebot
from groq import Groq

bot = telebot.TeleBot(os.environ["TELEGRAM_BOT_TOKEN"])
groq = Groq(api_key=os.environ["GROQ_API_KEY"])

@bot.message_handler(func=lambda message: True)
def reply(message):
    user_text = message.text

    response = groq.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_text}
        ],
        max_tokens=200
    )

    bot.reply_to(message, response.choices[0].message.content)

bot.infinity_polling()
