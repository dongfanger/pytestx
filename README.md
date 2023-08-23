# pytestx

体验：
- 安装依赖：前端（npm install）后端（pip install -r requirements.txt）
- 启动服务：前端（npm run serve）后端（python manage.py runserver）
- 访问：http://localhost:8080/ 
- 用户名密码：admin qa123456

一键部署：

在pytestx根目录执行命令

- 后端：
  
    chmod +x ./deploy/backend.sh
    
    ./deploy/backend.sh

- 前端： 
  
    修改deploy/nginx.conf的proxy_pass为宿主机IP地址
  
    chmod +x ./deploy/frontend.sh

    ./deploy/frontend.sh
