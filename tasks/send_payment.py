# -*- coding:utf-8 -*-
# 该模块给出了一个单线程发币的例子，多线程发币见 ***

import CONSTANT
from wrapper.client import Client
from tools import load_json

constant=CONSTANT.Constant('public')

# 定义一个发币端
seed=constant.SEED
seed='SDQ43Z762OW6L7YBCRBNB2LL57YADNHARB2AW4RE45RSKM7PWRTT76PT'
client=Client(private_key=seed, api_server=constant.API_SERVER)
# 定义一个收币端，of Client
destination=Client(address=constant.ISSUER_ADDRESS)

client.fund(destination='GCONR7JZN7VUSFI54BS76VQJRWGUZDLQFPTB7DXHNP6E5KZECUW77VFL', amount=10000)
client=Client(private_key=constant.DISTRIBUTOR_SEED, api_server=constant.API_SERVER)
client.pay_to(destination='GD6JTH7LE25ER42V7SLMQ4OH73WURPWV34W7MCYBFXLFSBR4E5425PHP', amount=10, asset_code='LINK', asset_issuer=constant.ISSUER_ADDRESS)

