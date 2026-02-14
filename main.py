import os
import time
import tweepy
import requests
from dotenv import load_dotenv

# ========================
# LOAD ENV
# ========================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")

required = {
    "GROQ_API_KEY": GROQ_API_KEY,
    "X_API_KEY": X_API_KEY,
    "X_API_SECRET": X_API_SECRET,
    "X_ACCESS_TOKEN": X_ACCESS_TOKEN,
    "X_ACCESS_SECRET": X_ACCESS_SECRET,
}

missing = [k for k, v in required.items() if not v]
if missing:
    raise RuntimeError(f"❌ Missing env vars: {', '.join(missing)}")

print("✅ Env loaded")

# ========================
# X CLIENT (OAuth 1.0a)
# ========================
auth = tweepy.OAuth1UserHandler(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_SECRET,
)
x_client = tweepy.API(auth)

# ========================
# GROQ TEXT GENERATION
# ========================
def generate_text():
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": "Ты AI-помощник для Twitter (X). Пиши короткие, полезные, дружелюбные посты. Без эмодзи спама. До 200 символов."
            },
            {
                "role": "user",
                "content": "Сгенерируй интересный пост про AI, технологии или личную продуктивность."
            }
        ],
        "temperature": 0.9,
        "max_tokens": 120,
    }

    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

# ========================
# CONFIG
# ========================
POST_INTERVAL_SECONDS = 60 * 60  # 1 пост в час (безопасно)

print("🚀 Twitter AI helper started")
print("🧠 Groq text generation enabled")
print("🟢 Mode: NO SEARCH (free)")
print("✍️ Auto-posting with AI")

# ========================
# MAIN LOOP
# ========================
while True:
    try:
        text = generate_text()
        x_client.update_status(status=text)
        print("✅ Posted:", text)

        time.sleep(POST_INTERVAL_SECONDS)

    except Exception as e:
        # НЕ ПАДАЕМ
        print("⚠️ Error:", str(e))
        time.sleep(120)
