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

gmail_address = pg.prompt(text='wpisz swoj email na który ma przyjść powiadomienie')
password = pg.password('wpisz hasło do swojego konta google', mask='*')

if gmail_address == "" or password == "":
    pg.alert('UZUPEŁNIJ DANE I URUCHOM PONOWNIE PROGRAM', 'BRAK DANYCH')
    sys.exit()

def send_email(Linki):
    
    subject = f'BOT ALERT - PRODUKT DOSTĘPNY! - link: {Linki}'

    msg = MIMEMultipart()
    msg['From'] = gmail_address
    msg['To'] = gmail_address
    msg['Subject'] = subject

    body = f'link do produktu: {Linki}'
    msg.attach(MIMEText(body, 'plain'))

    part = MIMEBase('application', 'octet-stream')

    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_address, password)


    server.sendmail(gmail_address, gmail_address, text)
    server.quit()


def pobieranie():
    
    counter_max = 0
    
    while True:
        counter = 0
        for Linki in list(tasks):
            
                
            page = requests.get(Linki)
            
            soup = BeautifulSoup(page.content, "html.parser")

            koszyk = soup.find_all('div', id='PrzyciskKupowania')
            
            for ele in koszyk:
                try:
                    ele['style']

                    if 'display:none' in ele['style']:
                        print (f'Produkt niedostępny - {Linki}')
                except:
                    counter += 1
                    if counter > counter_max:
                        print(f"Produkt jest dostępny!! - {Linki}")
                        send_email(Linki)
        counter_max = counter                  
        time.sleep(5)



root = tkinter.Tk()

root.configure(bg='lightyellow')

root.title('pokewave.eu - order status')

root.geometry('400x250')

tasks = []

# Create functions

def update_listbox():
    # Clear the current list
    clear_listbox()

    #update items to list
    for task in tasks:
        lb_tasks.insert("end", task)

def clear_listbox():
    lb_tasks.delete(0,"end")


def add_task():
    # Get the task
    task = txt_input.get()
    # Append the task to list
    if task != '':
        tasks.append(task)
        update_listbox()
    else:
        display['text'] = "Please enter a link!"
    txt_input.delete(0,'end')


def delete():
    task = lb_tasks.get('active')
    if task in tasks:
        tasks.remove(task)
    # Update list box
    update_listbox()

    display['text'] = "link deleted!"

def delete_all():
    global tasks
    # Clear the list
    tasks = []

    update_listbox()

def choose_random():
    task = random.choice(tasks)
    display['text'] = task

def number_of_task():
    number_of_tasks = len(tasks)

    msg = "Number of links : %s" %number_of_tasks
    display['text'] = msg

def exit():
    quit()
    

#Create Buttons and List options

title = tkinter.Label(root, text = "INPUT LINK AND DOWNLOAD STATUS ORDERS", bg='lightyellow')
title.grid(row=0,column=1)


display = tkinter.Label(root, text = "", bg='white')
display.grid(row=1,column=1)


txt_input = tkinter.Entry(root, width=30)
txt_input.grid(row=1,column=1)


btn_add_task = tkinter.Button(root, text = "Add link", fg = 'black', bg = None, command = add_task)

btn_add_task.grid(row=1,column=0)

btn_delete = tkinter.Button(root, text = "Delete", fg = 'black', bg = None, command = delete)

btn_delete.grid(row=2,column=0)


btn_delete_all = tkinter.Button(root, text = "Delete All", fg = 'black', bg = None, command = delete_all)

btn_delete_all.grid(row=3,column=0)


btn_choose_random = tkinter.Button(root, text = "Choose Random", fg = 'black', bg = None, command = choose_random)

btn_choose_random.grid(row=4,column=0)


btn_number_of_task = tkinter.Button(root, text = "Number of links", fg = 'black', bg = None, command = number_of_task)

btn_number_of_task.grid(row=5,column=0)


btn_close = tkinter.Button(root, text = "Exit", fg = 'black', bg = None, command = exit)

btn_close.grid(row=6,column=0)


btn_start = tkinter.Button(root, text = "START PROGRAM!", fg = 'black', bg = None, command = pobieranie)

btn_start.grid(row=12,column=1)


lb_tasks = tkinter.Listbox(root)
lb_tasks.grid(row=2,column=1,rowspan=10)



root.mainloop()
