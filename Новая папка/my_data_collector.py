import requests
import sqlite3
import threading
import time

def thread_func(requested_url,num):
    url_payload = {
        "requested_url": requested_url
    }
    port = 8000 + num
    result = requests.post(f"http://127.0.0.1:{port}/my_unique_api", json=url_payload).json()
    # print(result)
    # print("\n\n\n\n\n\n")
    global full_result
    full_result.update(result)

url_list = ["https://en.wikipedia.org/wiki/Henry_Kissinger","https://en.wikipedia.org/wiki/East_African_Community","https://en.wikipedia.org/wiki/Democratic_Republic_of_the_Congo"]
global full_result
full_result = {}
url = url_list.pop(0)
second_thread = threading.Thread(target=thread_func,args=(url, 1))
second_thread.start()
url = url_list.pop(0)
first_thread = threading.Thread(target=thread_func,args=(url, 0))
first_thread.start()
while len(url_list) != 0:
    time.sleep(2)
    if first_thread.is_alive() == False:
        url = url_list.pop(0)
        first_thread = threading.Thread(target=thread_func,args=(url, 0))
    if second_thread.is_alive() == False and len(url_list) != 0:
        url = url_list.pop(0)
        second_thread = threading.Thread(target=thread_func,args=(url, 1))
    if len(full_result) >= 2000:
        while first_thread.is_alive() and second_thread.is_alive():
            time.sleep(2)
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS word_count (
                word TEXT PRIMARY KEY,
                count INTEGER
            )
        ''')

        for word, count in full_result.items():
            cursor.execute('INSERT OR IGNORE INTO word_count (word, count) VALUES (?, 0)', (word,))
            cursor.execute('UPDATE word_count SET count = count + ? WHERE word = ?', (count, word))

        conn.commit()
        conn.close()
        full_result = {}
while first_thread.is_alive() and second_thread.is_alive():
    time.sleep(2)
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS word_count (
        word TEXT PRIMARY KEY,
        count INTEGER
    )
''')

for word, count in full_result.items():
    cursor.execute('INSERT OR IGNORE INTO word_count (word, count) VALUES (?, 0)', (word,))
    cursor.execute('UPDATE word_count SET count = count + ? WHERE word = ?', (count, word))

conn.commit()
conn.close()
full_result = {}
print(full_result)
