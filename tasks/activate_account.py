import CONSTANT
from wrapper.client import Client

accounts_to_be_activated=[
'SDJPAJAY223ECKE5UMLFA66XW6L7S53TNYAPEB5SSHKG2LVL27MHJC7O',
'SBFWXCCQ6ETYKNDPHSSOPXSQGC6X6NVQXU5AAJPRMJ2U4PZHFYS2TRDI',
'SCPRQM72Z5FLLEPG2EMS2IXHS3NLC4BGUFS5PQZN2C5S2KSXT2GMVQCV'
]

accounts_to_be_activated=[
'GAMEJK4T45MLQ5QJKOYHLW3EQNSOQVPDLVMNLJFG4Z53WJGUZI7FSWOI',
'GAMEXYMNGLDLG6HBXAGSKIN5GYYE2J6CB3Q376HW5BMECY62POVSTCZQ',
'GAMEORZL3JSAZVQQQALN3QBLSYWLLRGPTMV7BJDB2IMGPATWPX4QBUWM',
'GAMEYMSJFIZAI5J6TVFTVCXG2M25I6FXNG7HJNRCYXCZ27K7EO7ADMRI',
'GAMEBQD3ZA27LTKTSPLNPV3VVHMPF3QG6NE5S3NIQ5G37RI3O7UFELEU',
'GAME7LKT5STOP5RO35NHA7APWGHECKDB4477HMPBWZW5OFZRSZOZ7YD6'

]
constant=CONSTANT.Constant('public')
client=Client(private_key='SDQ43Z762OW6L7YBCRBNB2LL57YADNHARB2AW4RE45RSKM7PWRTT76PT',api_server=constant.API_SERVER)
# ..UAA
client.fund(destination='GBS4KOHWXJEN52BH4AHUMHHRNK23CJJLQBB7J3M6FK6QABCKLKBTYWPB',amount=1000)
