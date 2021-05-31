import requests
from bs4 import BeautifulSoup

from tracker import send_email, headers

bitcoin_URL = 'https://www.google.com/search?client=opera&q=bitcoin+price&sourceid=opera&ie=UTF-8&oe=UTF-8'

ethereum_URL = 'https://www.google.com/search?client=opera&q=ethereum+price&sourceid=opera&ie=UTF-8&oe=UTF-8'

dollar_URL = 'https://www.google.com/search?client=opera&q=dollar+price&sourceid=opera&ie=UTF-8&oe=UTF-8'

def coin_tracker(url):
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    div = soup.find(id='knowledge-currency__updatable-data-column')
    return ''.join((list(filter(lambda x: x.isnumeric() or  x == ',' or x == '.', next(next(next(div.children).children).next_sibling.children).get_text()))))

if __name__ == '__main__':
    price = coin_tracker(bitcoin_URL)
    print('Bitcoin price in euros: {:,}'.format(float(price.replace(',', '.'))).replace(',', ' '))
    price = coin_tracker(ethereum_URL)
    print('Ethereum price in euros: {:,}'.format(float(price.replace(',', '.'))).replace(',', ' '))
    price = coin_tracker(dollar_URL)
    print('Dollar price in euros: {:,}'.format(float(price.replace(',', '.'))).replace(',', ' '))

