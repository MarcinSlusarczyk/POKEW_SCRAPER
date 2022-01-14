import time
import datetime
import requests
from bs4 import BeautifulSoup
from pushbullet import Pushbullet


print('uruchamiam program...')

token = 'o.qOgEBkxanJbLbKPAvKs2BZUa2TZAcSoM'
pb = Pushbullet(token)


begin_time = datetime.datetime.now()
product_name = ""
counter_loop = 0
counter_max = 0
tablica = []
tablica_start = []
product_table = []
link_table = []
product_table_start = []
link_table_start = []

def send_email(current_price, previous_price, current_product, current_link):
    try:
        subject = f'BOT ALERT (PokeWave.eu) - {current_product}'     
        body = f'Cena spadła z {previous_price} zł na {current_price} !!!! -- link do produktu: {current_link}'
        pb.push_link(subject, body)
    
    except:
        print('błąd wysyłania')
        
def send_email_alert(count_tablica):
    try:
        subject = f'PROGRAM 2 - WSZYSTKO DZIAŁA! (BOT ALERT)'            
        body = f'Dostępnych produktów na stronie jest: {count_tablica}'
        pb.push_link(subject, body)
    except:
        print('błąd wysyłania')

def send_email_alert_new(product_link, product_name, product_price_2):
    try:
        subject = f'POJAWIŁ SIĘ NOWY PRODUKT! - {product_name} -- cena: {product_price_2}'       
        body = product_link
        pb.push_link(subject, body)
    except:
        print('błąd wysyłania')
            
counter_loop = 0
counter_max = 0
tablica = {}
tablica_check = {}
product_table = []
link_table = []
product_table_start = []
link_table_start = []
status_loop = True


while status_loop:
    
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
                    
                    tablica_check[product_link] = product_name, product_price_2                      
                                  
                    if product_link not in tablica:
                        tablica[product_link]= product_name, product_price_2
                        print(f'Wysyłam powiadomienie dla - {product_link}')
                        send_email_alert_new(product_link, product_name, product_price_2) 
                    
                                          
                                                                           
        except Exception as Err:
            print(f'Wystąpił problem z połączeniem... powód: {Err}')
            time.sleep(5)
    
    if tablica_check != tablica:
        try:
            for key in tablica:
                if key not in tablica_check:
                    tablica.pop(key, None)
        except RuntimeError:
            pass
        
    count_tablica = len(tablica)                                   
    counter_max = counter
    czas = datetime.datetime.now() - begin_time
    print(f'działa już: {czas} -- ilość dostępnych produktów: {len(tablica)} --- godzina: {aktualna}')
    tablica_check.clear()
    time.sleep(6)
