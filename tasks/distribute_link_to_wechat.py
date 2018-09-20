# -*- coding: UTF-8 -*-
import sys
sys.path.append("..")
from wrapper import db as DB
from wrapper import builder as BUILDER
from wrapper import client as CLIENT
import CONSTANT
import schedule
import time
from tasks import key_generation
from wrapper import user as USER
import requests
import json
import threading
from tools import timer as TIMER

# -1 CONSTANTS:
key='Xjr;H^P(RepxganS'
iv='7297115918661978'
constant=CONSTANT.Constant('public')
# 0. init
my_pgmanager=DB.PGManager(**constant.DB_CONNECT_ARGS)
horizon_pgmanager = DB.PGManager(**constant.HORIZON_DB_CONNECT_ARGS)

accounts_to_be_activated_by_inquiring_blockchain=[]
# 1. join inquery:

# √√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√
def total_link_to_be_distributed():
    t=time.time()
    if t<1537203600:
        return 5477
    else:
        return -0.025 * int((t-1537203600)/3600) + 5477.2135

def allocate_key(user_tokens):
    for user_token in user_tokens:
        sql='select * from private_keys where user_token=\'' + user_token + '\''
        row=my_pgmanager.select(sql)
        if len(row)==0:
            keypairs = key_generation.generate_keypairs(1, key, iv, False)
            sql='insert into private_keys(user_token,private_key,public_key) values(\'%s\',\'%s\',\'%s\')' % (user_token,keypairs[0][0],keypairs[0][1])
            my_pgmanager.execute(sql)
            a=1
    pass

def get_users_and_total_expenses(t, interval=3600):
    # dt = '2018-01-01 10:40:30'
    # ts = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
    datetime_upperbound = t
    datetime_lowerbound = datetime_upperbound-interval
    sql='select * from orders where created_at<' + str(datetime_upperbound) + ' and created_at>' + str(datetime_lowerbound) + ' and is_filled=0'
    rows=my_pgmanager.select(sql)
    # get all distinct user_tokens:
    user_tokens=[]
    total_expenses=0
    for row in rows:
        token = row[1]
        user_tokens.append(token)
    user_tokens = list(set(user_tokens))
    users={}
    for row in rows:
        token = row[1]
        expense = row[3]
        if not users.__contains__(token):
            sql = 'select * from private_keys where user_token=\'' + token + '\''
            rs = my_pgmanager.select(sql)
            if len(rs) == 0:
                keypair = key_generation.generate_keypairs(1, key, iv, False)[0]
                sql = 'insert into private_keys(user_token,private_key,public_key, is_activated) values(\'%s\',\'%s\',\'%s\',0)' % (
                    token, keypair[0], keypair[1])
                my_pgmanager.execute(sql)
                user = USER.User(token, expense, keypair[1], keypair[0], 0)
            else:
                keypair = (rs[0][2], rs[0][3])
                is_activated = rs[0][6]
                user = USER.User(token, expense, keypair[1], keypair[0], 1)
            users[token] = user
        else:
            users[token].add_expense(expense)
        total_expenses += expense
    result=(users,total_expenses)
    return result

def calculate_link_to_be_distributed_to_single_person(users, total_expenses, log=True):
    import copy
    users_ = copy.deepcopy(users)
    if len(users_) != 0:
        total_link = total_link_to_be_distributed()
        for k in users_:
            user = users_[k]
            link_to_be_distributed = float(user.expense) / float(total_expenses) * total_link
            user.link = round(link_to_be_distributed, 6)
    else:
        pass
    return users_

def append_inactivated_public_key_by_inquiring_blockchain(address):
    global accounts_to_be_activated_by_inquiring_blockchain
    res = requests.get('http://116.62.226.231:8888/accounts/' + address).text
    if res.find('"asset_type": "native"') == -1:
        accounts_to_be_activated_by_inquiring_blockchain.append(address)

def get_inactive_accounts(accounts, instance='test'):
    constant=CONSTANT.Constant(instance)
    horizon_pgmanager = DB.PGManager(**constant.HORIZON_DB_CONNECT_ARGS)
    sqls=[]
    active_accounts = []
    addresses=[]
    for account in accounts:
        addresses.append(account[1])
    str_addresses='\',\''.join(addresses)
    sql='select address from history_accounts where address in (\'' + str_addresses + '\')'
    rows=horizon_pgmanager.select(sql)  # get all the activated rows in the list: addresses
    for row in rows:
        active_accounts.append(row[0])
        sqls.append({'public_key': row[0]})
    my_pgmanager.execute_many('update private_keys set is_activated=1 where public_key=%(public_key)s',
                              sqls)
    inactive_accounts=list(set(addresses).difference(set(active_accounts)))
    return inactive_accounts

def get_untrusting_accounts(accounts, constant=None):
    # we have to make sure that incoming arg {accounts} are active accounts whereas not yet trust LINK
    horizon_pgmanager = DB.PGManager(**constant.HORIZON_DB_CONNECT_ARGS)
    trustee=constant.ISSUER_ADDRESS
    code=constant.ASSET_CODE
    import copy
    sqls=[]
    untrusting_accounts = copy.deepcopy(accounts)
    for account in accounts:
        sql='select * from history_operations where source_account=\'' + account[1] +'\''
        rows=horizon_pgmanager.select(sql)
        if len(rows)==0:
            pass
        else:
            for row in rows:
                detail=dict(row[4])
                if detail.get('trustee','')==trustee and detail.get('asset_issuer')==trustee and detail.get('asset_code')==code:
                    untrusting_accounts.remove(account)
                    sqls.append({'public_key': account[1]})
                    break
    my_pgmanager.execute_many('update private_keys set has_trusted=1 where public_key=%(public_key)s', sqls)

    return untrusting_accounts


def activate_accounts(instance='test'):
    '''
    1. this function requires zero arguments,
    2. api_server => horizon interface;
    3. horizon_DB_server => direct horizon DB server;
    3. DB_server => lyl_orders

    :return: None
    '''
    constant=CONSTANT.Constant(instance)
    api_server=constant.API_SERVER
    db_connet_args=constant.DB_CONNECT_ARGS

    # 0. instancialize a BUILDER?????????????????
    builder = BUILDER.Builder(secret=constant.SEED, network=constant.API_SERVER)

    # 1. get the accounts to be activated:
    accounts_to_be_activated = []
    my_pgmanager=DB.PGManager(**db_connet_args)
    sql = 'select private_key, public_key from private_keys where is_activated=0'
    all_accounts = []
    rows = my_pgmanager.select(sql)
    for row in rows:
        private_key = row[0]
        public_key = row[1]
        all_accounts.append((private_key, public_key))

    # inquire horizon DB server directly to determine which public keys are to be ACTIVATED
    accounts_to_be_activated = get_inactive_accounts(all_accounts, instance='public')
    # activate all the accounts by using multi ops
    if len(accounts_to_be_activated) != 0:
        try:
            sqls = []
            for account in accounts_to_be_activated:
                builder.append_create_account_op(destination=account, starting_balance=constant.FOTONO_STARTING_BALANCE)
                sqls.append({'public_key': account})
            builder.sign()
            res = builder.submit()

            # if dict(res).__contains__('hash') means the transaction is SUCCESSFUL
            if dict(res).__contains__('hash'):
                my_pgmanager.execute_many('update private_keys set is_activated=1 where public_key=%(public_key)s',
                                          sqls)
            # else the transaction MAY be SUCCESSFUL or UNSUCCESSFUL, so we do nothing
            else:
                pass
        except Exception as e:
            print('Accounts creation failed.\n' + e.message)
    else:
        pass
    pass

def main():
    # cnt=0
    global cnt
    cnt+=1
    t = int(time.time())
    timeArray = time.localtime(t)
    otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
    print('Epoch:   %s\tTime:   %s' % (str(cnt),otherStyleTime))
    users = {}
    expenses = {}
    total_expenses = 0

    # 0. get all distinct users group by token, and total expenses
    users,total_expenses=get_users_and_total_expenses(t, 1000000)

    # 1. calculate the link to be distributed to the single person
    users=calculate_link_to_be_distributed_to_single_person(users,total_expenses)

    # 2. activate accounts
    builder = BUILDER.Builder(secret=constant.SEED, network=constant.API_SERVER)
    sql='select private_key, public_key from private_keys where is_activated=0'
    all_accounts=[]
    rows=my_pgmanager.select(sql)
    for row in rows:
        private_key=row[0]
        public_key=row[1]
        all_accounts.append((private_key, public_key))

    # inquire blockchain to determine which public keys are to be #####activated#####
    accounts_to_be_activated=get_inactive_accounts(all_accounts, instance='public')
    # activate all the accounts by using multi ops
    if len(accounts_to_be_activated)!=0:
        try:
            sqls=[]
            iterations=int(len(accounts_to_be_activated)/100)
            for i in range(0,iterations+1):
                builder= BUILDER.Builder(secret=constant.SEED, network=constant.API_SERVER)
                accounts=accounts_to_be_activated[i*100:i*100+100]
                for account in accounts:
                    builder.append_create_account_op(destination=account, starting_balance=constant.FOTONO_STARTING_BALANCE)
                    sqls.append({'public_key': account})
                builder.sign()
                res=builder.submit()
                if dict(res).__contains__('hash'):
                    my_pgmanager.execute_many('update private_keys set is_activated=1 where public_key=%(public_key)s',
                                              sqls)
                time.sleep(10)
            # the following codes are correct:
            # for account in accounts_to_be_activated:
            #     builder.append_create_account_op(destination=account, starting_balance=constant.FOTONO_STARTING_BALANCE)
            #     sqls.append({'public_key': account})
            # builder.sign()
            # res=builder.submit()
            # if dict(res).__contains__('hash'):
            #     my_pgmanager.execute_many('update private_keys set is_activated=1 where public_key=%(public_key)s',
            #                               sqls)
        except Exception as e:
            print('Accounts creation failed\n' + e.message)
    else:
        pass

    # inquire the blockchain to determine if the account has trusted LINK issued by LINK issuer:
    sql = 'select private_key, public_key from private_keys where is_activated=1 and has_trusted=0'
    sqls=[]
    all_accounts = []
    rows = my_pgmanager.select(sql)
    for row in rows:
        private_key = row[0]
        public_key = row[1]
        all_accounts.append((private_key, public_key))
    accounts_to_do_trusting=get_untrusting_accounts(all_accounts,constant)
    # create trust using multi-threading:
    if len(accounts_to_do_trusting)!=0:
        import threading
        threads=[]
        for account in accounts_to_do_trusting:
            private_key=account[0]
            sqls.append({'public_key': account[1]})
            client=CLIENT.Client(private_key,api_server=constant.API_SERVER)
            thread = threading.Thread(target=client.trust, args=(constant.ISSUER_ADDRESS, 'LINK'))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        # my_pgmanager.execute_many('update private_keys set has_trusted=1 where public_key=%(public_key)s', sqls)
    else:
        pass

    # distribute link
    builder = BUILDER.Builder(secret=constant.DISTRIBUTOR_SEED, network=constant.API_SERVER)
    if len(users)!=0:
        for k in users:
            user = users[k]
            builder.append_payment_op(destination=user.address, amount=user.link, asset_type='LINK', asset_issuer=constant.ISSUER_ADDRESS)
        # add a memo, which specifies the timestamp when the latest order is submitted
        builder.add_text_memo(str(time.time()))
        builder.sign()
        res=builder.submit()
        # time.sleep(20)
        if res.__contains__('hash'):
            sqls=[]
            items=[]
            for k in users:
                sqls.append({'is_filled': 1, 'user_token': users[k].token})
                item = {
                    "UserToken": users[k].token,
                    "LinkAddress": users[k].address,
                    "LinkAmount": users[k].link
                }
                items.append(item)
            my_pgmanager.execute_many('update orders set is_filled=%(is_filled)s where usertoken=%(user_token)s', sqls)

            try:
                # respond to server end
                # url='http://19o60w6992.51mypc.cn/sunday/link/callback'
                url='http://weixin.jrlyl.com/sunday/link/callback'
                # items=json.dumps(items)
                # data=json.dumps({'LinkResult1':items})
                data={'LinkResult':json.dumps(items)}
                res0=requests.post(url,data)
                a=1
            except Exception as e:
                print(e)
    else:
        pass

if __name__=='__main__':
    base_time=1537455600
    t = time.time()
    while t<base_time:
        t = time.time()
        time.sleep(5)

    print('robot launched!!!\n\n')
    cnt=0
    timer=TIMER.Timer(3600,main)
    timer.run()

