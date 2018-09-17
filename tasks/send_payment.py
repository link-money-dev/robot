# -*- coding:utf-8 -*-
# 该模块给出了一个单线程发币的例子，多线程发币见 ***

import CONSTANT
from wrapper.client import Client
from wrapper import builder as BUILDER
from tools import load_json
keys=[
    ('GBKCZZZERNVJPGCPCPGXE5JTKGRTDY65QUQOFZ6YWTVQQF5GG2DMJNA6',30000000),
    ('GAWZIVH2PQHM57226665UNDRYZRBNDFC5O6XPQQU7E2ZNSN5B373EWEX',20000000),
    ('GDJSPDJOS3M6DJCIW4HKS4BBY3IKS5UNUDPUHYSJAQTNBXKDTGL3X7AI',25000000),
    ('GCIUT63MYY6LJ2ZW65M7E6EHPFPCD7BHDIOTXVM7WB67RNVYDNDFBJ7P',25000000),
    ('GBRBJ5MOJZJESMEY3RKCQFSBPOO3QHBVMXNJ5JNCMZITWVBZM7YJMADG',50000000),
    ('GCBTC5KZTWNXQLQAYT3NYG2IJJG6IX4F4G6A6EQDLBXPQOPYYFJ7RGFN',50000000),
    ('GC43P4PKMFE37UFHSRVKY6HBEQORCFZNWXFBXIKTFIUO2BBY7NZNXZL3',50000000),
    ('GB3F6LSWZTXULWWOYQY6RORXUGUQULOSPWMN6QX23EAJTIM2BGPU7AR6',50000000),
    ('GAOUYGFTPT7RO3VBQSDABXVKL5DRJNS3ZUMAARZ5UIBQIUIANGDHSDSV',50000000),
    ('GD43ZFXSJMJNNOIWJ2WY5H5CVISLN7LCZP2HK5GS3JZ5ZC2GL5763HX6',50000000)
    ]

constant=CONSTANT.Constant('public')

# 定义一个发币端
seed=constant.SEED
seed='SDQ43Z762OW6L7YBCRBNB2LL57YADNHARB2AW4RE45RSKM7PWRTT76PT'
client=Client(private_key=seed, api_server=constant.API_SERVER)

# 定义一个收币端，of Client
destination=Client(address=constant.ISSUER_ADDRESS)

# builder=BUILDER.Builder(secret=seed,network=constant.API_SERVER)
# for key in keys:
#     builder.append_create_account_op(destination=key[0],starting_balance=100)
# builder.sign()
# builder.submit()

builder=BUILDER.Builder(secret=constant.DISTRIBUTOR_SEED,network=constant.API_SERVER)
for key in keys:
    builder.append_payment_op(destination=key[0],amount=key[1],asset_type='LINK',asset_issuer=constant.ISSUER_ADDRESS)
builder.sign()
res=builder.submit()

client.fund(destination='GCONR7JZN7VUSFI54BS76VQJRWGUZDLQFPTB7DXHNP6E5KZECUW77VFL', amount=10000)
client=Client(private_key=constant.DISTRIBUTOR_SEED, api_server=constant.API_SERVER)
client.pay_to(destination='GD6JTH7LE25ER42V7SLMQ4OH73WURPWV34W7MCYBFXLFSBR4E5425PHP', amount=10, asset_code='LINK', asset_issuer=constant.ISSUER_ADDRESS)

