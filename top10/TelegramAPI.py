import requests

class Client:
    base_url = 'https://api.telegram.org/'

    def __init__(self, api_key):
        self.api_key = api_key

    def send_message(self, channel_id, message, reply_markup=None):
        data = {
            "chat_id": channel_id,
            "text": message,
            "parse_mode": "Markdown",
            'disable_web_page_preview': True
        }
        if reply_markup:
            data["reply_markup"] = reply_markup

        response = requests.post(
            f"{self.base_url}{self.api_key }/sendMessage", data=data
        )

        return response
