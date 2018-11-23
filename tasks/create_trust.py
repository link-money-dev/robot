from wrapper import client as CLIENT
import CONSTANT

constant=CONSTANT.Constant('public')
client=CLIENT.Client(private_key='SACLPILFUDZ2FDATFEAEOSF6TRICUCYZZZ72FOEOKHXSNQIEUBDEO7AH',api_server=constant.API_SERVER)
client.trust(issuer_address='GCNYF4V6CUY2XENJGRHLNB3AQE3RZIOWYHUN6YU5T34N3ZSK4KGCB7DD',asset_code='CNY',limit=1000000)
client.trust(issuer_address=constant.ISSUER_ADDRESS,asset_code='LINK',limit=1000000)