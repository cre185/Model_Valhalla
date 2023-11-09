## 测试说明  
### 数据库初始化  
测试用数据初始化方式：使用`python manage.py loaddata db.json`将简单的测试用数据导入数据库   
需要导出数据可以使用`python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json`  
顺便地，如果需要清空当前数据库可以使用`python manage.py flush`  