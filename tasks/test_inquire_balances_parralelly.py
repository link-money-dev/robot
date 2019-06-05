# passed
from wrapper.client import Client
from wrapper import db as DB
import os
import requests
import threading
import json

result=[]
def store_response(address):
    content = requests.get('http://47.52.0.154:8888/accounts/' + address)
    content=content.content
    try:
        content=json.loads(content)
        balance=float(content['balances'][0]['balance'])
        result.append((address,balance))
    except Exception as e:
        print(e)

store_response('GAA6EXQ7OZPJI4KWH3DNDNVEDAJ6QXF2DEDIKU7CGROWKHWDFQJAT5SQ')
path = os.getcwd()
DB_NAME = path + '\\keys.db'

my_sql_manager = DB.SQLManager(DB_NAME)
rows = my_sql_manager.execute('select * from keys order by ID asc limit 1024')

addresses = []
threads = []

for i in range(512):
    address = rows[i][2]
    thread = threading.Thread(target=store_response, args=(address,))
    threads.append(thread)
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()



a = 1