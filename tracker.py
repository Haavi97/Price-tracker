import requests
import smtplib
from bs4 import BeautifulSoup
from time import sleep

from personal_data import sender, receiver, pswd


def amazon_product(url):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123'}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    price = soup.find(id='priceblock_ourprice').get_text()
    price_converted = float(price[:-2].replace(',', '.'))

    print('The price of your amazon product: {} €'.format(price_converted))

    return price_converted


def send_email(subject, body, email_to=receiver):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(sender, pswd)

    msg = 'Subject:{}\n\n{}'.format(subject, body)
    msg = msg.encode('ascii', 'ignore')

    print('Sending from:\t{} \nto:\t\t{}\n\n'.format(sender, receiver))

    server.sendmail(sender, receiver, msg)

    print('Message sent:\n\n' + str(msg.decode('ascii'))+'\n\n')

    server.quit()


def check_every(func, interval, *args):
    MAX = 10**10
    current = 0
    while current < MAX:
        func(*args)
        sleep(interval)
        current += 1



if __name__ == '__main__':

    URL = 'https://www.amazon.es/AZDelivery-Canales-optoacoplador-Low-Level-Trigger-Arduino/dp/B07N2Z1DWG/ref=sr_1_1?__mk_es_ES=ÅMÅŽÕÑ&dchild=1&keywords=relay%2Bboard&qid=1612681652&sr=8-1&th=1'

    price = amazon_product(URL)

    subject = 'The amazon product you are tracking costs {}€ now'.format(
        price)
    body = ('Hey, there!' + \
        'The amazon product you are tracking costs {}€ now' +\
        'Check it out here: {}').format(price, URL)

    check_every(send_email, 60, subject, body)
