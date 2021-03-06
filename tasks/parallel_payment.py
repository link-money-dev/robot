# -*- coding: UTF-8 -*-

# 本程序并行发币，需要知道发币账户的私钥列表和目标账户的地址
# 因为区块链的自身特性，每个私钥在每时间间隔（典型值5s）内只能提交一次交易（transaction），所以，为了达到一个理想的速度，最好使用多个账户同时发币
# 本程序从自己启动，外部只能调用其方法
# 本程序的主入口程序为 main()

# 请填写下面几个参数：
# 第一个参数为生成的密钥对的数量
NUMBER=1000
# 第二个参数为AES加密类实例的key，必须为16位ascii字符，必须由 第一人 妥善保存
KEY='a'*16
# 第三个参数为AES加密类实例的iv，必须为16为数字，必须由 第二人 妥善保存
IV='1'*16
# 并发度，默认为单线程，单线程快38%
CONCURRENCY=1