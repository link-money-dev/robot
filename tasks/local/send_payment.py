# -*- coding:utf-8 -*-
# 该模块给出了一个单线程发币的例子，多线程发币见 ***

import CONSTANT
from wrapper.client import Client
from wrapper import builder as BUILDER
from tools import load_json

constant=CONSTANT.Constant('local')
# fixtures
client1=Client(private_key='SDQREYINW3OPRIKX5J6PSU3ZWEVRYPNJGMEAZFQ2CLQMUGDZUGUP4AX2')
client2=Client(private_key='SDTH3244ZJLICKJUNGOS3W3GS3GVPCOE24XS76FZSRAWFRWMBJH6S73N')
client3=Client(private_key='SDWDDZ7ALH27JHCZ22GFVFBGC3J7IPZJZXMAABP6AWBILYPGIDA5TH2P')
clients=[client1,client2,client3]

# 定义一个发币端
builder=BUILDER.Builder(secret='SDS4FTMCD55TNALNKNAMMZ6DF24STEMJSBZ66OPSY7WXZ7FUT4G2NRTB',network=constant.API_SERVER, horizon='http://localhost:8888')
master=Client(private_key=constant.SEED, api_server=constant.API_SERVER)

builder.append_payment_op(destination=client1.address,amount=1)
builder.add_text_memo('000000000+000000000+000000000+000000000+000000000+000000000')
builder.sign()
builder.submit()


# send fotono
client=Client(private_key=constant.SEED, api_server=constant.API_SERVER)
client.pay_to(destination='GCPPN2D7COSSQVP3LL3TKUAZNWEP2AEKITO57TDF42DBQEKESDA7CNXZ', amount=200)

# send link
client=Client(private_key=constant.DISTRIBUTOR_SEED,api_server=constant.API_SERVER)
result=client.pay_to(destination='GBBKSTPOVEUOXKTBMWYXLIAVIQSIUSJFQARFEGD4HGIMPDCEKS4FVZXP',amount=0.01,asset_code='LINK',asset_issuer=constant.ISSUER_ADDRESS)
print(result)