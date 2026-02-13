import os
import time
import requests

# =========================
# НАСТРОЙКИ
# =========================

X_USERNAME = "nurgoldman13"   # твой @username БЕЗ @
CHECK_INTERVAL = 60           # проверка раз в 60 секунд

X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

if not X_BEARER_TOKEN:
    raise RuntimeError("❌ Не найден X_BEARER_TOKEN в переменных окружения")

HEADERS = {
    "Authorization": f"Bearer {X_BEARER_TOKEN}",
    "Content-Type": "application/json"
}

# =========================
# ФУНКЦИИ
# =========================

def get_mentions():
    """
    Ищем упоминания @username, кроме своих твитов
    """
    url = "https://api.x.com/2/tweets/search/recent"
    params = {
        "query": f"@{X_USERNAME} -from:{X_USERNAME}",
        "tweet.fields": "author_id,conversation_id,created_at",
        "max_results": 5
    }

    r = requests.get(url, headers=HEADERS, params=params)
    print("🔍 SEARCH STATUS:", r.status_code)
    print(r.text)

    if r.status_code != 200:
        return []

    data = r.json()
    return data.get("data", [])


def reply_to_tweet(tweet_id, text):
    """
    Ответ на твит
    """
    url = "https://api.x.com/2/tweets"
    payload = {
        "text": text,
        "reply": {
            "in_reply_to_tweet_id": tweet_id
        }
    }

    r = requests.post(url, headers=HEADERS, json=payload)
    print("💬 REPLY STATUS:", r.status_code)
    print(r.text)


# =========================
# ОСНОВНОЙ ЦИКЛ
# =========================

def main():
    print("🚀 Twitter AI helper запущен")

    answered = set()  # чтобы не отвечать дважды

    while True:
        try:
            mentions = get_mentions()

            for tweet in mentions:
                tweet_id = tweet["id"]

                if tweet_id in answered:
                    continue

                reply_to_tweet(
                    tweet_id,
                    "👋 Привет! Бот работает и отвечает автоматически."
                )

                answered.add(tweet_id)

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print("❌ Ошибка:", e)
            time.sleep(30)


if __name__ == "__main__":
    main()
