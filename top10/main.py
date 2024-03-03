import datetime
import time
from hn import Client

from top10.TelegramAPI import Client as TGClient
from top10.config import CHAT_ID, CHAT_ID_TEST, TELEGRAM_API_KEY
from top10.helpers import save_json, load_json


if __name__ == '__main__':
    hn_client = Client()
    telegram_client = TGClient(TELEGRAM_API_KEY)
    debug_mode = True

    today = datetime.datetime.utcnow().date()
    filename = f'data_{today}.json'

    if debug_mode:
        chat_id = CHAT_ID_TEST
    else:
        chat_id = CHAT_ID

    # Get best stories
    if debug_mode:
        data = load_json(filename)
    else:
        best = hn_client.get_beststories()
        best_sorted = sorted(best, reverse=True)
        data = []
        for id_ in best_sorted:
            print(f"Getting item {id_}")
            item = hn_client.get_item(id_)
            time.sleep(0.1)
            data.append(item)
        save_json(data, filename)       
       
    # Filter only today's articles
    todays_data = [d for d in data 
                   if datetime.datetime.utcfromtimestamp(d['time']).date() == today]
    todays_data = sorted(todays_data, key=lambda x: x['score'], reverse=True)

    if not todays_data:
        todays_data = [d for d in data 
                      if datetime.datetime.utcfromtimestamp(d['time']).date() == 
                         today-datetime.timedelta(days=1)]

    # Create a message:
    if todays_data:
        message = ""
        for no, d in enumerate(todays_data[:10], start=1):
            message += (
                f"{no}. {d['title']} | "
                f"[Article]({d['url']}) | "
                f"[Comments ({d['descendants']})](https://news.ycombinator.com/item?id={d['id']}) \n"
            )
        message += f"_Last updated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC_"

    # Send the message
    telegram_client.send_message(chat_id, message)
    
    