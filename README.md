# iwillplay
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

iwillplay.ru web scraping module

![license](https://img.shields.io/github/license/szy13/py_iwillplay)
[![telegram](https://img.shields.io/badge/telegram-szyxiii-blue)](https://t.me/szyxiii)

## Requirements
* [requests](https://pypi.org/project/requests/) - http(s) library
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) - web scraping library


## Installation
Legacy setup
```
$ python3 setup.py install
```
Pip
```
No pip installation for now
```

## Usage
Search for a game

```python
from iwillplay import IWillPlay

iwp = IWillPlay()
results = iwp.search('gta v')

for result in results:
    print(result)
```

Get game info by url-like name

```python
from iwillplay import IWillPlay

iwp = IWillPlay()
game = iwp.get_game('battlefield-1')

print('Title:', game.title)
print(game.properties)
```
