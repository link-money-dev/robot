import CONSTANT
from wrapper.client import Client
from wrapper import builder as BUILDER
from wrapper import db as DB

# define 2 pg_managers
my_pgmanager_for_lyl_ordedrs=DB.PGManager(**CONSTANT.DB_CONNECT_ARGS_PUBLIC)
my_pgmanager_for_public_horizon=DB.PGManager(**CONSTANT.DB_CONNECT_ARGS_HORIZON_PUBLIC)

# import public keys from lyl_orders:
accounts_in_lyl_orders=[]
rows_in_lyl_orders=my_pgmanager_for_lyl_ordedrs.select('select public_key from private_keys')
for row in rows_in_lyl_orders:
    accounts_in_lyl_orders.append(row[0])

# import public keys from public horizon:
accounts_in_public_horizon=[]
rows_in_public_horizon=my_pgmanager_for_public_horizon.select('select address from history_accounts')
for row in rows_in_public_horizon:
    accounts_in_public_horizon.append(row[0])
# accounts to be activated should be those accounts exist in lyl_orders yet not in public horizon:
# so: accounts_in_lyl_orders-accounts_in_public_horizon
accounts_to_be_activated=list(set(accounts_in_lyl_orders).difference(set(accounts_in_public_horizon)))


constant=CONSTANT.Constant('public')
client=Client(private_key='SDQ43Z762OW6L7YBCRBNB2LL57YADNHARB2AW4RE45RSKM7PWRTT76PT',api_server=constant.API_SERVER)
# ..UAA

# for i in range(0,len(accounts_to_be_activated)/100+1):
#     accounts_to_be_activated_in_this_loop=accounts_to_be_activated[i*100:i*100+100]
#     builder = BUILDER.Builder(secret='SDQ43Z762OW6L7YBCRBNB2LL57YADNHARB2AW4RE45RSKM7PWRTT76PT',
#                               network=constant.API_SERVER)
#     for account in accounts_to_be_activated_in_this_loop:
#         builder.append_create_account_op(destination=account,starting_balance=200)
#     builder.sign()
#     print(builder.submit())

# single thread activation:
for account in accounts_to_be_activated:
    res=client.fund(destination=account, amount=200)
    print(account)
