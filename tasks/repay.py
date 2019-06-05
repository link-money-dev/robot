from  wrapper import  builder as BUILDER
from  wrapper import client as CLIENT
import CONSTANT
from wrapper import db as DB
from wrapper import operation as OPERATION
import requests
import json

# -------------------------------------------------------------------------------------
constant=CONSTANT.Constant('local')
my_pgmanager=DB.PGManager(**constant.HORIZON_DB_CONNECT_ARGS)
issuer_private_key_for_LINK='SDCCOAL6ILCJXWQPDZLRNHTMAHLZHC2IIHGPSQMLSIPHRTLNCFNT4A66'
issuer_address_for_LINK='GCA3SBI2Y6AYHLAW2GBTS7C5HTSFW6OTZACHOVJGBQ6JENTE3ZXPNNSL'
distributor_private_key_for_LINK='SCWDXYXEJL6GQWXUADDGFGFPF64ORWHXA7R2FNV4UVS6VIBIQCVD53JH'
distributor_address_for_LINK='GCONR7JZN7VUSFI54BS76VQJRWGUZDLQFPTB7DXHNP6E5KZECUW77VFL'

issuer_private_key_for_CNY='SBWATTQW5UDSVNZ7BVKX3DPR4EJFZCRUBYKRG5SMDESRSD5QWG7VSDQH'
issuer_address_for_CNY='GCNYF4V6CUY2XENJGRHLNB3AQE3RZIOWYHUN6YU5T34N3ZSK4KGCB7DD'
distributor_private_key_for_CNY='SCZVR6ZS3UKV3YHTK5YJJ3E7WD6RLWKJDPRTUNYQQ54BDFAYEQ4JDZ6S'
distributor_address_for_CNY='GB552GC4YLN7O7Z6DDDFOO7ZPK6374H4YZGZ4YJMWQW6HBRRAWNSIIQW'

# define 2 clients which are used to distribute link and cny selectively
client_to_distribute_link=CLIENT.Client(private_key=distributor_private_key_for_LINK,api_server='public')
client_to_distribute_cny =CLIENT.Client(private_key=distributor_private_key_for_CNY, api_server='public')

# -------------------------------------------------------------------------------------

def check_trust(address):
    horizon_pgmanager=DB.PGManager(**CONSTANT.DB_CONNECT_ARGS_HORIZON_PUBLIC)
    sql='select * from history_operations where source_account=\''+address+'\' and type=6'
    rows=horizon_pgmanager.select(sql)
    has_trusted_cny=False
    has_trusted_link=False
    if len(rows)==0:
        return False
    for row in rows:
        details=row[4]
        if details['asset_code']=='LINK':
            has_trusted_link=True
        if details['asset_code']=='CNY':
            has_trusted_cny=True
        a=1
    if has_trusted_cny==True and has_trusted_link==True:
        return True
    else:
        return False
    # res = requests.get('http://47.52.0.154:8888/accounts/' + address)
    # content=res.content
    # has_trusted_cny=False
    # has_trusted_link=False
    # try:
    #     content=json.loads(content)
    #     balances=content['balances']
    #     for item in balances:
    #         if dict(item).get('asset_code','None')=='LINK':
    #             has_trusted_link=True
    #         if dict(item).get('asset_code','None')=='CNY':
    #             has_trusted_cny=True
    #     if has_trusted_link==True and has_trusted_cny==True:
    #         return True
    #     else:
    #         return False
    # except Exception as e:
    #     return False

# test for check_trust
# address='GBSUS3QVUS7PIBROUKR4KUFU5ME2PJVI5ID6MMHYHRWPHFCWA7SQTG5R'
# r=check_trust(address)
# test for client topay
# address='GCN5WCMOYGUT27VOWGJUUMFK6NDOP7IVQNK6UIPKSKAGXZ4D5YUR54HE'
# print(client_to_distribute_cny.pay_to(address,0.00113,'CNY',issuer_address_for_CNY))

# fetch all accounts
accounts={}
rows=my_pgmanager.select('select * from liabilities where has_paid=0 ')

# iterate over all rows and decide which is to pay link and cny, after paying, set has_paid to 1
count=0
for row in rows:
    # check if this account has trusted link and cny both
    count+=1
    total_asset_equivalant_to_cny=row[4]
    if total_asset_equivalant_to_cny<50 :
        continue
    has_trusted_both_assets = check_trust(row[0])
    if has_trusted_both_assets == False:
        continue
    address=row[0]
    if has_trusted_both_assets==True:
        link_to_pay=row[1]
        cny_to_pay=row[2]
        if cny_to_pay>0.001:
            client_to_distribute_cny.pay_to(address,cny_to_pay,'CNY',issuer_address_for_CNY)
        if link_to_pay>0.001:
            client_to_distribute_link.pay_to(address,link_to_pay,'LINK',issuer_address_for_LINK)
        sql='update liabilities set has_paid=1 where account_id=\'' + address + '\''
        my_pgmanager.execute(sql)
        print(address+' has been sent '+str(link_to_pay) + ' LINK and ' + str(cny_to_pay) + 'CNY.\n')
