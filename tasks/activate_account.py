import CONSTANT
from wrapper.client import Client
from wrapper import builder as BUILDER
from wrapper import db as DB

# import public keys:
f=open('accounts.dat','r')
lines=f.readlines()
accounts=[]
for line in lines:
    accounts.append(line[:56])

constant=CONSTANT.Constant('public')
client=Client(private_key='SDQ43Z762OW6L7YBCRBNB2LL57YADNHARB2AW4RE45RSKM7PWRTT76PT',api_server=constant.API_SERVER)
# client.fund('GAX5PIR4Q75XQKZLLARXFPBIZW5XBVZHG7ILBUC6ZE5SSBQZKIUWIVDU',amount=200)
client.fund('GD4OYE7L66MWK7TKK4OYLSPRHIIHERXKOOYSCEOFJK26AQWBUMLI3VGM',amount=200)
# ..UAA

my_pgmanager=DB.PGManager(**constant.DB_CONNECT_ARGS)

rows=my_pgmanager.select('select public_key from private_keys')
for row in rows:
    address=row[0]
    if (address in accounts)==False:
        print(address+ str(client.fund(address,200)))

for i in range(32,len(accounts)/100+1):
    accounts_to_be_activated=accounts[i*100:i*100+100]
    builder = BUILDER.Builder(secret='SDQ43Z762OW6L7YBCRBNB2LL57YADNHARB2AW4RE45RSKM7PWRTT76PT',
                              network=constant.API_SERVER)
    for account in accounts_to_be_activated:
        builder.append_create_account_op(destination=account,starting_balance=200)
    builder.sign()
    builder.submit()

