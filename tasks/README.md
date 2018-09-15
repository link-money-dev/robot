
# 查询账户的API    

## 请求交互    

REST访问的根URL：
- 主网：
- 测试网：'https://116.62.226.231:12346'

请求交互说明
- 请求参数：根据接口请求参数规定进行参数封装。
- 提交请求参数：将封装好的请求参数通过 POST 或 GET 方式提交至服务器。
- 服务器响应：服务器首先对用户请求数据进行参数安全校验，通过校验后根据业务逻辑将响应数据以JSON格式返回给用户。
- 数据处理：对服务器响应数据进行处理。

## API参考

## 一、查询账户联金余额 API

获取指定账户的联金余额

## 1. Get link/api/call/run/balance/{LinkAddress}    获取指定账户的联金数量

URL `https://116.62.226.231:12346/link/api/call/run/balance`
其中{LinkAddress}是账户的地址
示例:

```
# Request

GET：

https://116.62.226.231:12346/link/api/call/run/balance?LinkAddress=GCHZDZXYLZ76XADS7735LK3OJUFZ2TBSXAR23YXKXCXXHUEEVT5C37PY

```
### 如果查询成功，那么：
```
# Response

{
    "Message": "Successful",
    "Code": 1,
    "Result": {
        "LinkAmount": 9300098.1781
    }
}
```

返回值说明

- "Message": 提示信息
- "Message"键的值包含以下四种可能：
    - "Successful": 成功
    - "Account is invalid": 入参即账户地址的格式错误
    - "Account does not exist": 账户地址不存在于数据库中
    - "Error": 可能是服务器端代码有问题
- "Code": 1表示成功，0表示失败
- "Result": 是一个对象
- "Result"对象的"LinkAmount"是一个数值，表示联金的数量，在任何查询不成功的情况下，该值都为0




请求参数

|参数名|	参数类型|	必填|	描述|
| :-----    | :-----   | :-----    | :-----   |
|LinkAddress|String|是|账户的地址|




## 二、发送交易金额 API

发送交易金额

## 1. Post link/api/call/run/order    发送订单到联金的服务端

URL `https://116.62.226.231:12346/link/api/call/run/orders`

示例:

```
# Request

POST：

https://116.62.226.231:12346/link/api/call/run/orders
```
### 如果查询成功，那么：
```
# Response

{
    "Message": "Successful",
    "Code": 1,
    "Result": {
        "LinkAmount": 9300098.1781
    }
}
```

返回值说明

- "Message": 提示信息
- "Message"键的值包含以下四种可能：
    - "Successful": 成功
    - "Unsuccessful": 失败
    - "Error": 可能是服务器端代码有问题
- "Code": 1表示成功，0表示失败
- "Result": None





请求参数

|参数名|	参数类型|	必填|	描述|
| :-----    | :-----   | :-----    | :-----   |
|OrderNo|String|是|订单号码，必须唯一|
|UserToken|String|是|用户标识|
|OrderAmount|Decimal|是|订单金额|
