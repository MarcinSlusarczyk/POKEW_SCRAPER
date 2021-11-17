import time
import os
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



gmail_address = pg.prompt(text='wpisz swoj email na który ma przyjść powiadomienie')
password = pg.password('wpisz hasło do swojego konta google', mask='*')


if gmail_address == "" and password == "":
    pg.alert('BRAK INFORMACJI! - URUCHOM PROGRAM OD NOWA I UZUPEŁNIJ ODPOWIEDNIO WSZYSTKIE POLA', 'UZUPEŁNIJ INFORMACJE!')
    sys.exit()

begin_time = datetime.datetime.now()
product_name = ""
counter_loop = 0
counter_max = 0
wartosc = 0
zmiana = 0
tablica = []
tablica_start = []
product_table = []
link_table = []
product_table_start = []
link_table_start = []

def send_email(current_price, previous_price, current_product, current_link):

    subject = f'BOT ALERT (PokeWave.eu) - {current_product}'
    
    msg = MIMEMultipart()
    msg['From'] = gmail_address
    msg['To'] = gmail_address
    msg['Subject'] = subject

    body = f'Cena spadła z {previous_price} zł na {current_price} !!!! -- link do produktu: {current_link}'
    msg.attach(MIMEText(body, 'plain'))

    part = MIMEBase('application', 'octet-stream')

    text = msg.as_string()


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_address, password)
    server.sendmail(gmail_address, gmail_address, text)
    server.quit()

def send_email_alert(count_tablica):
    
    subject = f'PROGRAM 2 - WSZYSTKO DZIAŁA! (BOT ALERT)'
    
    msg = MIMEMultipart()
    msg['From'] = gmail_address
    msg['To'] = gmail_address
    msg['Subject'] = subject

    body = f'Dostępnych produktów na stronie jest: {count_tablica}'
    msg.attach(MIMEText(body, 'plain'))

    part = MIMEBase('application', 'octet-stream')

    text = msg.as_string()


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_address, password)
    server.sendmail(gmail_address, gmail_address, text)
    server.quit()
    

def send_email_alert_new(link):
    
    subject = f'POJAWIŁ SIĘ NOWY PRODUKT! (BOT ALERT)'
    
    msg = MIMEMultipart()
    msg['From'] = gmail_address
    msg['To'] = gmail_address
    msg['Subject'] = subject

    body = f'link no nowego produktu: {link}'
    msg.attach(MIMEText(body, 'plain'))

    part = MIMEBase('application', 'octet-stream')

    text = msg.as_string()


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_address, password)
    server.sendmail(gmail_address, gmail_address, text)
    server.quit()

def petla():
    
    counter_loop = 0
    counter_max = 0
    tablica = []
    tablica_start = []
    product_table = []
    link_table = []
    product_table_start = []
    link_table_start = []
    status_loop = True
  
    
    while status_loop:
        
        godzina = time.localtime()
        aktualna = time.strftime("%H:%M:%S", godzina)
        if aktualna > '08:00:00' and aktualna < '08:00:10':
            send_email_alert(count_tablica)
            time.sleep(11)
        if aktualna > '20:00:00' and aktualna < '20:00:10':            
            send_email_alert(count_tablica)
            time.sleep(11)
        
        counter_loop +=1
        counter = 0
        main_site = 'https://pokewave.eu/produkty.html'    
        
        try:
            page = requests.get(main_site)
            soup = BeautifulSoup(page.content, "html.parser")
            index_page = soup.find(class_='IndexStron')
            page_count = index_page.text[16].replace(' ', '')
        except:
            page_count = 6
        
        seq = 1

        for seq in range(int(page_count)):
            
            try:

                page = (f'{main_site}/s={str(int(seq+1))}')
                page_request = requests.get(page)
                soup = BeautifulSoup(page_request.content, "html.parser")

                
                for index, order in enumerate(soup.find_all(class_='Okno OknoRwd')):
                    
                    product_name = order.find('h3').text
                    product_link = order.find('a')['href']
                    product_status = order.find(class_='ListaOpisowa').text
                    product_cart = order.find(class_='DoKoszyka')
                    
                    try:                        
                        product_price = order.find('span', class_='CenaPromocyjna').text                            
                    except:
                        product_price = 0
                                        
                    try:                       
                        price = order.find(class_='Cena').text
                    except:
                        price = 0
                        
                    if product_status.find('Dostępny') > 0  and product_cart != None:
                        
                        if price == 0:                               
                            product_price_2 = int(float(product_price.replace(' ', '').replace(',', '.').split('zł')[1]))
                        else:
                            product_price_2 =int(float(price.replace(' ', '').replace(',', '.').split('zł')[0]))
                        
                        
                            
                        tablica.append(product_price_2)
                        product_table.append(product_name)
                        link_table.append(product_link)
                        
                        
                        
                        if counter_loop == 1:
                            tablica_start.append(product_price_2)                                            
                            product_table_start.append(product_name)
                            link_table_start.append(product_link)
                    
            except:
                print('Wystąpił problem z połączeniem...')
                time.sleep(5)
                status_loop = False
                petla()
            # except requests.exceptions.HTTPError as errh:
            #     print ("Http Error:",errh)
            #     counter = counter_max
            #     time.sleep(5)
            # except requests.exceptions.ConnectionError as errc:
            #     print ("Error Connecting:",errc)
            #     counter = counter_max
            #     time.sleep(5)
                
            # except requests.exceptions.Timeout as errt:
            #     print ("Timeout Error:",errt)
            #     counter = counter_max
            #     time.sleep(5)
                
            # except requests.exceptions.RequestException as err:
            #     print ("OOps: Something Else",err)
            #     counter = counter_max
            #     time.sleep(5)
                       
        
        counter_max = counter

        
        count_tablica = len(tablica)       
        count_tablica_start = len(tablica_start)
        
        if count_tablica_start  > 0: 
            if count_tablica > count_tablica_start:
                for link in link_table:
                    if link not in link_table_start:
                        print(f"wysyłam powiadomienie dla nowego produktu, link: {link}")
                        send_email_alert_new(link)
                        status_loop = False
                        petla()
        
        if count_tablica < count_tablica_start:
            print(count_tablica, count_tablica_start)
            print(f'Ilość dostępnych produktów zmniejszyła się z {count_tablica_start} na {count_tablica} !')
            status_loop = False
            petla()
            
        
        
                   
        
        for wartosc in range(count_tablica_start):
    
            try:
                current_price = tablica[wartosc]
                current_product = product_table[wartosc]
                current_link = link_table[wartosc]
                previous_price = tablica_start[wartosc]

                if current_price > previous_price:
                    counter += 1            
                    if counter > counter_max:
                        send_email(current_price, previous_price, current_product, current_link)
            except IndexError:
                pass
                # print("restart programu")
                # status_loop = False
                # petla()
                # os.execl(sys.executable, sys.executable, *sys.argv)
            
                            
        counter_max = counter
        czas = datetime.datetime.now() - begin_time
        print(f'działa już: {czas} -- ilość dostępnych produktów: {count_tablica} --- godzina: {aktualna}')
        time.sleep(1)
        tablica.clear()
        product_table.clear()
        link_table.clear()

petla()