import requests
import datetime


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
        item = self._request(url)
        if item.get('time'):
            item['time_str'] = str(datetime.datetime.fromtimestamp(item['time']))
        return item

    def get_topstories(self):
        url = f"{self.__class__.base_url}/topstories/.json"
        return self._request(url)
    
    def get_beststories(self):
        url = f"{self.__class__.base_url}/beststories/.json"
        return self._request(url)
    
    def get_newstories(self):
        url = f"{self.__class__.base_url}/newstories/.json"
        return self._request(url)
    
    def get_maxitem(self):
        url = f"{self.__class__.base_url}/maxitem/.json"
        #datetime.fromtimestamp(user['created'])
        return self._request(url)

