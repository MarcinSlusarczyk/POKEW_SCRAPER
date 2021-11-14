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
tablica = []
tablica_start = []
product_table = []
link_table = []

def send_email():

    subject = f'BOT ALERT (PokeWave.eu) - {product_name}'
    
    msg = MIMEMultipart()
    msg['From'] = gmail_address
    msg['To'] = gmail_address
    msg['Subject'] = subject

    body = f'Cena spadła z {tablica_start[wartosc]} zł na {tablica[wartosc]} !!!! -- link do produktu: {link_table[wartosc]}'
    msg.attach(MIMEText(body, 'plain'))

    part = MIMEBase('application', 'octet-stream')

    text = msg.as_string()


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_address, password)
    server.sendmail(gmail_address, gmail_address, text)
    server.quit()

def send_email_alert():
    
    subject = f'PROGRAM 2 - WSZYSTKO DZIAŁA! (BOT ALERT)'
    
    msg = MIMEMultipart()
    msg['From'] = gmail_address
    msg['To'] = gmail_address
    msg['Subject'] = subject

    body = f'Wiadomość wygenerowana automatycznie...'
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


    status_loop = True

    while status_loop:
        godzina = time.localtime()
        aktualna = time.strftime("%H:%M:%S", godzina)
        if aktualna > '08:00:00' and aktualna < '08:00:10':
            send_email_alert()
            time.sleep(11)
        if aktualna > '20:00:00' and aktualna < '20:00:10':            
            send_email_alert()
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
                    try:
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
                        
                    except:                        
                        pass
                    
            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
                counter = counter_max
                time.sleep(5)
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
                counter = counter_max
                time.sleep(5)
                
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
                counter = counter_max
                time.sleep(5)
                
            except requests.exceptions.RequestException as err:
                print ("OOps: Something Else",err)
                counter = counter_max
                time.sleep(5)
                       
        
        counter_max = counter

        
        count_tablica = len(tablica)
         
        
        for wartosc in range(count_tablica):
            try:
                # print(f'{tablica[wartosc]}, {tablica_start[wartosc]}')
                if tablica[wartosc] > tablica_start[wartosc]:
                    counter += 1            
                    if counter > counter_max:
                        send_email()
            except IndexError:
                print("restart programu")
                status_loop = False
                petla()
                # os.execl(sys.executable, sys.executable, *sys.argv)
            
                            
        counter_max = counter
        czas = datetime.datetime.now() - begin_time
        print(f'działa już: {czas} -- wysłano: {counter_max} powiadomień -- ilość produktów: {count_tablica} -- godzina: {aktualna}')
        time.sleep(1)
        tablica.clear()
        product_table.clear()
        link_table.clear()

petla()
