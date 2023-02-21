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
    
    def _makeurl(endpoint, type_='json'):
        return f"{self.__class__.base_url}/{endpoint}.{type_}"

    def get_item(self, item_id):
        """
        item['descendants'] refers to the number of comments, if the item is story.
        item['score'] is exactly the points shown in hckrnews.com
        """
        url = f"{self.__class__.base_url}/item/{item_id}.json"
        item = self._request(url)

        # Add a string represented time to the dict
        if item.get('time'):
            item['time_str'] = str(datetime.datetime.utcfromtimestamp(item['time']))
        return item

    def get_topstories(self):
        url = f"{self.__class__.base_url}/topstories/.json"
        return self._request(url)
    
    def get_beststories(self):
        """It returns the id of the best stories.
        """

        url = f"{self.__class__.base_url}/beststories/.json"
        return self._request(url)
    
    def get_newstories(self):
        url = f"{self.__class__.base_url}/newstories/.json"
        return self._request(url)
    
    def get_maxitem(self):
        url = f"{self.__class__.base_url}/maxitem/.json"
        return self._request(url)
