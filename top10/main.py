import datetime
import json
import time
from top10.hn import Client


def save_json(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)
        print(f"Data saved to {filename}")

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data



if __name__ == '__main__':
    hn_client = Client()
    live_mode = False
    filename = f'data_{str(datetime.datetime.now())[:10]}.json'

    # Get best stories
    if live_mode:
        best = hn_client.get_beststories()
        best_sorted = sorted(best, reverse=True)
        data = []
        for id_ in best_sorted:
            print(f"Getting item {id_}")
            item = hn_client.get_item(id_)
            time.sleep(0.1)
            data.append(item)
        save_json(data, filename)       
    else:
        data = load_json(filename)
        
    # Now what to do? 
    x = 1
    