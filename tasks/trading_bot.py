from wrapper import client as CLIENT
import CONSTANT
constant=CONSTANT.Constant('public')

robot1=CLIENT.Client("", api_server=constant.API_SERVER)
robot2=CLIENT.Client("", api_server=constant.API_SERVER)