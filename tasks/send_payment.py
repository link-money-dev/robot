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

# send fotono
client=Client(private_key=constant.SEED, api_server=constant.API_SERVER)
client.pay_to(destination='GCPPN2D7COSSQVP3LL3TKUAZNWEP2AEKITO57TDF42DBQEKESDA7CNXZ', amount=200)

# send link
client=Client(private_key=constant.DISTRIBUTOR_SEED,api_server=constant.API_SERVER)
result=client.pay_to(destination='GBBKSTPOVEUOXKTBMWYXLIAVIQSIUSJFQARFEGD4HGIMPDCEKS4FVZXP',amount=0.01,asset_code='LINK',asset_issuer=constant.ISSUER_ADDRESS)
print(result)