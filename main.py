import os
from groq import Groq
import time

# ====== НАСТРОЙКИ ======
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set")

MODEL = "llama-3.1-8b-instant"

client = Groq(api_key=GROQ_API_KEY)

# ====== ОСНОВНОЙ ЦИКЛ (чтобы Railway не падал) ======
def main():
    while True:
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": "Ping"}
                ]
            )

            print("AI response:", response.choices[0].message.content)

        except Exception as e:
            print("ERROR:", e)

        time.sleep(30)  # чтобы сервис жил и не крашился


if __name__ == "__main__":
    main()
