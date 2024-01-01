## 测试说明  
### 数据库初始化  
导入标准测试数据可以使用如下命令：  
```bash
python manage.py flush
python manage.py init_db
``` 
当前的标准测试数据包括：  
* 一个管理员账户，用户名为realadmin，密码为realadmin  
* 一个普通用户账户，用户名为testuser，密码为testuser  
* 5个标准的数据集，并分别对应一个题目库  
* 5个标准的模型，并分别对应一个模型的调用接口  
* 这些模型/数据集对应的测试分数，其中客观数据集对应的测试分数已经初始化，为之前测试得到的数据  

如需更改init_db命令的行为，请修改`user/management/commands/init_db.py`  
### 单元测试  
单元测试使用了Django自带的测试框架，使用下列命令进行测试：  
```bash
python manage.py test
```
本项目提供的单元测试较为完善，覆盖了大部分的功能。单元测试的成功率为100%。  
使用coverage工具进行了测试覆盖率的统计，使用下列命令即可在进行测试的同时查看单元测试覆盖率：  
```bash
coverage run manage.py test
coverage report
```
目前项目的单元测试覆盖率已经达到97%，较为令人满意。  
