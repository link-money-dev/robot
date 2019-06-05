from wrapper import client as CLIENT
from wrapper import db as DB
import CONSTANT
import requests
import json as JSON

seed='SDJPAJAY223ECKE5UMLFA66XW6L7S53TNYAPEB5SSHKG2LVL27MHJC7O'

constant=CONSTANT.Constant('public')
client=CLIENT.Client(seed,api_server=constant.API_SERVER)
# client.pay_to('GB552GC4YLN7O7Z6DDDFOO7ZPK6374H4YZGZ4YJMWQW6HBRRAWNSIIQW',1,asset_code='CNY',asset_issuer='GCNYF4V6CUY2XENJGRHLNB3AQE3RZIOWYHUN6YU5T34N3ZSK4KGCB7DD')
data=requests.get('http://47.52.0.154:8888/accounts/GCNY2H4OAQNSVG2WUQ5EGABFLEG2GXF3OZZVJCQB7N2KCIGWVTY6WTHB').text
data=dict(JSON.loads(data)['data'])
for key in data.keys():
    print(key)
    client.manage_data(key,None)
client.manage_data('test',None)

chars='a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9'.split(' ')
import random
for i in range(0,100):
    key=''
    value=''
    for j in range(0, 10):
        key+=random.choice(chars)
        value+=random.choice(chars)
    client.manage_data(key,value)