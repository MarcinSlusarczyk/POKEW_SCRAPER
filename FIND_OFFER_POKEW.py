import time
import sys
import tkinter
import random
import requests
from bs4 import BeautifulSoup
import pymsgbox as pg
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

gmail_address = pg.prompt(text='wpisz swoj email')
password = pg.password('wpisz hasło do swojego konta', mask='*')
your_sale_price_level = pg.prompt('wpisz wysokość promocji produktu')

def send_email():

    subject = f'BOT ALERT z PokeWave.eu! - {product_name}'

    msg = MIMEMultipart()
    msg['From'] = gmail_address
    msg['To'] = gmail_address
    msg['Subject'] = subject

    body = f'link do produktu: {product_link}'
    msg.attach(MIMEText(body,'plain'))

    part = MIMEBase('application','octet-stream')

    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(gmail_address, password)


    server.sendmail(gmail_address,gmail_address,text)
    server.quit()


counter_max = 0

while True:
    counter = 0
    main_site = 'https://pokewave.eu/produkty.html'    
    page = requests.get(main_site)
    soup = BeautifulSoup(page.content, "html.parser")
    index_page = soup.find(class_='IndexStron')
    page_count = index_page.text[16].replace(' ', '')

    seq = 1

    for seq in range(int(page_count)):
        page = (f'{main_site}/s={str(int(seq+1))}')
        page_request = requests.get(page)
        soup = BeautifulSoup(page_request.content, "html.parser")

        
        for order in soup.find_all(class_='Okno OknoRwd'):
            
            product_name = order.find('h3').text
            product_link = order.find('a')['href']
            product_status = order.find(class_='ListaOpisowa').text
            product_cart = order.find(class_='DoKoszyka')
            product_previous_price = order.find('em', class_='CenaPoprzednia')
            product_price = order.find('span', class_='CenaPromocyjna')

            if product_status.find('Dostępny') > 0 and product_previous_price != None and product_cart != None:
                
                product_previous_price = int(float(product_price.text.replace('zł', '').replace(',', '.').split()[0]))
                product_price = int(float(product_price.text.replace('zł', '').replace(',', '.').split()[1]))

                if product_previous_price-product_price > int(your_sale_price_level):
                    counter += 1
                    if counter > counter_max:
                        print(f'SALE LEVEL is: {product_previous_price-product_price} --- {product_name} --- product link: {product_link}')
                        send_email()
    time.sleep(1)
    counter_max = counter