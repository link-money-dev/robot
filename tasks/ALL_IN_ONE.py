# -*- coding: UTF-8 -*-

import distribute_link_to_wechat
import send_orders
import CONSTANT
from wrapper.client import Client
from wrapper import builder as BUILDER
constant=CONSTANT.Constant('public')
seed='SDQ43Z762OW6L7YBCRBNB2LL57YADNHARB2AW4RE45RSKM7PWRTT76PT'


def fund_addresses(addresses):
    builder=BUILDER.Builder(secret=seed, network=constant.API_SERVER)
    for address in addresses:
        builder.append_create_account_op(destination=address, starting_balance=100)
    builder.sign()
    builder.submit()

def pay_to_addresses(addresses):
    builder = BUILDER.Builder(secret=seed, network=constant.API_SERVER)
    for address in addresses:
        builder.append_payment_op(destination=address, amount=100000)
    builder.sign()
    builder.submit()

if __name__=='__main__':
    # 1. fund addresses:
    # addresses = ['GA7FQTM7JE7Q6LK7NES7XFEYD5HRPAUBTQM5W4T4GK6XLYO7XAPGLDXZ']
    # fund_addresses(addresses)

    # 2. pay
    addresses=['GCA3SBI2Y6AYHLAW2GBTS7C5HTSFW6OTZACHOVJGBQ6JENTE3ZXPNNSL']
    pay_to_addresses(addresses)