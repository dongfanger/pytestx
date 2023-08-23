#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  2021/3/26 11:06
@Desc    :  
"""
import os
import re
import shutil
import subprocess
import time
import uuid

import jwt
from loguru import logger
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from pytestx import settings
from pytestx.settings import LOCAL_PATH, DEPLOY_PATH, REPORT_PATH
from task.constant.TaskRunMode import TaskRunMode
from task.exception.TaskException import TaskException
from task.models import Task, Project
from task.serializers import TaskUpdateResultSerializer


class TaskRunner:
    def __init__(self, task_id, run_user_id):
        self.task_id = task_id
        self.directory = Task.objects.get(id=task_id).directory
        self.project_id = Task.objects.get(id=task_id).project_id
        self.git_repository = Project.objects.get(id=self.project_id).git_repository
        self.git_branch = Project.objects.get(id=self.project_id).git_branch
        self.git_name = re.findall(r"^.*/(.*).git", self.git_repository)[0]
        self.local_path = os.path.join(LOCAL_PATH, str(uuid.uuid1()).replace("-", ""))
        self.run_user_id = run_user_id
        self.current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        self.report_name = f"{str(self.git_name)}-{self.task_id}-{self.run_user_id}-{self.current_time}.html"
        self.project_report_path = os.path.join(self.local_path, self.git_name, "reports", self.report_name)
        self.dockerfile_pytest = os.path.join(DEPLOY_PATH, "Dockerfile.pytest")
        self.cmd_list = []

    def run(self):
        logger.info("任务开始执行")
        self.get_pytest_cmd_list()
        if settings.TASK_RUN_MODE == TaskRunMode.DOCKER:  # 容器模式
            try:
                self.execute_by_docker()
            except Exception as e:
                logger.info(e)
                if e == TaskException.DockerNotSupportedException:
                    logger.info("降级为本地执行")
                    self.execute_by_local()
        if settings.TASK_RUN_MODE == TaskRunMode.LOCAL:  # 本地模式
            self.execute_by_local()
        self.save_task()

    def execute_by_local(self):
        logger.info("运行模式：本地")
        os.makedirs(self.local_path, exist_ok=True)
        os.chdir(self.local_path)
        for cmd in self.cmd_list:
            logger.info(cmd)
            output = subprocess.getoutput(cmd)
            if output:
                logger.info(output)
        os.makedirs(REPORT_PATH, exist_ok=True)
        shutil.copy2(self.project_report_path, REPORT_PATH)
        shutil.rmtree(LOCAL_PATH)

    def execute_by_docker(self):
        logger.info("运行模式：容器")
        output = subprocess.getoutput("docker -v")
        logger.info(output)
        if "command not found" in output:
            raise TaskException.DockerNotSupportedException
        # 复制文件到container目录，多线程，构建pytest镜像，运行
        self.pytest_container()

    def get_pytest_cmd_list(self):
        self.cmd_list = [
            f"git clone -b {self.git_branch} {self.git_repository}",
            f"pytest {os.path.join(self.git_name, self.directory)} --html={self.project_report_path} --self-contained-html"
        ]

    def container(self, *args):
        """构建镜像，运行"""
        cmd = f"docker build --build-arg TESTS={self.container_tests_path} -f {self.dockerfile_pytest} -t {self.container_name} {self.project_dir}"
        logger.info(cmd)
        output = subprocess.getoutput(cmd)
        logger.info(output)

    def save_task(self):
        data = {
            "status": "1",
            "run_time": self.current_time,
            "run_user_id": self.run_user_id,
            "report_path": self.report_name
        }
        logger.info(data)
        instance = Task.objects.get(id=self.task_id)
        serializer = TaskUpdateResultSerializer(data=data, instance=instance)  # 更新
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
