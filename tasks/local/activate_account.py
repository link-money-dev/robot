import CONSTANT
from wrapper.client import Client
from wrapper import builder as BUILDER
from wrapper import db as DB

# fixtures
client1=Client(private_key='SDQREYINW3OPRIKX5J6PSU3ZWEVRYPNJGMEAZFQ2CLQMUGDZUGUP4AX2')
client2=Client(private_key='SDTH3244ZJLICKJUNGOS3W3GS3GVPCOE24XS76FZSRAWFRWMBJH6S73N')
client3=Client(private_key='SDWDDZ7ALH27JHCZ22GFVFBGC3J7IPZJZXMAABP6AWBILYPGIDA5TH2P')
clients=[client1,client2,client3]

constant=CONSTANT.Constant('local')
master=Client(private_key='SDS4FTMCD55TNALNKNAMMZ6DF24STEMJSBZ66OPSY7WXZ7FUT4G2NRTB',api_server=constant.API_SERVER)
for cli in clients:
    master.fund(destination=cli.address,amount=200)
