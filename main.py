import os
import asyncio
from groq import Groq
from aiogram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = Bot(token=BOT_TOKEN)
groq = Groq(api_key=GROQ_API_KEY)

async def main():
    response = groq.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": "Напиши короткий умный ответ на твит про AI и стартапы"}
        ]
    )

    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"💡 Ответ от Groq:\n\n{response.choices[0].message.content}"
    )

asyncio.run(main())
