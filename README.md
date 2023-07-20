# pytestx

体验：
- 安装依赖：前端（npm install）后端（pip install -r requirements.txt）
- 启动服务：前端（npm run serve）后端（python manage.py runserver）
- 访问：http://localhost:8080/ 
- 用户名密码：admin qa123456



- 延续tep1.0，基于teprunner改造，聚焦任务调度
- 脚手架下载
- git项目同步平台，“沙箱”隔离
- 创建任务、关联用例，“容器”执行
- allure替换为pytest-html，可在线查看报告

todo：
- [ ] 定时任务
- [ ] 并行/串行
- [ ] docker
- [ ] 通知
- [ ] 任务关联用例交互
- [ ] 优先命令行参数拼接路径执行，超长则降级为用例复制

