# -*- coding:utf-8 -*-
# 该模块给出了一个单线程发币的例子，多线程发币见 ***

import CONSTANT
from wrapper.client import Client
from tools import load_json

constant=CONSTANT.Constant('public')

# 定义一个发币端
seed=constant.SEED
client=Client(private_key=constant.SEED, api_server=constant.API_SERVER)
# 定义一个收币端，of Client
destination=Client(address=constant.DISTRIBUTOR_ADDRESS)

# client.fund(destination=constant.DISTRIBUTOR_ADDRESS, amount=1000000)
client.pay_to(destination=constant.DISTRIBUTOR_ADDRESS, amount=1000000, asset_code='LINK', asset_issuer=constant.ISSUER_ADDRESS)

