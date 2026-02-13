import os
import time
import requests
from groq import Groq
from requests_oauthlib import OAuth1

# ===== ENV =====
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ===== CLIENTS =====
groq_client = Groq(api_key=GROQ_API_KEY)

auth = OAuth1(
    X_API_KEY,
    X_API_SECRET,
    X_ACCESS_TOKEN,
    X_ACCESS_SECRET
)

SEARCH_URL = "https://api.twitter.com/2/tweets/search/recent"
REPLY_URL = "https://api.twitter.com/2/tweets"

replied_ids = set()

# ===== FUNCTIONS =====
def generate_ai_reply(text: str) -> str:
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a polite, neutral Twitter assistant. Reply briefly and naturally."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        max_tokens=120,
        temperature=0.6
    )
    return response.choices[0].message.content.strip()


def search_mentions():
    headers = {
        "Authorization": f"Bearer {X_BEARER_TOKEN}"
    }
    params = {
        "query": "@nurgoldman13 -is:retweet",
        "max_results": 10,
        "tweet.fields": "author_id"
    }

    r = requests.get(SEARCH_URL, headers=headers, params=params)
    if r.status_code != 200:
        print("❌ Search error:", r.text)
        return []

    return r.json().get("data", [])


def reply(tweet_id: str, text: str):
    payload = {
        "text": text,
        "reply": {"in_reply_to_tweet_id": tweet_id}
    }

    r = requests.post(REPLY_URL, auth=auth, json=payload)
    if r.status_code not in (200, 201):
        print("❌ Reply error:", r.text)
    else:
        print(f"✅ Replied to tweet {tweet_id}")


# ===== MAIN LOOP =====
print("🚀 Twitter AI helper started")

while True:
    try:
        tweets = search_mentions()
        for tweet in tweets:
            tid = tweet["id"]
            if tid in replied_ids:
                continue

            text = tweet["text"]
            ai_reply = generate_ai_reply(text)
            reply(tid, ai_reply)

            replied_ids.add(tid)
            time.sleep(15)  # anti-ban

    except Exception as e:
        print("🔥 ERROR:", e)

    time.sleep(60)
