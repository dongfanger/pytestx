#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  2021/3/26 11:06
@Desc    :  
"""
import os
import shutil
import subprocess
import time
from concurrent.futures import wait
from concurrent.futures.thread import ThreadPoolExecutor

import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from loguru import logger
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from constant.TaskRunMode import TaskRunMode
from exception.TaskException import TaskException
from pytestx import settings
from pytestx.settings import SANDBOX_PATH, DEPLOY_PATH
from task.models import Task, Project
from task.serializers import TaskSerializer


class TaskRunner:
    def __init__(self, task_id, run_user_id):
        self.task_id = task_id
        self.project_id = Task.objects.get(id=task_id).project_id
        self.project_name = Project.objects.get(id=self.project_id).name
        self.project_dir = os.path.join(SANDBOX_PATH, self.project_name)
        self.run_user_id = run_user_id
        self.current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        self.report_path = os.path.join(self.project_name, "reports", self.current_time + ".html")
        self.container_path = os.path.join(SANDBOX_PATH, self.project_name, "container")
        self.container_name = f"{self.task_id}-{self.run_user_id}-{self.project_id}-{self.current_time}"
        self.container_sub_path = os.path.join(self.container_path, self.container_name)
        self.container_tests_path = os.path.join(self.container_sub_path, self.project_name, "tests")
        self.case_filepath_list = []
        self.dockerfile_pytest = os.path.join(DEPLOY_PATH, "Dockerfile.pytest")

    def run(self):
        logger.info("任务开始执行")
        os.makedirs(SANDBOX_PATH, exist_ok=True)
        if settings.TASK_RUN_MODE == TaskRunMode.DOCKER:  # 容器模式
            try:
                self.execute_by_docker()
            except Exception as e:
                logger.info(e)
                if e == TaskException.DockerNotSupportedException:
                    logger.info("降级为命令行执行")
                    self.execute_by_param()
        if settings.TASK_RUN_MODE == TaskRunMode.COMMAND:  # 命令行模式
            self.execute_by_param()
        self.save_task_result()

    def execute_by_param(self):
        """命令行拼装路径"""
        logger.info("运行模式：命令行")
        try:
            os.chdir(self.project_dir)
            path_list = [os.sep.join(x.split(os.sep)[1:]) for x in self.case_filepath_list]
            cmd = f"pytest {' '.join(path_list)} --html={os.path.join(SANDBOX_PATH, self.report_path)} --self-contained-html"
            output = subprocess.getoutput(cmd)
            logger.info(output)
        except Exception as e:  # 如果字符超长报错
            logger.info(e)
            logger.error("命令行模式执行异常，请切换为容器模式")

    def execute_by_docker(self):
        logger.info("运行模式：容器")
        output = subprocess.getoutput("docker -v")
        logger.info(output)
        if "command not found" in output:
            raise TaskException.DockerNotSupportedException
        # 复制文件到container目录，多线程，构建pytest镜像，运行
        self.pytest_container()

    def pytest_container(self):
        """复制文件到container目录"""
        os.makedirs(self.container_sub_path, exist_ok=True)
        executor = ThreadPoolExecutor()  # 多线程复制用例
        futures = []
        for filepath in self.case_filepath_list:
            future = executor.submit(self.copy_case, filepath)
            futures.append(future)
        # 关闭线程池，不再接受新的任务
        executor.shutdown()
        # 等待所有线程执行完毕
        wait(futures)
        # 所有线程执行完毕后继续执行
        self.pytest_shell()

    def pytest_shell(self, *args):
        """构建镜像，运行"""
        cmd = f"docker build --build-arg TESTS={self.container_tests_path} -f {self.dockerfile_pytest} -t {self.container_name} {self.project_dir}"
        logger.info(cmd)
        output = subprocess.getoutput(cmd)
        logger.info(output)

    def copy_case(self, filepath):
        src_file = os.path.join(SANDBOX_PATH, filepath)
        dest_file = os.path.join(self.container_sub_path, filepath)
        dest_dir = os.path.dirname(dest_file)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(src_file, dest_file)

    def save_task_result(self):
        """保存测试报告地址"""
        data = {
            "taskId": self.task_id,
            "result": "执行成功",
            "runUserId": self.run_user_id,
            "reportPath": self.report_path
        }
        try:
            instance = Task.objects.get(task_id=self.task_id, run_user_id=self.run_user_id)
            serializer = TaskSerializer(data=data, instance=instance)  # 更新
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ObjectDoesNotExist:  # 新增
            serializer = TaskSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()


@api_view(['POST'])
def run_task(request, *args, **kwargs):
    task_id = kwargs["task_id"]
    request_jwt = request.headers.get("Authorization").replace("Bearer ", "")
    request_jwt_decoded = jwt.decode(request_jwt, verify=False, algorithms=['HS512'])
    run_user_id = request_jwt_decoded["user_id"]
    task_runner = TaskRunner(task_id, run_user_id)
    task_runner.run()

    return Response({"msg": "任务运行成功"}, status=status.HTTP_200_OK)
