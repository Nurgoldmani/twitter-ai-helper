import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from groq import Groq

# Логи
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Переменные окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN не задан")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY не задан")

# Groq клиент
groq = Groq(api_key=GROQ_API_KEY)

def ask_ai(text: str) -> str:
    try:
        completion = groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Ты полезный AI помощник."},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"GROQ ERROR: {e}")
        return "⚠️ Ошибка AI, попробуй позже."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    reply = ask_ai(text)
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("🤖 Telegram AI бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
