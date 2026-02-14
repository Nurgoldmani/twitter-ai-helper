import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# 🔑 Клиент Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/", methods=["GET"])
def health():
    return "OK", 200


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # ✅ messages — СТРОГО ТАК
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": user_message}
    ]

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )

        answer = response.choices[0].message.content
        return jsonify({"reply": answer})

    except Exception as e:
        print("GROQ ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
