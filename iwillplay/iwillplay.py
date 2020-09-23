import re
import requests
from urllib.parse import urlencode

from bs4 import BeautifulSoup


BASE_URL = 'https://iwillplay.ru'
SEARCH_URL = BASE_URL + '/search?'
GAME_URL = BASE_URL + '/game/'


class IWillPlay:
    """IWillPlay class provides interaction with IWillPlay service"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) '
            'Gecko/20100101 Firefox/79.0'
        })

    def search(self, text):
        """Search a game

        :param text: query text for search
        :type text: str

        :return: list of found games
        :rtype: list
        """
        results = []

        query_url = SEARCH_URL + urlencode({'q': text})
        response = requests.get(query_url)

        for match in re.finditer(r"location\.href='(.+?)'", response.text):
            name = match.group(1).replace('/game/', '')
            results.append(self.get_game(name))

        return results

    def get_game(self, name):
        """Get the game data

        :param name: iwillplay-formatted game name
        :type name: str

        :return: IWPGame object contains game data
        :rtype: IWPGame
        """
        url = GAME_URL + name

        response = requests.get(url)
        bs = BeautifulSoup(response.text, 'html.parser')

        title = self._get_title(bs)
        picture_url = self._get_picture_url(bs)
        properties = self._get_properties(bs)
        offers = self._get_offers(bs)

        return IWPGame(title, url, picture_url, properties, offers)

    def _get_title(self, bs):
        """Parse game title using bs4

        :param bs: BeautifulSoup object to use
        :type bs: BeautifulSoup

        :return: title text
        :rtype: str
        """
        return bs.find('h1', {'itemprop': 'name'}).text

    def _get_picture_url(self, bs):
        """Parse game picture url using bs4

        :param bs: BeautifulSoup object to use
        :type bs: BeautifulSoup

        :return: picutre url text
        :rtype: str
        """
        return BASE_URL + bs.find('div', {'class': 'image'}).find('img').get('src')

    def _get_properties(self, bs):
        """Parse game properties using bs4

        :param bs: BeautifulSoup object to use
        :type bs: BeautifulSoup

        :return: properties dictionary
        :rtype: dict
        """
        properties = {}

        container = bs.find('div', {'class': 'properties container'}).find_all('tr')
        for prop in container:
            name, value = (td.text.strip() for td in prop.find_all('td'))
            properties[name] = [p[0].upper() + p[1:] for p in value.split(', ')]

        return properties

    def _get_offers(self, bs):
        """Parse game offers using bs4

        :param bs: BeautifulSoup object to use
        :type bs: BeautifulSoup

        :return: offers list
        :rtype: IWPOffer list
        """
        offers = []

        table = bs.find('div', {'class': 'stores-offers-list'}).find('table')
        table.find('thead').extract()
        for tr in table.find_all('tr', {'class': ''}):
            td = tr.find_all('td')

            name = td[0].text.strip()
            price = int(td[1].text.strip().split(' ')[0])
            link = td[2].find('a').get('href')

            offers.append(IWPOffer(name, price, link))

        return offers


class IWPGame:
    """IWPGame class represents IWillPlay game object and containing game info

    :prop title: game title
    :type title: str

    :prop url: iwillplay game url
    :type url: str

    :prop picture_url: game picture url
    :type picture_url: str

    :prop properties: game properties dictionary
    :type properties: dict

    :prop offers: game offers list
    :type offers: list
    """

    def __init__(self, title, url, picture_url, properties=None, offers=None):
        self.title = title
        self.url = url
        self.picture_url = picture_url
        self.properties = properties or {}
        self.offers = offers or []

    def __repr__(self):
        return '<{}:{}> {}'.format(self.__class__.__name__, self.title, self.url)

    def __str__(self):
        return self.title


class IWPOffer:
    """IWPOffer class represents IWillPlay game offer and containing offer info

    :prop name: store name
    :type name: str

    :prop price: store game price in rub.
    :type price: int

    :prop url: store game url
    :type url: str
    """

    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url

    def __repr__(self):
        return '<{}:{}> {}'.format(self.__class__.__name__, self.title, self.url)

    __str__ = __repr__
