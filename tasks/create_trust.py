from wrapper import client as CLIENT
from wrapper import db as DB
import CONSTANT

constant=CONSTANT.Constant('public')
my_pgmanager=DB.PGManager(**constant.DB_CONNECT_ARGS)


# example for 1 client to trust an asset
# client=CLIENT.Client(private_key='SACLPILFUDZ2FDATFEAEOSF6TRICUCYZZZ72FOEOKHXSNQIEUBDEO7AH',api_server=constant.API_SERVER)
# client.trust(issuer_address='GCNYF4V6CUY2XENJGRHLNB3AQE3RZIOWYHUN6YU5T34N3ZSK4KGCB7DD',asset_code='CNY',limit=1000000)
# client.trust(issuer_address=constant.ISSUER_ADDRESS,asset_code='LINK',limit=1000000)

# example for multiple clients to trust an asset
def mutil_trust(accounts_to_do_trusting):
    import threading
    threads = []
    for account in accounts_to_do_trusting:
        private_key = account[0]
        client = CLIENT.Client(private_key, api_server=constant.API_SERVER)
        thread = threading.Thread(target=client.trust, args=(constant.ISSUER_ADDRESS, 'LINK'))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('trusting successfully')

accounts=[]
sql='select private_key,public_key from private_keys'
accounts=my_pgmanager.select(sql)

for i in range(0,len(accounts)/5+1):
    accounts_to_do_trusting_in_this_loop=accounts[i*5:i*5+5]
    mutil_trust(accounts_to_do_trusting_in_this_loop)