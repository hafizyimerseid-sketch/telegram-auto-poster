import os
import time
import threading
import requests
from flask import Flask

app = Flask(__name__)

# Config - Environment Variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CHANNEL_ID = os.environ.get("MY_CHANNEL_ID")

@app.route('/')
def home():
    return "Telegram Auto-Poster Bot is Active and Live 24/7!"

def send_telegram_post(text):
    """ወደ ቴሌግራም ቻናልዎ መረጃ የሚልክ ተግባር"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": MY_CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("[Auto-Poster] መልእክቱ/ማስታወቂያው በስኬት ተፖስቷል!")
        else:
            print(f"[Auto-Poster Error]: {response.text}")
    except Exception as e:
        print(f"[Exception]: {e}")

def auto_poster_loop():
    """በየተወሰነ ሰዓቱ አውቶማቲክ ፖስት የሚያደርግ ሉፕ"""
    print("=== Auto-Poster Loop Started ===")
    
    posts = [
        "📢 *ማስታወቂያ:* ወደ እኛ የቴሌግራም ቻናል እንኳን ደህና መጡ! አዳዲስ የትሬዲንግ መረጃዎች እዚህ ይለቀቃሉ።",
        "💡 *የቀኑ ማስታወሻ:* በትሬዲንግ ወቅት ስሜትን መቆጣጠር እና Risk Management መጠቀም አስፈላጊ ነው!",
        "📊 *Exness Auto-Trading Bot:* አውቶማቲክ የትሬዲንግ ቦታችን 24/7 ገበያውን በመከታተል ላይ ይገኛል!"
    ]
    
    index = 0
    while True:
        try:
            current_post = posts[index % len(posts)]
            send_telegram_post(current_post)
            
            index += 1
            # በየ 2 ሰዓቱ (7200 ሰከንድ) ይፖስታል
            time.sleep(7200) 
            
        except Exception as e:
            print(f"Error in Auto-Poster loop: {e}")
            time.sleep(60)

if __name__ == '__main__':
    # 1. Auto-Poster thread
    poster_thread = threading.Thread(target=auto_poster_loop)
    poster_thread.daemon = True
    poster_thread.start()

    # 2. Render Web Server
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
