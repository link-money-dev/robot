# -*- coding:utf-8 -*-

import CONSTANT
from wrapper import keypair
from wrapper.client import Client
from tools import load_json
from wrapper import builder as BUILDER

constant=CONSTANT.Constant('test')

# fund a random account
def fund_a_random_account():
    seed=constant.SEED
    client=Client(seed,api_server=constant.API_SERVER)
    destination=keypair.Keypair.random()
    address=destination.address().decode().encode('ascii')
    print(address)
    client.fund(destination=address,amount=30)

# fund an account
def fund_an_account(id,amount):
    seed=constant.SEED
    client=Client(seed,api_server=constant.API_SERVER)
    address=id
    print(address)
    client.fund(destination=address,amount=amount)

# fund the first 100 accounts in keys.json
def fund_accounts_in_keys_dot_json(lower_bound=0, upper_bound=1):
    seed=constant.SEED
    client=Client(seed,api_server=constant.API_SERVER)
    builder=BUILDER.Builder(secret=seed)
    keys=None
    keys=load_json.file2json('keys.json')[lower_bound:upper_bound]
    for key in keys:
        address=key['public_key']
        print(address)
        builder.append_create_account_op(destination=address, starting_balance=100)
    builder.sign()
    builder.submit()


if __name__=='__main__':
    import time
    # while True:
    #     fund_a_random_account();
    #     time.sleep(5)
    # fund_accounts_in_keys_dot_json(lower_bound=102, upper_bound=103)
    fund_an_account('GCHZDZXYLZ76XADS7735LK3OJUFZ2TBSXAR23YXKXCXXHUEEVT5C37PY',100000)
