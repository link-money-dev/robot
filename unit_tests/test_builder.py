import unittest
from wrapper import builder as BUILDER
from wrapper import keypair as KEYPAIR
import requests
import CONSTANT


class TestBuilder(unittest.TestCase):
    # def test_init(self):
    #     '''
    #
    #     :return:
    #     '''
    #
    #     pass

    def test_append_create_account_op(self):
        '''
        this test should test against append_create_account_op with 3 different network environments

        :param destination:
        :param starting_balance:
        :param source:
        :return:
        '''
        constants=[
            CONSTANT.Constant('local'),
            CONSTANT.Constant('public'),
        ]
        builders=[]

        # fund a non-existing account, should return true:
        for constant in constants:
            builder=BUILDER.Builder(secret=constant.SEED,  network=constant.API_SERVER)
            random_account=KEYPAIR.Keypair.random()
            random_address=random_account.address().decode()
            builder.append_create_account_op(destination=random_address,starting_balance=100)
            builder.sign()
            builder.submit()
            # inquire the blockchain and the destination should have a balance of 100
            res=requests.get(constant.HORIZON_BASE_URL+'/accounts/'+random_address).text
            import json
            res=dict(json.loads(res))
            balance=res.get('balances',list())[0]['balance']
            self.assertAlmostEqual(float(balance),100,delta=0.01)
            a=1
