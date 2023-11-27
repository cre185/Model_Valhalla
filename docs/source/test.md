## 测试说明  
**目录**  
- [测试说明](#测试说明)
  - [更新与下载python依赖](#更新与下载python依赖)
  - [数据库迁移](#数据库迁移)
  - [数据库初始化](#数据库初始化)
  - [单元测试](#单元测试)
### 更新与下载python依赖  
下载python依赖：  
```bash
pip install -r requirements.txt
```
引入了新的python库后，使用下列命令重新导出依赖：  
```bash
pip list --format=freeze > requirements.txt
```
### 数据库迁移  
当一次更新改变了Models时，需要进行数据库迁移  
使用下列命令迁移数据库至最新版本：  
```bash
python manage.py makemigrations
python manage.py migrate
```
### 数据库初始化  
导入标准测试数据可以使用如下命令：  
```bash
python manage.py flush
python manage.py init_db
``` 
当前的标准测试数据包括：  
* 一个管理员账户，用户名为realadmin，密码为realadmin  
* 一个普通用户账户，用户名为testuser，密码为testuser  
* 5个标准的数据集，名称分别为dataset1-5，并分别对应一个题目库  
* 4个标准的模型，名称分别为llm1-4，并分别对应一个模型的调用接口  
* 20个这些模型/数据集对应的测试分数，其中客观数据集对应的测试分数已经初始化，为之前测试得到的数据  

如需更改init_db命令的行为，请修改`user/management/commands/init_db.py`  
### 单元测试  
单元测试使用了Django自带的测试框架，使用下列命令进行测试：  
```bash
python manage.py test
```
测试样例中有部分测试需要调用模型的api接口，较为费时，因此平时不会进行测试。  
需要对这部分测试用例也进行测试时，将`settings.py`中的DEBUG设为False，再运行单元测试即可。  
