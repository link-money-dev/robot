import key_generation
from wrapper import keypair as KEYPAIR

cnt=0
while True:
    k=KEYPAIR.Keypair.random()
    address=k.address()
    seed=k.seed()
    if address[0:3]=='GFX':

        print(address)
        print(seed)
        print
        cnt+=1
        if cnt>5:
            break

