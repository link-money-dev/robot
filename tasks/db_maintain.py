# coding: utf-8
# this program transalates horizon:history_transactions into lyl_orders:raw_transactions and link_transactions
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from  wrapper import  builder as BUILDER
import CONSTANT
from wrapper import db as DB
from wrapper import operation as OPERATION
import time
import datetime

def sync_db():
    constant = CONSTANT.Constant('public')
    horizon_pgmanager = DB.PGManager(**constant.HORIZON_DB_CONNECT_ARGS)
    lyl_pgmanager = DB.PGManager(**constant.DB_CONNECT_ARGS)

    # 0. select max(created_at) from horizon:history_transactions, and set it to last_updated_time
    sql = 'select max(created_at) from history_transactions'
    rows = horizon_pgmanager.select(sql)
    last_created_at_in_horizon = rows[0][0]

    # 1. select max(created_at) from lyl_orders:link_transactions
    sql = 'select max(created_at) from link_transactions'
    rows = lyl_pgmanager.select(sql)
    if rows[0][0] is None:
        last_created_at_in_lyl = t = datetime.datetime(2017, 3, 22, 16, 9, 33, 494248)
    else:
        last_created_at_in_lyl = rows[0][0]

    if 0==0: #last_created_at_in_lyl<last_created_at_in_horizon:
        sql1="select * from history_transactions where created_at>'" + str(last_created_at_in_lyl) + "' order by created_at asc"
        rows_in_horizon=horizon_pgmanager.select(sql1)
        for row in rows_in_horizon:
            transaction_hash=row[0]
            ledger_sequence=row[1]
            account_id=row[3]
            operation_count=row[6]
            created_at=row[7]
            updated_at=row[8]
            id='None'
            tx_envelope=row[10]
            result_envelope=row[11]
            memo_type=row[15]
            memo=row[16]

            # parse tx_envelope and result_envelope
            builder = BUILDER.Builder(secret='SAY5LFX5WJ7VX6HNVYLBBACGO52KJD2HN6CP3CCDKQGNMKC24A2CAHO5',
                                      network='public')
            builder.import_from_xdr(tx_envelope)
            if len(builder.ops) == 0:
                continue
            for op in builder.tx.operations:
                if isinstance(op, OPERATION.Payment):
                    if op.asset.issuer is None:
                        continue
                    if op.asset.code == 'LINK':
                        amount= float(op.amount)
                        destination=op.destination
                        source=op.source
                        if source is None:
                            source='None'
                        sql2="insert into link_transactions values('%s',%d,'%s',%d,'%s','%s','%s','%s','%s','%s','%s','%s',%d,NULL)" % \
                             (transaction_hash,ledger_sequence,account_id,operation_count,created_at,updated_at,tx_envelope,result_envelope,
                              memo_type,memo,source,destination,amount)
                        lyl_pgmanager.execute(sql2)
                        a=1
            a = 1
# if last created record in lyl is less than that in horizon, do the following jobs:
from wrapper import timer as TIMER
timer=TIMER.Timer(5,sync_db)
timer.run()

