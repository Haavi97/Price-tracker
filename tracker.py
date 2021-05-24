import requests
import smtplib
from bs4 import BeautifulSoup

from personal_data import sender, receiver, pswd

URL = 'https://www.amazon.es/AZDelivery-Canales-optoacoplador-Low-Level-Trigger-Arduino/dp/B07N2Z1DWG/ref=sr_1_1?__mk_es_ES=ÅMÅŽÕÑ&dchild=1&keywords=relay%2Bboard&qid=1612681652&sr=8-1&th=1'

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123'}

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

price = soup.find(id='priceblock_ourprice').get_text()
price_contverted = float(price[:-2].replace(',','.'))

print(price_contverted)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()

server.login(sender, pswd)

subject = 'Board price {} (from python script)'.format(price_contverted)

body = 'Check it out: {}'.format(URL)

msg = 'Subject:{}\n\n{}'.format(subject, body)
msg = msg.encode('ascii', 'ignore')

print('Sending from:\t{} \nto:\t\t{}\n\n'.format(sender, receiver))

server.sendmail(sender, receiver, msg)

print('Message sent:\n\n{}\n\n'.format(msg))

server.quit()
