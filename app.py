import tkinter as tk
import requests
import sqlite3
from datetime import datetime
from tkinter import ttk

root = tk.Tk()
root.title("Запрос вывода API ")


style = ttk.Style(root)
style.theme_use("clam")
style.configure('Treeview', background='#D3D3D3', foreground='black', fieldbackground='#D3D3D3')
style.configure('Treeview.Heading', background='#B0C3D9', foreground='black')
style.map('Treeview', background=[('selected', '#347083')])


tree = ttk.Treeview(root, columns=('IP адрес', 'Дата запроса'), show='headings')
tree.heading('#1', text='IP ')
tree.heading('#2', text='Дата ')
tree.column('#1', width=200)
tree.column('#2', width=200)
tree.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

def insert_data():
    response = requests.get('http://51.250.91.193:5000/logs?')
    data = response.json()


    with sqlite3.connect('requests.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS requests (ip_address TEXT, request_time TEXT)')


        for item in data:
            ip_address = item.get('ip_address', '')
            request_time = item.get('request_time', '')
            request_time = datetime.strptime(request_time, '%d/%b/%Y:%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('INSERT INTO requests VALUES (?, ?)', (ip_address, request_time))


    populate_table()

def time():
    with sqlite3.connect('requests.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM requests ORDER BY request_time DESC')
        rows = cursor.fetchall()


        for record in tree.get_children():
            tree.delete(record)
        for row in rows:
            tree.insert('', tk.END, values=row)

def populate_table(reverse=False):
    with sqlite3.connect('requests.db') as conn:
        cursor = conn.cursor()
        if reverse:
            cursor.execute('SELECT * FROM requests ORDER BY request_time DESC')
        else:
            cursor.execute('SELECT * FROM requests')
        rows = cursor.fetchall()


        for record in tree.get_children():
            tree.delete(record)
        for row in rows:
            tree.insert('', tk.END, values=row)


time_button = tk.Button(root, text="Сортировать ", command=time, bg='#347083', fg='white')
time_button.grid(row=2, column=0, padx=5, pady=5, sticky='W')


insert_button = tk.Button(root, text="данные", command=insert_data, bg='#347083', fg='white')
insert_button.grid(row=1, column=0, padx=5, pady=5, sticky='W')


update_button = tk.Button(root, text="Обновить данные", command=populate_table, bg='#347083', fg='white')
update_button.grid(row=3, column=0, padx=5, pady=5, sticky='W')

root.mainloop()


