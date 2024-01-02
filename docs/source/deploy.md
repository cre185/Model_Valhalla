## 部署  
### 项目结构简述  
项目部署基于docker，具体关系为数据库MySQL、后端Django(DRF)、代理服务器Nginx分别位于三个容器内，前两者与后两者分别连接，与小作业保持一致。  
项目中的主要配置文件均位于backend目录下，具体位置为（相对backend目录）：  
* requirements.txt：python依赖  
* Model_Valhalla/settings_prod.py：生产环境采用的配置（指定了MySQL等）  
* nginx/model_valhalla.conf：nginx配置文件  
* Dockerfile and docker-compose.yml：docker配置文件  
* .env：MySQL环境变量配置文件  

### 部署至服务器  
项目的服务器部署依靠docker实现，主要需要以下几个步骤：
1. 修改后端的settings中的`CORS_ORIGIN_WHITELIST`，添加目标服务器的地址。  
2. 将后端部分的文件拷贝进服务器。  
3. 在backend目录下执行`docker-compose up`即可。 

注意，在部署前需要确保前端的静态产生文件已经正确提供。前端得到的静态文件在本项目中为assets文件夹以及一个index.html文件，这些文件应当位于backend/build目录下。 
