# -*- coding: UTF-8 -*-
import sys
sys.path.append("..")
import requests
import json
import random
import CONSTANT
from wrapper import db as DB
import schedule

constant=CONSTANT.Constant('public')
url=constant.BASE_URL + '/link/api/call/run/orders'
url2=constant.BASE_URL + '/link/api/call/run/orders_q'
user_tokens=['oliver','Thor','jeff','gary','jessy','omega','lindsey','mary','c001','c002','c003','Jacob','Michael','Ethan','Joshua','Alexander','Anthony','William','Christopher','Jayden','Andrew','Joseph','David','Noad','Aiden','James','Ryan','Logan','John','Nathan','Elijah','Christian','Gabriel','Benjamin','Jonathan','Tyler','Samuel','Nicholas','Gavin','Dylan']
# user_tokens=['oOZg40kK2BLQAXxGY29kpxXetc0c','oliver','Thor','jeff','gary']
# user_tokens=['bitch','slut','whore','motherfucker']
# user_tokens=['1001','1002','1003','1004','1005','1006','1007']
user_tokens=[]
prefix='Oxxx'
for i in range(10):
    user_token=prefix
    for j in range(10):
        user_token+=random.choice('1 2 3 4 5 6 7 8 9 0 p o i u y t r e w q a s d f g h j k l m n b v c x z'.split(' '))
    user_tokens.append(user_token)
fees=[1]
order_no=15200
def send_orders(span=300, interval=0.5):
    global user_tokens
    import time

    global order_no

    t0=time.time()
    end_time=t0+span

    # while t0<end_time:
    #     t0=time.time()
    #     data = {'UserToken': random.choice(user_tokens), 'OrderAmount': random.choice(fees), 'OrderNo':str(order_no).rjust(8,'0')}
    #     order_no+=1
    #     r=requests.post(url,data=data).text
    #     print(r)
    #     time.sleep(interval)
    while t0<end_time:
        for token in user_tokens:
            t0 = time.time()
            data = {'UserToken': token, 'OrderAmount': random.choice(fees),
                    'OrderNo': str(random.randint(1,1000000000)).rjust(16, '0')}
            order_no += 1
            r = requests.post(url, data=data).text
            print(r)
            time.sleep(interval)
        time.sleep(300)

def send_orders2():
    user_tokens = [
        'oucE10XP5VPF5t86nWp-4L7jRCsQ',
        'oucE10e6W6Qem_oGQ_Lkk4Bz-cuY',
        'oOZg40qEEE5NPaNNnhC6jETtlBVc',
        'oOZg40hX-huCNqKfuGGpihW5cfqw',
        'oOZg40kK2BLQAXxGY29kpxXetc0c'
    ]
    import random
    import time


    for user_token in user_tokens:
        data = {'UserToken': user_token, 'OrderAmount': random.choice(fees) ,
                'OrderNo': str(random.randint(1,1000000000)).rjust(16, '0')}
        # time.sleep(random.randint(0, 30))
        r = requests.post(url, data=data).text
        print(r)
        data = {'UserToken': user_token, 'OrderAmount': random.choice(fees),
                'OrderNo': str(random.randint(1, 1000000000)).rjust(16, '0')}
        r=requests.post(url2,data=data).text
        print(r)

if __name__=='__main__':
    global user_tokens
    from tools import timer as TIMER
    # constant=CONSTANT.Constant('public')
    # old_constant=CONSTANT.Constant('test')
    # old_pgmanager=DB.PGManager(**old_constant.DB_CONNECT_ARGS)
    # my_pgmanager = DB.PGManager(**constant.DB_CONNECT_ARGS)
    # rows = my_pgmanager.select('select distinct usertoken from orders where usertoken like \'%oOZg40%\'')
    # for row in rows:
    #     user_tokens.append(row[0])
    send_orders2()