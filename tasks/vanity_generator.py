import key_generation
from wrapper import keypair as KEYPAIR

cnt=0
while True:
    k=KEYPAIR.Keypair.random()
    address=k.address()
    seed=k.seed()
    a=address[-3:]
    if address[0:4]=='GBTC':

        print(address)
        print(seed)
        print


