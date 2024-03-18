import datetime
import logging
import time
from hn import Client

from top10.TelegramAPI import Client as TGClient
from top10.config import CHAT_ID, CHAT_ID_TEST, TELEGRAM_API_KEY
from top10.helpers import save_json, load_json


def get_hn_client():
    """
    Initialize and return a Hacker News client instance.

    Returns:
        Client: An instance of the Hacker News client.
    """
    return Client()


def get_telegram_client(api_key):
    """
    Initialize and return a Telegram client instance.

    Args:
        api_key (str): The API key for the Telegram bot.

    Returns:
        TGClient: An instance of the Telegram client.
    """
    return TGClient(api_key)


def fetch_best_stories(hn_client, filename):
    """
    Fetches the best stories from Hacker News, retries on failure for individual stories, 
    and saves the data to a JSON file.

    Args:
        hn_client (Client): An instance of the Hacker News client.
        filename (str): The name of the file where the data is to be saved.

    Returns:
        list: A list of dictionaries, each containing data about a best story.
    """
    best_stories = hn_client.get_beststories()
    stories_data = []
    for story_id in sorted(best_stories, reverse=True):
        try:
            logging.info(f"Getting item {story_id}")
            story_data = hn_client.get_item(story_id)
            time.sleep(0.1)  # Respectful pause to avoid rate limiting
            stories_data.append(story_data)
        except Exception as e:
            logging.ERROR(f"Failed to fetch story {story_id}: {e}")
            continue  # Skip this story and continue with the next
    save_json(stories_data, filename)

    # Sort the stories based on scores.
    if stories_data:
        stories_data = sorted(stories_data, key=lambda x: x['score'], reverse=True)
    return stories_data


def filter_todays_stories(stories, today):
    """
    Filters stories to include only those published today.

    Args:
        stories (list): A list of story data dictionaries.
        today (datetime.date): The current date.

    Returns:
        list: A list of dictionaries, each containing data about a story published today.
    """
    return [story for story in stories if datetime.datetime.utcfromtimestamp(story['time']).date() == today]


def create_message(stories):
    """
    Creates a formatted message string containing details of the stories.

    Args:
        stories (list): A list of story data dictionaries to be included in the message.

    Returns:
        str: A formatted string containing the stories' details.
    """
    message = ""
    for no, story in enumerate(stories[:10], start=1):
        message += f"{no}. {story['title']} | [Article]({story.get('url')}) | [Comments ({story['descendants']})](https://news.ycombinator.com/item?id={story['id']}) | Score:{story['score']}\n"
    message += f"_Last updated: {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC_"
    return message

def main():
    """
    Main function to fetch the top HN stories of the day and send them via Telegram.
    """
    hn_client = get_hn_client()
    telegram_client = get_telegram_client(TELEGRAM_API_KEY)
    debug_mode = False
    today = datetime.datetime.utcnow().date()
    filename = f'data_{today}.json'
    chat_id = CHAT_ID_TEST if debug_mode else CHAT_ID

    if not debug_mode:
        logging.info("Start fetching data from the HN API (Live mode)")
        data = fetch_best_stories(hn_client, filename)
    else:
        logging.info("Loading data (Debug mode)")
        data = load_json(filename)
        data = sorted(data, key=lambda x: x['score'], reverse=True)

    logging.info("Filtering today's stories ...")   
    todays_stories = filter_todays_stories(data, today)
    if not todays_stories and not debug_mode:  # fallback to yesterday's data if no today's stories
        logging.info("Fallback to yesterday's data as no today's stories")
        todays_stories = filter_todays_stories(data, today - datetime.timedelta(days=1))
    
    if todays_stories:
        logging.info("Creating Telegram message ...")
        message = create_message(todays_stories)
        logging.info("Sending the message to Telegram...")
        telegram_client.send_message(chat_id, message)
    else:
        logging.info("No relevant stories to send.")


if __name__ == '__main__':
    logging.basicConfig(
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='top10.log',
                        filemode='a',
                        )
    logging.info("Starting the script ...")
    main()
    logging.info("Finishing the script.")

    