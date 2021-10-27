import time
import sys
import datetime
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
import socket
socket.getaddrinfo('localhost', 8080)

gmail_address = pg.prompt(text='wpisz swoj email na który ma przyjść powiadomienie')
password = pg.password('wpisz hasło do swojego konta google', mask='*')
your_sale_price_level = pg.prompt('wpisz wysokość promocji produktu (w PLN)')

if gmail_address == "" and password == "" and your_sale_price_level == "":
    pg.alert('BRAK INFORMACJI! - URUCHOM PROGRAM OD NOWA I UZUPEŁNIJ ODPOWIEDNIO WSZYSTKIE POLA', 'UZUPEŁNIJ INFORMACJE!')
    sys.exit()

begin_time = datetime.datetime.now()

def send_email():

    subject = f'BOT ALERT (PokeWave.eu) - {product_name}'
    
    msg = MIMEMultipart()
    msg['From'] = gmail_address
    msg['To'] = gmail_address
    msg['Subject'] = subject

    body = f'PROMOCJA o {product_previous_price-product_price} zł !!!! -- link do produktu: {product_link}'
    msg.attach(MIMEText(body, 'plain'))

    part = MIMEBase('application', 'octet-stream')

    text = msg.as_string()


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_address, password)
    server.sendmail(gmail_address, gmail_address, text)
    server.quit()

counter_max = 0
sale_max = 0

while True:
    counter = 0
    main_site = 'https://pokewave.eu/produkty.html'    
    #page = requests.get(main_site)
    #soup = BeautifulSoup(page.content, "html.parser")
    #index_page = soup.find(class_='IndexStron')
    page_count = 10 #index_page.text[16].replace(' ', '')

    seq = 1

    for seq in range(int(page_count)):
        
        try:

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
                    sale = product_previous_price-product_price

                    if sale > int(your_sale_price_level):
                        counter += 1
                        if counter > counter_max:                      
                            print(f'Wysyłam powiadomienie: Promocja o: {sale} zł --- {product_name} --- product link: {product_link}')
                            send_email()
                            
                    
            
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
            counter = counter_max
            print(counter)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
            counter = counter_max
            print(counter)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
            counter = counter_max
            print(counter)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
            counter = counter_max
            print(counter)
    
    
    time.sleep(1)
    counter_max = counter    
    czas = datetime.datetime.now() - begin_time
    print(f'program pracuje już: {czas} ---- łącznie wysłano: {counter_max} powiadomień')
        
