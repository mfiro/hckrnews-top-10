import json
import requests
from top10.config import TELEGRAM_API_KEY, TELEGRAM_URL

def send_message(chat_id, message, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        'disable_web_page_preview': True,
    }
    if reply_markup:
        data["reply_markup"] = reply_markup

    response = requests.post(
        f"{TELEGRAM_URL}{TELEGRAM_API_KEY}/sendMessage", data=data
    )

    return response
