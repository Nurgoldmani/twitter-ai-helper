import os
import time
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
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")  # optional

# ========================
# CHECK REQUIRED VARS
# ========================
required_vars = {
    "GROQ_API_KEY": GROQ_API_KEY,
    "X_API_KEY": X_API_KEY,
    "X_API_SECRET": X_API_SECRET,
    "X_ACCESS_TOKEN": X_ACCESS_TOKEN,
    "X_ACCESS_SECRET": X_ACCESS_SECRET,
}

missing = [k for k, v in required_vars.items() if not v]

if missing:
    raise RuntimeError(f"❌ Missing env vars: {', '.join(missing)}")

print("✅ All required environment variables loaded")

# ========================
# CONFIG
# ========================
NO_SEARCH = True  # 🔕 IMPORTANT: disable search (no credits mode)
IDLE_SLEEP_SECONDS = 60 * 30  # 30 minutes

print("🚀 Twitter AI helper started")
print("🟢 Mode: NO SEARCH (free mode)")
print("🧠 Groq ready")
print("⏳ Idle mode started")

# ========================
# MAIN LOOP (IDLE)
# ========================
while True:
    try:
        # 🔕 SEARCH IS DISABLED
        if NO_SEARCH:
            print("😴 Idle... waiting (no search, no credits)")
        
        # ⏱ sleep to avoid bans
        time.sleep(IDLE_SLEEP_SECONDS)

    except Exception as e:
        # NEVER CRASH CONTAINER
        print("⚠️ Runtime warning:", str(e))
        time.sleep(60)
