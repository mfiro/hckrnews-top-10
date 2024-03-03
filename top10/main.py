import datetime
import time
from hn import Client

from top10.TelegramAPI import Client as TGClient
from top10.config import CHAT_ID, CHAT_ID_TEST, TELEGRAM_API_KEY
from top10.helpers import save_json, load_json


def get_hn_client():
    return Client()


def get_telegram_client(api_key):
    return TGClient(api_key)


def fetch_best_stories(hn_client, filename):
    best_stories = hn_client.get_beststories()
    stories_data = []
    for story_id in sorted(best_stories, reverse=True):
        try:
            print(f"Getting item {story_id}")
            story_data = hn_client.get_item(story_id)
            time.sleep(0.1)  # Respectful pause to avoid rate limiting
            stories_data.append(story_data)
        except Exception as e:
            print(f"Failed to fetch story {story_id}: {e}")
            continue  # Skip this story and continue with the next
    save_json(stories_data, filename)

    # Sort the stories based on scores.
    if stories_data:
        stories_data = sorted(stories_data, key=lambda x: x['score'], reverse=True)
    return stories_data


def filter_todays_stories(stories, today):
    return [story for story in stories if datetime.datetime.utcfromtimestamp(story['time']).date() == today]


def create_message(stories):
    message = ""
    for no, story in enumerate(stories[:10], start=1):
        message += f"{no}. {story['title']} | [Article]({story['url']}) | [Comments ({story['descendants']})](https://news.ycombinator.com/item?id={story['id']}) | Score:{story['score']}\n"
    message += f"_Last updated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC_"
    return message


def main():
    hn_client = get_hn_client()
    telegram_client = get_telegram_client(TELEGRAM_API_KEY)
    debug_mode = False
    today = datetime.datetime.utcnow().date()
    filename = f'data_{today}.json'
    chat_id = CHAT_ID_TEST if debug_mode else CHAT_ID

    if not debug_mode:
        data = fetch_best_stories(hn_client, filename)
    else:
        data = load_json(filename)
        data = sorted(data, key=lambda x: x['score'], reverse=True)
        
    todays_stories = filter_todays_stories(data, today)
    if not todays_stories and not debug_mode:  # fallback to yesterday's data if no today's stories
        todays_stories = filter_todays_stories(data, today - datetime.timedelta(days=1))
    
    if todays_stories:
        message = create_message(todays_stories)
        telegram_client.send_message(chat_id, message)
    else:
        print("No relevant stories to send.")


if __name__ == '__main__':
    main()

    