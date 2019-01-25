# -*- coding: UTF-8 -*-
from  wrapper import  builder as BUILDER
from  wrapper import client as CLIENT
import CONSTANT
from wrapper import db as DB
from wrapper import operation as OPERATION
import requests
import json
import time
from wrapper import db as DB

def get_all_payments(account_id, interval=3600):
    this_url = ''
    now=time.time()
    # account_id = 'GCNY2H4OAQNSVG2WUQ5EGABFLEG2GXF3OZZVJCQB7N2KCIGWVTY6WTHB'
    base_url = 'http://47.75.115.19:8888/accounts/' + account_id + '/payments/'
    base_url = base_url + '?limit=10&order=desc'

    records = []
    records_from_requests=None
    this_url = base_url

    exit_flag=False
    while records_from_requests != []:
        res = requests.get(this_url)
        records_from_requests = json.loads(res.text)['_embedded']['records']
        for record in records_from_requests:
            t=int(time.mktime(time.strptime(record['created_at'], '%Y-%m-%dT%H:%M:%SZ')))+3600*8
            if t>now-interval:
                records.append(record)
            else:
                exit_flag=True
                break
        if exit_flag==True:
            break
        this_url = json.loads(res.text)['_links']['next']['href']

    return records

def find_max_coin_sender(records):
    senders = {}
    for record in records:
        asset_issuer = record.get('asset_issuer', 'fotono.org')
        asset_code = record.get('asset_code', 'ftn')
        if asset_code == 'CNY' and asset_issuer == 'GCNYF4V6CUY2XENJGRHLNB3AQE3RZIOWYHUN6YU5T34N3ZSK4KGCB7DD':
            sender = record['from']
            if senders.has_key(sender):
                senders[sender] += float(record['amount'])
            else:
                senders[sender] = float(record['amount'])

    max_coin_sender = None
    max_coin_sent = 0
    for sender in senders.keys():
        if senders[sender] > max_coin_sent:
            max_coin_sent = senders[sender]
            max_coin_sender = sender
    return max_coin_sender

def sort(records, num=10):
    senders={}
    for record in records:
        asset_issuer = record.get('asset_issuer', 'fotono.org')
        asset_code = record.get('asset_code', 'ftn')
        if asset_code == 'CNY' and asset_issuer == 'GCNYF4V6CUY2XENJGRHLNB3AQE3RZIOWYHUN6YU5T34N3ZSK4KGCB7DD':
            sender = record['from']
            if senders.has_key(sender):
                senders[sender] += float(record['amount'])
            else:
                senders[sender] = float(record['amount'])

    senders=sorted(senders.items(),key=lambda d:d[1],reverse=True)
    return senders[:num]

def get_all_payments_of_a_sender(sender,records):
    all_payments = []
    for record in records:
        asset_code = record.get('asset_code', 'ftn')
        asset_issuer = record.get('asset_issuer', 'fotono.org')
        if asset_code == 'CNY' and asset_issuer == 'GCNYF4V6CUY2XENJGRHLNB3AQE3RZIOWYHUN6YU5T34N3ZSK4KGCB7DD':
            if record['from'] == sender:
                all_payments.append(record)
    return all_payments

def get_all_memos_from_payments(payments):
    all_memos = []

    for payment in payments:
        this_url = payment['_links']['transaction']['href']
        res = requests.get(this_url).text
        res = json.loads(res)
        memo = res.get('memo', '')
        all_memos.append(memo)
    return all_memos

def filter_memos(memos):
    result=[]
    for memo in memos:
        if memo[1]=='>' and memo[:1].isdigit():
            result.append(memo)
    result.sort()
    return result

def concatenate_memos(memos):
    result=''
    memos.sort()
    for memo in memos:
        result+=memo[2:]
    return result


text=''
def main():
    global text
    # 1. collect all payments paid to account:XXX within last 1 hour
    # using http request
    records = get_all_payments('GALLDNSLZWOHUBXFGTPM7BHVVBNJK7RBNPNAN4GZQBLIMGBIVGO7H52Z', 86400)

    # 2. fetch top 10 senders who sent the most fee
    senders = sort(records, 10)
    # max_coin_sender = find_max_coin_sender(records)

    adds=[]
    # fetch top 10 senders who spent the most
    for sender in senders:
        # 3. re-format the text the sender has sent
        # 3.1 extract all payments of max coin send
        all_payments = get_all_payments_of_a_sender(sender[0], records)

        # 3.2 get all corresponding transactions of the payments:
        all_memos = get_all_memos_from_payments(all_payments)
        # 3.3 filter memos that only format compatible are OK
        memos = filter_memos(all_memos)
        text=concatenate_memos(memos)
        addresser=sender[0]
        fee=sender[1]
        if text!='':
            add={'addresser':addresser,'fee':fee,'text':text}
            # insert in to database
            my_pgmanager=DB.PGManager(**CONSTANT.DB_CONNECT_ARGS_PUBLIC)
            t=time.time()
            sql = 'insert into messages(created_at,text,addresser, fee) values(%d,\'%s\',\'%s\',\'%s\')' % (
                t, text, addresser,str(fee))
            my_pgmanager.execute(sql)
            adds.append(add)
    print('done')
    # _text = concatenate_memos(memos)
    # if _text!='':
    #     text=_text
    # print(text)

from tools import timer as TIMER
# loop: every one hour do a loop:
timer=TIMER.Timer(6000,main)
timer.run()

a=1