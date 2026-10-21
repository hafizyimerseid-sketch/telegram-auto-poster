import os
import time
import threading
import requests
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route('/')
def home():
    return "Bot Testing Status Page"

def test_telegram_connection():
    time.sleep(5)  # ሰርቨሩ በበራ በ 5 ሰከንድ ውስጥ ይሞክራል
    print("=== STARTING DIRECT TELEGRAM TEST ===")
    print(f"Checking BOT_TOKEN: {BOT_TOKEN[:5] if BOT_TOKEN else 'MISSING'}")
    print(f"Checking CHAT_ID: {CHAT_ID}")
    
    if BOT_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": "🚨 የሙከራ መልእክት፡ ቦቱ አሁን በ Render ላይ በስኬት እየሰራ ነው!"
        }
        
        try:
            res = requests.post(url, json=payload)
            print(f"Telegram API Response Code: {res.status_code}")
            print(f"Telegram API Response Text: {res.text}")
        except Exception as e:
            print(f"Network Error: {e}")
    else:
        print("ERROR: BOT_TOKEN ወይም CHAT_ID በ Render Environment Variables ላይ አልተሞላም!")

if __name__ == '__main__':
    t = threading.Thread(target=test_telegram_connection)
    t.daemon = True
    t.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
