import os
import time
import threading
import requests
from flask import Flask

app = Flask(__name__)

# Render Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# የሚፖስቱ ማስታወቂያዎች/መልእክቶች
MESSAGES = [
    "📢 እንኳን ወደ ቻናላችን በሰላም መጡ! አዳዲስ መረጃዎችን እዚህ ያገኛሉ።",
    "💡 በየቀኑ የሚወጡ አዳዲስ የገበያ መረጃዎችን እና ትንተናዎችን ይከታተሉ።",
    "🚀 ስለተከታተሉን እናመሰግናለን!"
]

@app.route('/')
def home():
    return "Telegram Auto-Poster Bot is Fully Active!"

def post_messages():
    print("=== Telegram Auto-Poster Loop Started ===")
    index = 0
    while True:
        try:
            if BOT_TOKEN and CHAT_ID:
                text = MESSAGES[index % len(MESSAGES)]
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                payload = {"chat_id": CHAT_ID, "text": text}
                
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    print(f"[Auto-Poster] መልእክቱ ተፖስቷል: {text}")
                else:
                    print(f"[Auto-Poster Error] መፖስት አልተቻለም: {response.text}")
            else:
                print("[Warning] BOT_TOKEN ወይም CHAT_ID በ Render ላይ አልተሞላም!")

            index += 1
        except Exception as e:
            print(f"[Exception Error]: {e}")

        # በየ 2 ሰዓቱ (7200 ሰከንድ) ማስታወቂያ ይፖስታል
        time.sleep(7200)

if __name__ == '__main__':
    # Threading
    t = threading.Thread(target=post_messages)
    t.daemon = True
    t.start()

    # Flask Server for Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
