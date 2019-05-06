# -*- coding: UTF-8 -*-

# 该模块给出了一个发行数字资产的例子
# 发行资产需要两个账户：一个是发行账户，一个是分发账户，产生的资产在分发账户里
# 对于本例，产生的资产咋子distributor这个账户里

# 发行账户即：
# 分发账户即：
import wrapper.client as CLIENT
import CONSTANT



constant=CONSTANT.Constant('public')
issuer_private_key_for_LINK='SDCCOAL6ILCJXWQPDZLRNHTMAHLZHC2IIHGPSQMLSIPHRTLNCFNT4A66'
issuer_address_for_LINK='GCA3SBI2Y6AYHLAW2GBTS7C5HTSFW6OTZACHOVJGBQ6JENTE3ZXPNNSL'
distributor_private_key_for_LINK='SCWDXYXEJL6GQWXUADDGFGFPF64ORWHXA7R2FNV4UVS6VIBIQCVD53JH'
distributor_address_for_LINK='GCONR7JZN7VUSFI54BS76VQJRWGUZDLQFPTB7DXHNP6E5KZECUW77VFL'

issuer_private_key_for_CNY='SBWATTQW5UDSVNZ7BVKX3DPR4EJFZCRUBYKRG5SMDESRSD5QWG7VSDQH'
issuer_address_for_CNY='GCNYF4V6CUY2XENJGRHLNB3AQE3RZIOWYHUN6YU5T34N3ZSK4KGCB7DD'
distributor_private_key_for_CNY='SCZVR6ZS3UKV3YHTK5YJJ3E7WD6RLWKJDPRTUNYQQ54BDFAYEQ4JDZ6S'
distributor_address_for_CNY='GB552GC4YLN7O7Z6DDDFOO7ZPK6374H4YZGZ4YJMWQW6HBRRAWNSIIQW'

issuer_private_key_for_OTHERS='SC53U46XXITEIDTDHLKUJAETF2JSLRQ6GKLMEYUAL3YO32EOKPXNFM44'
issuer_address_for_OTHERS='GBTCF6RETMMKZ6NKXIIAL5X3JZEZY2DPIIW77IZ6NWTNIUSAY37EQWAR'
distributor_private_key_for_OTHERS='SCZVR6ZS3UKV3YHTK5YJJ3E7WD6RLWKJDPRTUNYQQ54BDFAYEQ4JDZ6S'
distributor_address_for_OTHERS='GB552GC4YLN7O7Z6DDDFOO7ZPK6374H4YZGZ4YJMWQW6HBRRAWNSIIQW'

# issue LINK
issuer=CLIENT.Client(private_key=issuer_private_key_for_LINK, api_server=constant.API_SERVER)
distributor=CLIENT.Client(private_key=distributor_private_key_for_LINK, api_server=constant.API_SERVER)
result=issuer.issue_asset(distributor.private_key,asset_code='LINK',amount=1000000000)
print(result)
#
# # issue CNY
# issuer=CLIENT.Client(private_key=issuer_private_key_for_CNY, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_CNY, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='CNY',amount=10000000)
# print(result)
#
# # issue FX
# issuer=CLIENT.Client(private_key=issuer_private_key_for_CNY, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_CNY, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='FX',amount=21000000)
# print(result)

# issue Others
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='BTC',amount=21000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='ETH',amount=104000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='LTC',amount=84000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='XRP',amount=100000000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='BCH',amount=21000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='EOS',amount=1000000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='XLM',amount=100000000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='USD',amount=2580000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='ADA',amount=31000000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='XMR',amount=17000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='IOTA',amount=2700000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='DASH',amount=18900000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='TRX',amount=99000000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='NEO',amount=100000000)
# print(result)

# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='ETC',amount=107000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='XEM',amount=8999999999)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='ZEC',amount=5000000)
# print(result)
#
# issuer=CLIENT.Client(private_key=issuer_private_key_for_OTHERS, api_server=constant.API_SERVER)
# distributor=CLIENT.Client(private_key=distributor_private_key_for_OTHERS, api_server=constant.API_SERVER)
# result=issuer.issue_asset(distributor.private_key,asset_code='MKR',amount=1000000)
# print(result)