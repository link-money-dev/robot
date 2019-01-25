from  wrapper import  builder as BUILDER
import CONSTANT
from wrapper import db as DB
from wrapper import operation as OPERATION

constant=CONSTANT.Constant('local')
my_pgmanager=DB.PGManager(**constant.HORIZON_DB_CONNECT_ARGS)
f=open('balances.dat','w')
# fetch all accounts and make them a dict like {id:'G...',link:...,cny:...}
accounts={}
rows=my_pgmanager.select('select * from history_accounts')
for row in rows:
    balances=[0,0]
    accounts[row[1]]=balances
# fetch 100 random transactions from history_transactions
sql='SELECT * FROM public.history_transactions'
rows=my_pgmanager.select(sql)
cnt=0
try:
    for row in rows:
        builder=BUILDER.Builder(secret='SAY5LFX5WJ7VX6HNVYLBBACGO52KJD2HN6CP3CCDKQGNMKC24A2CAHO5',network='public')
        builder.import_from_xdr(row[10])
        if len(builder.ops)==0:
            continue
        for op in builder.tx.operations:
            if isinstance(op,OPERATION.Payment):
                if op.asset.issuer is None:
                    continue
                if op.asset.code=='LINK':
                    accounts[builder.address][0]-=float(op.amount)
                    accounts[op.destination][0]+=float(op.amount)
                if op.asset.code=='CNY':
                    accounts[builder.address][1] -= float(op.amount)
                    accounts[op.destination][1] += float(op.amount)
            if isinstance(op,OPERATION.PathPayment):
                pass
        a=1
        cnt+=1
except Exception as e:
    print(e.message)
for account in accounts.keys():
    f.write(account+'\t'+ str(accounts[account][0])+'\t'+str(accounts[account][1])+'\n')
f.flush()
f.close()
a=1