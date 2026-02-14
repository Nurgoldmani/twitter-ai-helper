import os
import threading
from flask import Flask
from telegram_bot import bot

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return "OK", 200


def run_telegram():
    print("Telegram bot started")
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    # 🔁 Запуск Telegram-бота в отдельном потоке
    threading.Thread(target=run_telegram, daemon=True).start()

    # 🌐 Запуск Flask (для Railway)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
