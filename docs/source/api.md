## API参考文档  
本部分文档用于记录开发过程中的API设计以及使用方法。   
*** 
**目录**  
- [API参考文档](#api参考文档)
  - [用户账号部分](#用户账号部分)
    - [login](#login)
    - [login\_with\_verify\_code](#login_with_verify_code)
    - [logout](#logout)
    - [register](#register)
    - [retrieve](#retrieve)
    - [send\_email](#send_email)
    - [send\_message](#send_message)
    - [verify\_code](#verify_code)
    - [verify\_email](#verify_email)
  - [数据集部分](#数据集部分)
  - [排行榜部分](#排行榜部分)
  - [模型测试部分](#模型测试部分)
***
### 用户账号部分  
#### login  
**请求方式**：POST  
**请求URL**：`/user/login`  
**请求参数**：字符串username，字符串password  
**返回情况**：  
* 正常返回  
```python
{
    "jwt": "jwt字符串",
    "userId": "用户id",
    "username": "用户名",
    "message": "ok"
}, status=200
```
* 参数异常  
```python
{
    "message": "Invalid credentials"
}, status=401
```
#### login_with_verify_code  
**请求方式**：POST  
**请求URL**：`/user/login_with_verify_code`  
**请求参数**：字符串mobile，字符串verify_code  
**返回情况**：  
* 正常返回  
```python
{
    "jwt": "jwt字符串",
    "userId": "用户id",
    "username": "用户名",
    "message": "ok"
}, status=200
```
* 验证码异常  
```python
{
    "message": "Invalid code"
}, status=401
```
* 其余参数异常  
```python
{
    "message": "Invalid credentials"
}, status=401
```
#### logout  
**请求方式**：POST  
**请求URL**：`/user/logout`  
**请求参数**：jwt  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
}, status=200
```
* 未登录  
```python
{
    "message": "User must be authorized."
}, status=401
```
#### register  
**请求方式**：POST  
**请求URL**：`/user/register`  
**请求参数**：字符串username，字符串password，字符串mobile，可选字符串email  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
}, status=201
```
* 参数异常  
```python
{
    "message": #根据参数错误情况而定
}, status=400
```
#### retrieve  
**请求方式**：GET  
**请求URL**：`/user/retrieve/<id>`  
**请求参数**：无  
**返回情况**：
* 正常返回  
```python
{
    "username": "用户名",
    "mobile": "手机号",
    ...(略)
}, status=200
```
* 未找到用户  
```python
{
    "detail": "未找到。"
}, status=404
```
#### send_email  
**请求方式**：POST  
**请求URL**：`/user/send_email`  
**请求参数**：字符串email  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
}, status=201
```
* 参数异常  
```python
{
    "message": #根据参数错误情况而定
}, status=401
```
#### send_message  
**请求方式**：POST  
**请求URL**：`/user/send_message`  
**请求参数**：字符串mobile  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
}, status=201
```  
* 参数异常  
```python
{
    "message": #根据参数错误情况而定
}, status=401
```
**特殊说明**：实际发送功能暂未实现  
#### verify_code  
**请求方式**：POST  
**请求URL**：`/user/verify_code`  
**请求参数**：字符串mobile，字符串verify_code
**返回情况**：  
* 正常返回   
```python
{
    "message": "ok"
}, status=200
```
* 验证码错误    
```python
{
    "message": "Invalid code"
}, status=401
```
#### verify_email  
**请求方式**：POST  
**请求URL**：`/user/verify_email`  
**请求参数**：字符串email，字符串verify_code  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
}, status=200
```
* 验证码错误  
```python
{
    "message": "Invalid code"
}, status=401
```
***
### 数据集部分  
***
### 排行榜部分  
***
### 模型测试部分  
