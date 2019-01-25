# -*- coding:utf-8 -*-
# 该模块给出了一个单线程发币的例子，多线程发币见 ***

import CONSTANT
from wrapper.client import Client
from tools import load_json
from  wrapper import db as DB
from wrapper import builder as BUILDER

constant=CONSTANT.Constant('public')
sql_manager=DB.SQLManager('keys.db')
rows=sql_manager.execute('select * from keys')


# 定义一个发币端
seed='SDYYLWVFTUPF6QKVYEUWP7GR5X3SFY2MOPMEPPPCES5ZT2DYJIBY4P63'
client=Client(private_key=constant.SEED, api_server=constant.API_SERVER)

# for i in range(0,9):
#     builder = BUILDER.Builder(seed, network=constant.API_SERVER)
#     current_rows=rows[i*100:i*100+100]
#     for row in current_rows:
#         public_key=row[1]
#         builder.append_create_account_op(public_key,100000000)
#     builder.sign()
#     builder.submit()

# for i in range(9,10):
#     builder = BUILDER.Builder(seed, network=constant.API_SERVER)
#     current_rows = rows[i * 100:i*100 + 99]
#     for row in current_rows:
#         public_key = row[1]
#         builder.append_create_account_op(public_key, 100000000)
#     builder.sign()
#     builder.submit()

builder = BUILDER.Builder(seed, network=constant.API_SERVER)
current_row=rows[-1:]
public_key = current_row[0][1]
builder.append_create_account_op(public_key, 99999999-20)
builder.sign()
builder.submit()
# # 定义一个收币端，of Client
# destination=Client(address=constant.ISSUER_ADDRESS)
#
# # client.fund(destination='GD6JTH7LE25ER42V7SLMQ4OH73WURPWV34W7MCYBFXLFSBR4E5425PHP', amount=100)
# client=Client(private_key=constant.DISTRIBUTOR_SEED, api_server=constant.API_SERVER)
# client.pay_to(destination='GD6JTH7LE25ER42V7SLMQ4OH73WURPWV34W7MCYBFXLFSBR4E5425PHP', amount=10, asset_code='LINK', asset_issuer=constant.ISSUER_ADDRESS)
#
