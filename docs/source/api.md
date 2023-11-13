## API参考文档  
本部分文档用于记录开发过程中的API设计以及使用方法。   
所有API的url均可以使用OPTIONS进行访问，会返回CORS相关信息，以支持Vue.js的跨域访问，下面不再说明。  
文档中的返回参数中，带有大括号`{}`的部分为确定的data键值对内容，未带有该部分说明该api返回的data可能因情况而异（如参数格式错误说明等），不应作为绝对的判定标准。  
有关额外需求的说明参见文章末尾额外需求部分。  
*** 
**目录**  
- [API参考文档](#api参考文档)
  - [用户账号部分](#用户账号部分)
    - [delete](#delete)
    - [login](#login)
    - [login\_with\_verify\_code](#login_with_verify_code)
    - [logout](#logout)
    - [register](#register)
    - [retrieve](#retrieve)
    - [send\_email](#send_email)
    - [send\_message](#send_message)
    - [update](#update)
    - [update\_avatar](#update_avatar)
    - [verify\_code](#verify_code)
    - [verify\_email](#verify_email)
  - [数据集部分](#数据集部分)
    - [create](#create)
    - [upload](#upload)
  - [排行榜部分](#排行榜部分)
  - [模型测试部分](#模型测试部分)
  - [额外需求](#额外需求)
    - [jwt](#jwt)
***
### 用户账号部分  
#### delete  
**请求方式**：POST  
**请求URL**：`/user/delete/<id>`  
**请求参数**：无  
**额外需求**：jwt  
**返回情况**：  
* 正常返回   
```python
{
    "message": "ok"
}, 
status=200
```
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
}, 
status=200
```
* 参数异常  
```python
{
    "message": "Invalid credentials"
}, 
status=401
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
}, 
status=200
```
* 验证码异常  
```python
{
    "message": "Invalid code"
}, 
status=401
```
* 其余参数异常  
```python
{
    "message": "Invalid credentials"
}, 
status=401
```
#### logout  
**请求方式**：POST  
**请求URL**：`/user/logout`  
**请求参数**：无    
**额外需求**：jwt  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
}, 
status=200
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
}, 
status=201
```
* 参数异常  
```python
status=400
```
#### retrieve  
**请求方式**：GET  
**请求URL**：`/user/retrieve/<id>`  
**请求参数**：无  
**额外需求**：jwt  
**返回情况**：
* 正常返回  
```python
{
    "message": "ok",
    "username": "用户名",
    "password": "********",
    "mobile": "手机号",
    ...(略)
}, 
status=200
```
* 未找到用户  
```python
status=404
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
}, 
status=201
```
* 参数异常  
```python
status=401
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
}, 
status=201
```  
* 参数异常  
```python
status=401
```
#### update  
**请求方式**：PUT/PATCH  
**请求URL**：`/user/update/<id>`  
**请求参数**：使用PUT时为字符串username，字符串password，字符串mobile，可选字符串email；使用PATCH时字段均为可选  
**额外需求**：jwt  
**返回情况**：
* 正常返回  
```python
{
    "message": "ok"
    "username": "用户名",
    "password": "********",
    "mobile": "手机号",
    # ...(略)
}, 
status=200
```
* 未找到用户  
```python
status=404
```
#### update_avatar  
**请求方式**：POST  
**请求URL**：`/user/update_avatar/<id>`  
**请求参数**：文件avatar  
**额外需求**：jwt  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
}, 
status=200
```
* 未找到用户  
```python
status=404
```
#### verify_code  
**请求方式**：POST  
**请求URL**：`/user/verify_code`  
**请求参数**：字符串mobile，字符串verify_code
**返回情况**：  
* 正常返回   
```python
{
    "message": "ok"
}, 
status=200
```
* 验证码错误    
```python
{
    "message": "Invalid code"
}, 
status=401
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
}, 
status=200
```
* 验证码错误  
```python
{
    "message": "Invalid code"
}, 
status=401
```
***
### 数据集部分  
#### create  
**请求方式**：POST  
**请求URL**：`/dataset/create`  
**请求参数**：字符串name  
**额外需求**：jwt  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "datasetId": "数据集id"
},
status=201
```
* 参数异常  
```python
status=400
```
#### upload  
**请求方式**：POST  
**请求URL**：`/dataset/upload`  
**请求参数**：文件file，字符串datasetId  
**额外需求**：jwt  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "datasetId": "数据集id"
},
status=200
```
* 参数异常  
```python
status=400
```
***
### 排行榜部分  
***
### 模型测试部分  
***
### 额外需求  
此部分专门论述上述api中的额外需求要求明细。  
#### jwt  
jwt是一种用于身份验证的token，用于验证用户身份。大部分需要身份验证的api均需要提供jwt作为身份验证。  
**获取方式**：在用户正确登录后会获得jwt，其中压缩包含了用户的id。  
**返回情况**：  
在所有需要jwt的接口中，如果jwt错误，会返回如下信息：  
```python
{
    "message": "User must be authorized."
},
status=401
```
