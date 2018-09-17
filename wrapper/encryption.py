#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import random
from binascii import b2a_hex, a2b_hex
from Crypto.Cipher import AES


def generate_random_key_pair(lenth=16):
    raw=list('`1234567890-=][poiuytrewqasdfghjkl;.,mnbvcxz~!@#$%^&*()_+}{POIUYTREWQASDFGHJKL:"?><MNBVCXZ')
    nums=list('0123456789')
    lenth_raw = len(raw)
    iv=[]
    result=[]
    for i in range(lenth):
        postion_raw=random.randint(0,lenth_raw-1)
        postion_iv=random.randint(0,9)
        result.append(raw[postion_raw])
        iv.append(nums[postion_iv])
    key="".join(result)
    iv="".join(iv)
    return (key,iv)

class Prpcrypt():
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.mode = AES.MODE_CBC
        self.BS = AES.block_size
        # 补位
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    def encrypt(self, text):
        text = self.pad(text)
        cryptor = AES.new(self.key, self.mode, self.iv)
        # 目前AES-128 足够目前使用
        ciphertext = cryptor.encrypt(text)
        # 把加密后的字符串转化为16进制字符串
        return b2a_hex(ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return self.unpad(plain_text.rstrip('\0'))

#
if __name__ == '__main__':
    key,iv=('VDg0?Uk=`-a_!q!2','3384960057786404')
    pc = Prpcrypt(key, iv)  # 初始化密钥 和 iv

    e = pc.encrypt('SDQ43Z762OW6L7YBCRBNB2LL57YADNHARB2AW4RE45RSKM7PWRTT76PT')  # 加密
    # assert e=='e79b53d0ddb86c5892d5394111baf101f26635fac3ec20e7d7bcbd493c78998a3bf100a98604a6d20eb487fe68c89f2a0cfaa89fb3bbda60cec8a97fc0669d9a'
    e='7cf51b0a17b1b4f65bedf437654a65272a95eacf0dc93d994d8244b579a529a54d4c7608a96f30f22baf9f227feaec9c18895ce75f8c760018eda9affffcfabf'
    d = pc.decrypt(e)  # 解密
    print "加密:", e
    print "解密:", d
    print "长度:", len(d)
