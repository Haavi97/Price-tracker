import os
import os.path
import requests
from bs4 import BeautifulSoup
from datetime import date

from tracker import send_email, headers

bitcoin_URL = 'https://www.google.com/search?client=opera&q=bitcoin+price&sourceid=opera&ie=UTF-8&oe=UTF-8'

ethereum_URL = 'https://www.google.com/search?client=opera&q=ethereum+price&sourceid=opera&ie=UTF-8&oe=UTF-8'

dollar_URL = 'https://www.google.com/search?client=opera&q=dollar+price&sourceid=opera&ie=UTF-8&oe=UTF-8'


def coin_tracker(url):
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    div = soup.find(id='knowledge-currency__updatable-data-column')
    return ''.join(
        (list(filter(lambda x: x.isnumeric() or x == ',' or x == '.',
                     next(next(next(div.children).children).next_sibling.children).get_text()))))


def create_folder(folder_name):
    '''Function to create a folder in case it does not exists'''
    try:
        os.mkdir(folder_name)
        #print('Created folder. Abs path: {}.'.format(os.path.abspath(folder_name)))
    except FileExistsError:
        #print('Folder already existed')
        pass

def add_entry(path, entry):
    with open(path, 'a+') as f:
        f.write(entry + '\n')

def register_bitcoin_day():
    # TODO! Check if already registered
    path = 'data' + os.sep + 'bitcoinprices.tsv'
    create_folder('data')
    price = coin_tracker(bitcoin_URL)
    print('Bitcoin price in euros: {:,}'.format(
        float(price.replace(',', '.'))).replace(',', ' '))
    entry = str(date.today()) + '\t' + price
    add_entry(path, entry)


if __name__ == '__main__':
    today = date.today()
    register_bitcoin_day()
    price = coin_tracker(ethereum_URL)
    print('Ethereum price in euros: {:,}'.format(
        float(price.replace(',', '.'))).replace(',', ' '))
    price = coin_tracker(dollar_URL)
    print('Dollar price in euros: {:,}'.format(
        float(price.replace(',', '.'))).replace(',', ' '))
    create_folder('data')
