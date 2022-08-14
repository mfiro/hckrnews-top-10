import requests

class Client:
    base_url = 'https://hacker-news.firebaseio.com/v0/'

    def __init__(self):
        pass

    def _request(self, url):
        r = requests.get(url)
        r = r.json()
        return r

    def get_item(self, item_id):
        url = f"{self.__class__.base_url}/item/{item_id}.json"
        return self._request(url)
