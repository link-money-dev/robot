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

# CONSTANTS:
UNIXTIMEZERO = datetime.datetime(1970, 1, 1)
builder = BUILDER.Builder(address='GB552GC4YLN7O7Z6DDDFOO7ZPK6374H4YZGZ4YJMWQW6HBRRAWNSIIQW',
                          network='public')
constant = CONSTANT.Constant('public')
horizon_pgmanager = DB.PGManager(**constant.HORIZON_DB_CONNECT_ARGS)
lyl_pgmanager = DB.PGManager(**CONSTANT.DB_CONNECT_ARGS_LOCAL)


def sync_db():
    try:

        # 0. select max(ledger_sequence) from horizon:history_transactions, and set it to ledger_sequence
        sql = 'select max(ledger_sequence) from history_transactions'
        rows = horizon_pgmanager.select(sql)
        max_ledger_sequence_in_horizon = rows[0][0]

        # 1. select max(ledger_sequence) from lyl_orders:messages
        sql = 'select max(ledger_sequence) from messages'
        rows = lyl_pgmanager.select(sql)
        if rows[0][0] is None:
            max_ledger_sequence_in_lyl = 0
        else:
            max_ledger_sequence_in_lyl = rows[0][0]

        # please comment the following line in product mode:
        # max_ledger_sequence_in_lyl=2600255-100

        if max_ledger_sequence_in_lyl<max_ledger_sequence_in_horizon:
            sql1="select * from history_transactions where ledger_sequence>'" + str(max_ledger_sequence_in_lyl) + "' order by ledger_sequence asc"
            rows_in_horizon=horizon_pgmanager.select(sql1)
            sqls = []
            for row in rows_in_horizon:
                transaction_hash=row[0]
                ledger_sequence=row[1]
                account_id=row[3]
                created_at=row[7]
                tx_envelope=row[10]
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
                            if op.asset.code == 'FX' and op.asset.issuer=='GCNYF4V6CUY2XENJGRHLNB3AQE3RZIOWYHUN6YU5T34N3ZSK4KGCB7DD':
                                if memo is None:
                                    continue
                                amount = float(op.amount)
                                destination = op.destination
                                source = op.source
                                if source is None:
                                    source = 'None'

                                sqls.append({'transaction_hash': transaction_hash,
                                             'ledger_sequence': ledger_sequence,
                                             'account': account_id,
                                             'created_at': int((created_at-UNIXTIMEZERO).total_seconds()),
                                             'memo_text': memo,
                                             'source': source,
                                             'destination': destination,
                                             'amount': amount,
                                             'has_read':0
                                             })

                                break_point=1
                except Exception as e:
                    print(e.message)
                a = 1
            sql2 = "insert into messages (transaction_hash,ledger_sequence,account,created_at,memo_text,amount,has_read,source,destination) values(%(transaction_hash)s," \
                   "%(ledger_sequence)s,%(account)s,%(created_at)s," \
                   "%(memo_text)s,%(amount)s,0,%(source)s,%(destination)s)"
            lyl_pgmanager.execute_many(sql2, sqls)
            a = 1
    except Exception as e:
        print(e.message)

# run schedually:
# if last created record in lyl is less than that in horizon, do the following jobs:
from wrapper import timer as TIMER
timer=TIMER.Timer(5,sync_db)
timer.run()

# run at once
# sync_db()

