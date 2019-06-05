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
    builder = BUILDER.Builder(address='GB552GC4YLN7O7Z6DDDFOO7ZPK6374H4YZGZ4YJMWQW6HBRRAWNSIIQW',
                              network='public')
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

    if True: #last_created_at_in_lyl<last_created_at_in_horizon:
        sql1="select * from history_transactions where created_at>'" + str(last_created_at_in_lyl) + "' order by created_at asc limit 100"
        rows_in_horizon=horizon_pgmanager.select(sql1)
        sqls = []
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

            try:
                builder.import_from_xdr(tx_envelope)
                if len(builder.ops) == 0:
                    continue
                for op in builder.tx.operations:
                    if isinstance(op, OPERATION.Payment):
                        if op.asset.issuer is None:
                            continue
                        if op.asset.code == 'LINK':
                            amount = float(op.amount)
                            destination = op.destination
                            source = op.source
                            if source is None:
                                source = 'None'
                            sqls.append({'transaction_hash': transaction_hash,
                                         'ledger_sequence': ledger_sequence,
                                         'account': account_id,
                                         'operation_count': operation_count,
                                         'created_at': created_at,
                                         'updated_at': updated_at,
                                         'raw_tx_envelope': tx_envelope,
                                         'raw_tx_result': result_envelope,
                                         'memo_type': memo_type,
                                         'memo': memo,
                                         'source': source,
                                         'destination': destination,
                                         'amount': amount
                                         })
                            # sql2="insert into link_transactions values('%s',%d,'%s',%d,'%s','%s','%s','%s','%s','%s','%s','%s',%d,NULL)" % \
                            #      (transaction_hash,ledger_sequence,account_id,operation_count,created_at,updated_at,tx_envelope,result_envelope,
                            #       memo_type,memo,source,destination,amount)

            except Exception as e:
                print(e.message)
                print(tx_envelope)
            a = 1
        sql2 = "insert into link_transactions values(%(transaction_hash)s," \
               "%(ledger_sequence)s,%(account)s,%(operation_count)s,%(created_at)s," \
               "%(updated_at)s,%(raw_tx_envelope)s,%(raw_tx_result)s,%(memo_type)s," \
               "%(memo)s,%(source)s,%(destination)s,%(amount)s,NULL)"
        lyl_pgmanager.execute_many(sql2, sqls)
        a = 1
# if last created record in lyl is less than that in horizon, do the following jobs:
from wrapper import timer as TIMER
timer=TIMER.Timer(60,sync_db)
timer.run()

