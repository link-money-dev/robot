# -*- coding: UTF-8 -*-
import sys
sys.path.append("..")
from wrapper import db as DB
import CONSTANT

constant=CONSTANT.Constant('test')
my_pgmanager=DB.PGManager(**constant.DB_CONNECT_ARGS)

def create_table():

    pass
# my_pgmanager=DB.PGManager(**CONSTANT.DB_CONNECT_ARGS_TEST)
