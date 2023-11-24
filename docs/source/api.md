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
    - [list\_subscription](#list_subscription)
    - [login](#login)
    - [login\_with\_verify\_code](#login_with_verify_code)
    - [logout](#logout)
    - [register](#register)
    - [retrieve](#retrieve)
    - [retrieve\_password](#retrieve_password)
    - [send\_email](#send_email)
    - [send\_message](#send_message)
    - [subscribe](#subscribe)
    - [update](#update)
    - [update\_avatar](#update_avatar)
    - [verify\_code](#verify_code)
    - [verify\_email](#verify_email)
  - [数据集部分](#数据集部分)
    - [create](#create)
    - [delete](#delete-1)
    - [list](#list)
    - [retrieve](#retrieve-1)
    - [update](#update-1)
    - [upload](#upload)
  - [排行榜部分](#排行榜部分)
    - [average](#average)
    - [average\_list](#average_list)
    - [clear](#clear)
    - [comment](#comment)
    - [dataset\_comment](#dataset_comment)
    - [like\_dataset\_comment](#like_dataset_comment)
    - [like\_llm\_comment](#like_llm_comment)
    - [list](#list-1)
    - [llm\_comment](#llm_comment)
    - [retrieve](#retrieve-2)
    - [update](#update-2)
  - [模型测试部分](#模型测试部分)
    - [battle\_match](#battle_match)
    - [battle\_result](#battle_result)
    - [create](#create-1)
    - [delete](#delete-2)
    - [generate](#generate)
    - [list](#list-2)
    - [retrieve](#retrieve-3)
    - [test](#test)
    - [update](#update-3)
  - [额外需求](#额外需求)
    - [jwt](#jwt)
    - [admin\_required](#admin_required)
***
### 用户账号部分  
#### delete  
**功能描述**：删除指定的用户。该api在传入的jwt对应一般用户时只允许删除用户自己，而在传入的jwt对应管理员时允许删除任意用户。  
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
#### list_subscription  
**功能描述**：列出指定用户订阅的所有模型。  
**请求方式**：GET  
**请求URL**：`/user/list_subscription/<id>`  
**请求参数**：无  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "llms": [
        "llm信息等",
        ...
    ]
},
status=200
```
* id异常  
```python
status=400
```
#### login  
**功能描述**：进行用户登录并获取jwt。  
**请求方式**：POST  
**请求URL**：`/user/login`  
**请求参数**：  
```python
{
    "username": "用户名",
    "password": "密码"
}
```
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
**功能描述**：使用验证码进行登录。  
**请求方式**：POST  
**请求URL**：`/user/login_with_verify_code`  
**请求参数**：  
```python
{
    "mobile": "手机号",
    "verify_code": "验证码"
}
```
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
**功能描述**：用户登出。  
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
**功能描述**：注册新用户。  
**请求方式**：POST  
**请求URL**：`/user/register`  
**请求参数**：  
```python
{
    "username": "用户名",
    "password": "密码",
    "mobile": "手机号",
    #"email": "邮箱",
    #"secret": "邀请码"
}
```
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
**功能描述**：获取指定用户的信息。  
**请求方式**：GET  
**请求URL**：`/user/retrieve/<id>`  
**请求参数**：无  
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
#### retrieve_password  
**功能描述**：获取指定用户的密码。  
**请求方式**：GET  
**请求URL**：`/user/retrieve_password`  
**请求参数**：无  
**额外需求**：jwt  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "password": "password"
},
status=200
```
* 未找到用户  
```python
status=400
```
#### send_email  
**功能描述**：发送邮箱验证码。  
**请求方式**：POST  
**请求URL**：`/user/send_email`  
**请求参数**：  
```python
{
    "email": "邮箱"
}
```
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
**功能描述**：发送短信验证码。  
**请求方式**：POST  
**请求URL**：`/user/send_message`  
**请求参数**：  
```python
{
    "mobile": "手机号"
}
```
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
#### subscribe  
**功能描述**：订阅某一模型。  
**请求方式**：POST  
**请求URL**：`/user/subscribe`  
**请求参数**：  
```python
{
    "llmId": "模型id"
}
```
**额外需求**：jwt  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
},
status=200
```
* 参数异常  
```python
status=400
```
#### update  
**功能描述**：更新指定用户的信息。  
**请求方式**：PUT/PATCH  
**请求URL**：`/user/update/<id>`  
**请求参数**：  
```python
PUT={
    "username": "用户名",
    "password": "密码",
    "mobile": "手机号",
    #"email": "邮箱"
}
PATCH={
    #"username": "用户名",
    #"password": "密码",
    #"mobile": "手机号",
    #"email": "邮箱"
}
```
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
**功能描述**：更新指定用户的头像。  
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
**功能描述**：验证短信验证码的正确性。  
**请求方式**：POST  
**请求URL**：`/user/verify_code`  
**请求参数**：   
```python
{
    "mobile": "手机号",
    "verify_code": "验证码"
}
```
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
**功能描述**：验证邮箱验证码的正确性。  
**请求方式**：POST  
**请求URL**：`/user/verify_email`  
**请求参数**：  
```python
{
    "email": "邮箱",
    "verify_code": "验证码"
}
```
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
**功能描述**：创建新的数据集。  
**请求方式**：POST  
**请求URL**：`/dataset/create`  
**请求参数**：  
```python
{
    "name": "数据集名称",
    #"description": "数据集描述",
    #"subjective": "是否为主观题"
}
```
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
#### delete  
**功能描述**：删除指定的数据集。  
**请求方式**：DELETE  
**请求URL**：`/dataset/delete/<id>`  
**请求参数**：无  
**额外需求**：admin_required  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
},
status=200
```
* ID异常  
```python
status=400
```
#### list  
**请求方式**：GET  
**请求URL**：`/dataset/list`  
**请求参数**：无  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "data": [
        {
            "id": "数据集id",
            "name": "数据集名称",
            "description": "数据集描述",
            ...
        },
        ...
    ]
},
status=200
```
#### retrieve  
**功能描述**：获取指定数据集的信息。  
**请求方式**：GET  
**请求URL**：`/dataset/retrieve/<id>`  
**请求参数**：无  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "name": "数据集名称",
    "description": "数据集描述",
    ...
},
status=200
```
* ID异常  
```python
status=404
```
#### update  
**功能描述**：更新指定数据集的信息。  
**请求方式**：PUT/PATCH  
**请求URL**：`/dataset/update/<id>`  
**请求参数**：  
```python
PUT={
    "name": "数据集名称",
    #"description": "数据集描述",
    #"subjective": "是否为主观题"
}
PATCH={
    #"name": "数据集名称",
    #"description": "数据集描述",
    #"subjective": "是否为主观题"
}
```
**额外需求**：admin_required  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
},
status=200
```
* ID异常  
```python
status=404
```
#### upload  
**功能描述**：上传数据集文件。  
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
#### average  
**功能描述**：获取指定数据集的平均分数。  
**请求方式**：GET  
**请求URL**：`/ranking/average/<id>`  
**请求参数**：无  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "average": "平均分数"
},
status=200
```
* ID异常  
```python
status=400
```
#### average_list  
**功能描述**：获取所有数据集的平均分数。  
**请求方式**：GET  
**请求URL**：`/ranking/average_list`  
**请求参数**：无  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "data": [
        "平均分数1",
        "平均分数2",
        ...
    ]
},
status=200
```
#### clear  
**功能描述**：清空排行榜中某一格的分数。    
**请求方式**：POST  
**请求URL**：`/ranking/clear`  
**请求参数**：  
```python
{
    "datasetId": "数据集id",
    "llmId": "模型id"
}
```
**额外需求**：admin_required  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
},
status=200
```
* 参数异常  
```python
status=400
```
#### comment  
**功能描述**：对某一数据集或模型进行评论。  
**请求方式**：POST  
**请求URL**：`/ranking/comment`  
**请求参数**：  
```python
{
    "datasetId": "数据集id" or "llmId": "模型id",
    "comment": "评论内容",
    "respond_to": "回复的评论id"  
}
```
**额外需求**：jwt  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "id": "评论id"
},
status=200
```
* 参数异常  
```python
status=400
```
#### dataset_comment  
**功能描述**：获取某一数据集下的全部评论。  
**请求方式**：GET  
**请求URL**：`/ranking/dataset_comment/<id>`  
**请求参数**：无  
**额外需求**：jwt  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "comments": [
        {
            "comment": "评论内容",
            "add_time": "添加时间(未格式化)"
        },
        ...
    ]
},
status=200
```
* ID异常  
```python
status=400
```
#### like_dataset_comment  
**功能描述**：对某一数据集评论进行点赞。  
**请求方式**：POST  
**请求URL**：`/ranking/like_dataset_comment`  
**请求参数**：  
```python
{
    "id": "评论id"
}
```
**额外需求**：jwt  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
},
status=200
```
* 参数异常  
```python
status=400
```
#### like_llm_comment  
**功能描述**：对某一模型评论进行点赞。  
**请求方式**：POST  
**请求URL**：`/ranking/like_llm_comment`  
**请求参数**：  
```python
{
    "id": "评论id"
}
```
**额外需求**：jwt  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
},
status=200
```
* 参数异常  
```python
status=400
```
#### list  
**功能描述**：获取所有分数情况，包括模型id，数据集id，对应分数，添加时间等    
**请求方式**：GET  
**请求URL**：`/ranking/list`  
**请求参数**：无  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "data": [
        {
            "LLM": "模型id",
            "dataset": "数据集id",
            "add_time": "添加时间(未格式化)",
            "credit": "分数",
        },
        ...
    ]
},
status=200
```
#### llm_comment  
**功能描述**：获取某一模型下的全部评论。  
**请求方式**：GET  
**请求URL**：`/ranking/llm_comment/<id>`  
**请求参数**：无  
**额外需求**：jwt  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "comments": [
        {
            "comment": "评论内容",
            "add_time": "添加时间(未格式化)"
        },
        ...
    ]
},
status=200
```
* ID异常  
```python
status=400
```
#### retrieve  
**功能描述**：获取某一模型在某一数据集下的分数。  
**请求方式**：POST  
**请求URL**：`/ranking/retrieve`  
**请求参数**：   
```python
{
    "datasetId": "数据集id",
    "llmId": "模型id"
}
```
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "credit": "分数 or null"
},
status=200
```
#### update  
**功能描述**：更新某一模型在某一数据集下的分数。  
**请求方式**：POST  
**请求URL**：`/ranking/update`  
**请求参数**：  
```python
{
    "datasetId": "数据集id",
    "llmId": "模型id",
    "credit": "分数"
}
```
**额外需求**：login_required    
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
},
status=200
```
* 参数异常  
```python
status=400
```
**特殊说明**：接口会检查数据集是否为主观题，正常用户仅能对主观题进行评分，管理员则不受限制。  
***
### 模型测试部分  
#### battle_match  
**功能描述**：通过一个模型id，返回一个与之势均力敌的模型id。  
**请求方式**：POST  
**请求URL**：`/testing/battle_match`  
**请求参数**：  
```python
{
    "llmId": "模型id"
}
```
**额外需求**：login_required  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "llmId": "模型id",
},
status=200
```
* 参数异常  
```python
status=400
```
**特殊说明**：当数据库中仅有一个数据集时返回值也为200，但不包含llmId。  
#### battle_result  
**功能描述**：提交一场模型对战的结果并进行结算。  
**请求方式**：POST  
**请求URL**：`/testing/battle_result`  
**请求参数**：  
```python
{
    "llm1": "1号模型id",
    "llm2": "2号模型id",
    "winner": "结果，0为平局，1为1号胜利，-1为1号失败",
    "round": "回合数",
    "result": "JSON对象，包含每一回合的prompt和双方response"
}
```
**额外需求**：login_required  
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
#### create  
**功能描述**：创建一个新的模型测试。  
**请求方式**：POST  
**请求URL**：`/testing/create`  
**请求参数**：  
```python
{
    "name": "模型名称",
    #"api_url": "api地址",
    #"api_headers": "api请求头",
    #"api_data": "api请求体",
    #"api_RPM": "api请求频率",
    #"description": "模型描述",
    #"official_website": "官方网站",
    #"document_name": "文档名称",
    #"document_website": "文档地址",
    #"license": "认证"
}
```
**额外需求**：jwt  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "llmId": "模型id"
},
status=201
```
* 参数异常  
```python
status=400
```
**特殊说明**：关于上面列出的参数详细信息请查阅标准部分。  
#### delete  
**功能描述**：删除指定的模型测试。  
**请求方式**：DELETE  
**请求URL**：`/testing/delete/<id>`  
**请求参数**：无  
**额外需求**：admin_required  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
},
status=200
```
* ID异常  
```python
status=400
```
#### generate  
**功能描述**：基于某个模型的api信息，用提供的prompt进行一次生成。  
**请求方式**：POST  
**请求URL**：`/testing/generate`  
**请求参数**：  
```python
{
    "llmId": "模型id",
    "prompt": "生成的prompt"
}
```
**额外需求**：login_required  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "content": "生成结果"
},
status=200
```
* 参数异常  
```python
status=400
```
#### list  
**功能描述**：获取所有模型测试的信息。  
**请求方式**：GET  
**请求URL**：`/testing/list`  
**请求参数**：无  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "data": [
        {
            "id": "模型id",
            "name": "模型名称",
            "api_url": "api地址",
            ...
        },
        ...
    ]
},
status=200
```
#### retrieve  
**功能描述**：获取指定模型测试的信息。  
**请求方式**：GET  
**请求URL**：`/testing/retrieve/<id>`  
**请求参数**：无  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok",
    "name": "模型名称",
    "api_url": "api地址",
    ...
},
status=200
```
* ID异常  
```python
status=404
```
#### test  
**功能描述**：对指定模型测试进行测试。使用llmId和datasetId筛选后，会对指定的模型和数据集对应的行/列所有单元进行测试。  
**请求方式**：POST  
**请求URL**：`/testing/testing`   
**请求参数**：  
```python
{
    #"llmId": "模型id",
    #"datasetId": "数据集id",
    #"style": "筛选样式"
}
```
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
},
status=200
```
**特殊说明**：测试筛选样式style支持以下值：  
* `fill`：在llmId和datasetId筛选后，仅针对表格中还未被测试（也即credit为null）的单元格进行测试。  

#### update  
**功能描述**：更新指定模型测试的信息。  
**请求方式**：PUT/PATCH  
**请求URL**：`/testing/update/<id>`  
**请求参数**：  
```python
PUT={
    "name": "模型名称",
    #"api_url": "api地址",
    #"api_headers": "api请求头",
    #"api_data": "api请求体",
    #"api_RPM": "api请求频率",
    #"description": "模型描述",
    #"official_website": "官方网站",
    #"document_name": "文档名称",
    #"document_website": "文档地址",
    #"license": "认证"
}
PATCH={
    #"name": "模型名称",
    #"api_url": "api地址",
    #"api_headers": "api请求头",
    #"api_data": "api请求体",
    #"api_RPM": "api请求频率",
    #"description": "模型描述",
    #"official_website": "官方网站",
    #"document_name": "文档名称",
    #"document_website": "文档地址",
    #"license": "认证"
}
```
**额外需求**：admin_required  
**返回情况**：  
* 正常返回  
```python
{
    "message": "ok"
},
status=200
```
* ID异常  
```python
status=404
```
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
#### admin_required  
admin_required标签仅用于管理员专用接口，其本质为强化版的jwt，在返回之前会检验用户是否具有管理员权限，故不需要跟jwt一起使用。  
**获取方式**：只需正常传入jwt即可。  
**返回情况**：  
在需要管理员权限的接口中，如果jwt对应用户并非管理员，会返回以下信息：  
```python
{
    "message": "User must be admin."
},
status=401
```