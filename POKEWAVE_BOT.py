import time
import datetime
import requests
from bs4 import BeautifulSoup
from pushbullet import Pushbullet
import schedule


token = 'yourtoken'
pb = Pushbullet(token)


begin_time = datetime.datetime.now()
product_name = ""
tablica = []
product_table = []
link_table = []


def send_email(current_price, previous_price, current_product, current_link):
    try:
        subject = f'BOT ALERT (PokeWave.eu) - {current_product}'     
        body = f'Cena spadła z {previous_price} zł na {current_price} !!!! -- link do produktu: {current_link}'
        pb.push_link(subject, body)
    
    except:
        print('błąd wysyłania')
        
def send_email_alert(count_tablica):
    try:
        subject = f'BOT POKEWAVE - WSZYSTKO DZIAŁA!'            
        body = f'Dostępnych produktów na stronie jest: {count_tablica}'
        pb.push_note(subject, body)
    except:
        print('błąd wysyłania')

def send_email_alert_new(product_link, product_name, product_price_2):
    try:
        subject = f'POJAWIŁ SIĘ NOWY PRODUKT! - {product_name} -- cena: {product_price_2}'       
        body = product_link
        pb.push_link(subject, body)
    except:
        print('błąd wysyłania')
            
tablica = {}
tablica_check = {}
product_table = []
link_table = []


def main():
    godzina = time.localtime()
    aktualna = time.strftime("%H:%M:%S", godzina)
    if aktualna > '08:00:00' and aktualna < '08:00:30':
        send_email_alert(count_tablica)
        time.sleep(30)
    if aktualna > '20:00:00' and aktualna < '20:00:30':            
        send_email_alert(count_tablica)
        time.sleep(30)
    if aktualna > '16:00:00' and aktualna < '16:00:30':            
        send_email_alert(count_tablica)
        time.sleep(30)
    if aktualna > '18:00:00' and aktualna < '18:00:30':            
        send_email_alert(count_tablica)
        time.sleep(30)
    if aktualna > '22:00:00' and aktualna < '22:00:30':            
        send_email_alert(count_tablica)
        time.sleep(30)
    
 
   
    main_site = 'https://pokewave.eu/produkty.html'    
    
    try:
        page = requests.get(main_site)
        soup = BeautifulSoup(page.content, "html.parser")
        index_page = soup.find(class_='IndexStron')
        page_count = index_page.text[16].replace(' ', '')
    except:
        page_count = 6
    
    seq = 1
    try:
        for seq in range(int(page_count)):
            
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
                        
                        tablica_check[product_link] = product_name, product_price_2                      
                                    
                        if product_link not in tablica:
                            tablica[product_link]= product_name, product_price_2
                            print(f'Wysyłam powiadomienie dla - {product_link}')
                            send_email_alert_new(product_link, product_name, product_price_2) 
                                    
        
        if tablica_check != tablica:
            try:
                for key in tablica:
                    if key not in tablica_check:
                        tablica.pop(key, None)
            except RuntimeError:
                pass
    
    except:
        print(f'Wystąpił problem z połączeniem...')
        time.sleep(5)
            
    count_tablica = len(tablica)                                   
    czas = datetime.datetime.now() - begin_time
    print(f'działa już: {czas} -- ilość dostępnych produktów: {len(tablica)} --- godzina: {aktualna}')
    tablica_check.clear()


schedule.every(10).seconds.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
