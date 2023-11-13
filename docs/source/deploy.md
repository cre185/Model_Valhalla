## 部署  
### 服务器部署  
项目的服务器部署依靠docker一步实现，在backend目录下执行`docker-compose up`即可。  
注意，在部署前需要确保前端的静态产生文件已经正确放置在backend/build目录下。  
### 后端环境  
#### 安装python依赖库  
```bash
pip install -r requirements.txt
```