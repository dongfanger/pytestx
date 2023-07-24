# pytestx

体验：
- 安装依赖：前端（npm install）后端（pip install -r requirements.txt）
- 启动服务：前端（npm run serve）后端（python manage.py runserver）
- 访问：http://localhost:8080/ 
- 用户名密码：admin qa123456

已完成：
- 延续tep1.0，基于teprunner改造，聚焦任务调度
- 脚手架下载
- git项目同步平台，“沙箱”隔离
- 创建任务、关联用例，“容器”执行
- allure替换为pytest-html，可在线查看报告

TODO：
- [ ] 定时任务
- [ ] 并行/串行
- [ ] docker
- [ ] 通知
- [ ] 任务关联用例交互
- [x] 优先命令行参数拼接路径执行，超长则降级为用例复制
- [x] docker镜像

Docker：

在pytestx根目录执行以下命令

- 后端：
  
    打包 docker build --progress=plain -f ./backend/deploy/Dockerfile -t backend:v1.0 ./backend
    
    运行 docker run -p 8000:80 backend
  

- 前端：
    
    编译 docker run --rm -v $(pwd)/frontend/:/data/src  -w /data/src/ node:latest  /bin/sh -c "npm install && npm run build"
    (本地可跳过，在frontend目录执行npm install && npm run build是一样的)    
   
    打包 docker build -f ./frontend/deploy/Dockerfile -t frontend:v1.0 ./frontend
  
    配置 修改frontend/deploy/nginx.conf的proxy_pass为宿主机IP地址
  
    运行 docker run -p 8080:80 frontend