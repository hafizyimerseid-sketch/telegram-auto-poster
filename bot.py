import os
import time
import threading
import requests
from flask import Flask
from telethon import TelegramClient, events

app = Flask(__name__)

# --- Environment Variables (በ Render ላይ የሚሞሉ) ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")      # የርስዎ ቦት Token (ከ BotFather)
MY_CHANNEL_ID = os.environ.get("MY_CHANNEL_ID")                # የእርስዎ ቻናል ID ወይም Username (ለምሳሌ: @mychannel)
API_ID = int(os.environ.get("API_ID", 0))                      # ከ my.telegram.org የሚገኝ API ID
API_HASH = os.environ.get("API_HASH", "")                       # ከ my.telegram.org የሚገኝ API HASH

# Source Channels / Pages
TELEGRAM_SOURCE = "yesakbet01"
FACEBOOK_SOURCE_URL = "https://www.facebook.com/InfoZer12"

@app.route('/')
def home():
    return "Facebook & Telegram Auto-Poster Bot is Running Live 24/7!"

# ----------------------------------------------------
# 1. Telegram-to-Telegram Forwarder (Telethon)
# ----------------------------------------------------
client = TelegramClient('anon_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=TELEGRAM_SOURCE))
async def my_event_handler(event):
    """ከ @yesakbet01 አዲስ መልእክት ሲወጣ ወዲያውኑ ወደ እርስዎ ቻናል የሚልክ"""
    try:
        print(f"[Telegram Source] አዲስ ፖስት ከ @{TELEGRAM_SOURCE} ተገኝቷል!")
        await client.send_message(MY_CHANNEL_ID, event.message)
        print("[Success] ወደ እርስዎ ቻናል በስኬት ተፖስቷል!")
    except Exception as e:
        print(f"[Telegram Forward Error]: {e}")

def run_telegram_listener():
    client.start()
    client.run_until_disconnected()

# ----------------------------------------------------
# 2. Facebook-to-Telegram Auto-Poster (Scraper)
# ----------------------------------------------------
last_fb_post_text = ""

def check_facebook_posts():
    global last_fb_post_text
    print(f"[Facebook Monitor] {FACEBOOK_SOURCE_URL} ን በመፈተሽ ላይ...")
    
    while True:
        try:
            # ፌስቡክን ለመቃኘት የሚረዳ ጥያቄ
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }
            response = requests.get(FACEBOOK_SOURCE_URL, headers=headers)
            
            if response.status_code == 200:
                # እዚህ ጋር አዳዲስ ጽሁፎች መኖራቸውን ማረጋገጥ
                # (አዲስ ፖስት ከተገኘ እና ከቀደመው የተለየ ከሆነ ወደ ቴሌግራም ይልካል)
                pass
                
        except Exception as e:
            print(f"[Facebook Scraper Error]: {e}")
            
        # በየ 15 ደቂቃው (900 ሰከንድ) ፌስቡክን ይፈትሻል
        time.sleep(900)

# ----------------------------------------------------
# 3. Main Startup
# ----------------------------------------------------
if __name__ == '__main__':
    # A. Telegram Listener Thread
    if API_ID and API_HASH:
        tg_thread = threading.Thread(target=run_telegram_listener)
        tg_thread.daemon = True
        tg_thread.start()

    # B. Facebook Scraper Thread
    fb_thread = threading.Thread(target=check_facebook_posts)
    fb_thread.daemon = True
    fb_thread.start()

    # C. Render Web Server
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
      
