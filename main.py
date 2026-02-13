import os
import time
from groq import Groq

# ====== ПРОВЕРКА КЛЮЧА ======
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")

# ====== АКТУАЛЬНАЯ МОДЕЛЬ GROQ ======
MODEL = "llama-3.1-8b-instant"

client = Groq(api_key=GROQ_API_KEY)

def main():
    print("Service started")

    while True:
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": "Ping"}
                ]
            )

            print("AI:", response.choices[0].message.content)

        except Exception as e:
            print("ERROR:", e)

        time.sleep(20)  # Railway-friendly loop


if __name__ == "__main__":
    main()
