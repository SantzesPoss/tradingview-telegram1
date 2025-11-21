from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
PASSPHRASE = os.getenv('PASSPHRASE', 'change_me_now')

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        'chat_id': CHAT_ID,
        'text': f" {text}",
        'parse_mode': 'Markdown'
    }).json()

@app.route('/', methods=['GET'])
def home():
    return "TradingView → Telegram bot is alive!"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json(force=True) or {}
    
    if data.get('passphrase') != PASSPHRASE:
        return 'Wrong passphrase', 403
    
    message = data.get('message') or 'TradingView alert!'
    send_telegram(message)
    
    return 'Sent to Telegram!', 200

# Vercel needs this exact line
app = app
