from  wrapper import  builder as BUILDER
import CONSTANT
from wrapper import db as DB
from wrapper import operation as OPERATION

constant=CONSTANT.Constant('local')
my_pgmanager=DB.PGManager(**constant.HORIZON_DB_CONNECT_ARGS)
f=open('trades.dat','w')
# fetch all accounts and make them a dict like {id:'G...',link:...,cny:...}
accounts={}
accounts_id={}

rows=my_pgmanager.select('select * from history_accounts')
for row in rows:
    balances=[0,0]
    accounts[row[1]]=balances
    accounts_id[row[0]]=row[1]

# fetch 100 random transactions from history_transactions
sql='SELECT * FROM public.history_trades order by ledger_closed_at'
rows=my_pgmanager.select(sql)
cnt=0
try:
    for row in rows:
        base_account=accounts_id[row[4]]
        counter_account=accounts_id[row[7]]
        base_amount=float(row[6])/10000000
        counter_amount=float(row[9])/10000000

        accounts[base_account][0]-=base_amount
        accounts[base_account][1]+=counter_amount

        accounts[counter_account][0]+=base_amount
        accounts[counter_account][1]-=counter_amount

        cnt+=1
except Exception as e:
    print(e.message)
for account in accounts.keys():
    f.write(account+'\t'+ str(accounts[account][0])+'\t'+str(accounts[account][1])+'\n')
f.flush()
f.close()
a=1