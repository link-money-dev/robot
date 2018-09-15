# -*- coding: UTF-8 -*-
import sys
sys.path.append("..")
from wrapper import db as DB
from tasks import key_generation
from wrapper import user as USER
import CONSTANT


def get_users_and_total_expenses(t, interval=3600):
    # dt = '2018-01-01 10:40:30'
    # ts = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")))
    my_pgmanager = DB.PGManager(**CONSTANT.DB_CONNECT_ARGS_TEST)
    horizon_pgmanager = DB.PGManager(**CONSTANT.DB_CONNECT_ARGS_HORIZON_TEST)
    datetime_upperbound = t
    datetime_lowerbound = datetime_upperbound-interval
    sql='select * from orders where created_at<' + str(datetime_upperbound) + ' and is_filled=0'
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
        expense = row[2]
        if not users.__contains__(token):
            sql = 'select * from private_keys where user_token=\'' + token + '\''
            rs = my_pgmanager.select(sql)
            if len(rs) == 0:
                key='0'*16
                iv='0'*16
                keypair = key_generation.generate_keypairs(1, key, iv, False)[0]
                sql = 'insert into private_keys(user_token,private_key,public_key, is_activated) values(\'%s\',\'%s\',\'%s\',0)' % (
                token, keypair[0], keypair[1])
                my_pgmanager.execute(sql)
                user = USER.User(token, expense, keypair[0], keypair[1], 0)
            else:
                keypair = (rs[0][3], rs[0][2])
                is_activated = rs[0][6]
                user = USER.User(token, expense, keypair[0], keypair[1], 1)
            users[token] = user
        else:
            users[token].add_expense(expense)
        total_expenses += expense
    result=(users,total_expenses)
    return result