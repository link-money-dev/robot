# -*- coding:utf-8 -*-
# 该模块给出了一个单线程发币的例子，多线程发币见 ***

import CONSTANT
from wrapper.client import Client
from wrapper import builder as BUILDER
from tools import load_json

constant=CONSTANT.Constant('public')

# 定义一个发币端
seed=constant.SEED
seed='SA7WDEIBHFVSKWH6Q7UNCVVDEGXOGB5H3D7SWWKD6OTMWQH43V3G53H3'
client=Client(private_key=constant.SEED, api_server=constant.API_SERVER)

# 定义一个收币端，of Client
destination=Client(address=constant.ISSUER_ADDRESS)

# client.pay_to(destination='GCA3SBI2Y6AYHLAW2GBTS7C5HTSFW6OTZACHOVJGBQ6JENTE3ZXPNNSL', amount=1000000)
client=Client(private_key='SCZVR6ZS3UKV3YHTK5YJJ3E7WD6RLWKJDPRTUNYQQ54BDFAYEQ4JDZ6S', api_server=constant.API_SERVER)
client.pay_to(destination='GAMEXYMNGLDLG6HBXAGSKIN5GYYE2J6CB3Q376HW5BMECY62POVSTCZQ', amount=400)