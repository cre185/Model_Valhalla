## 测试说明  
**目录**  
- [测试说明](#测试说明)
  - [更新与下载python依赖](#更新与下载python依赖)
  - [数据库迁移](#数据库迁移)
  - [数据库初始化](#数据库初始化)
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
python manage.py loaddata db.json
```
需要导出数据时可以使用  
```bash
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db_test.json
```  
正常情况下项目下的db.json为标准测试用数据，不定期更新，建议不要随意修改。  
当前标准数据中包含：  
* 管理员realadmin与一般用户testuser，密码与用户名一致；  
* 两个测试用llm以及dataset（未绑定文件）；  
* 对应的credits，其中有两个被修改。  

(上述信息修改于：2023.11.14)   