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
from concurrent.futures.thread import ThreadPoolExecutor

import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from constant.TaskRunType import TaskRunType
from pytestx import settings
from pytestx.settings import SANDBOX_PATH
from task.models import Case, TaskResult, Task, TaskCase
from task.serializers import TaskResultSerializer


class TaskRunner:
    def __init__(self, task_id, run_user_id):
        self.task_id = task_id
        self.project_id = Task.objects.get(id=task_id).project_id
        self.project_name = Case.objects.filter(project_id=self.project_id)[0].filepath.split(os.sep)[0]
        self.project_dir = os.path.join(SANDBOX_PATH, self.project_name)
        self.run_user_id = run_user_id
        self.current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        self.report_path = os.path.join(self.project_name, "reports", self.current_time + ".html")
        task_case_id_list = [task_case.case_id for task_case in TaskCase.objects.filter(task_id=self.task_id)]
        self.case_list = Case.objects.filter(Q(id__in=task_case_id_list))
        self.case_num = len(self.case_list)
        self.case_count = 0
        self.directory_path = os.path.join(SANDBOX_PATH, self.project_name, "directory")
        self.directory_sub_path = os.path.join(self.directory_path, f"{str(self.task_id)}-{self.current_time}")
        self.case_filepath_list = []

    def run(self):
        if not os.path.exists(SANDBOX_PATH):
            os.mkdir(SANDBOX_PATH)
        self.get_case_from_db()
        if settings.TASK_RUN_TYPE == TaskRunType.COMMAND:
            try:
                self.execute_by_param()
            except:  # 如果命令行参数添加路径，字符超长报错，降级为复制用例
                self.execute_by_directory()
        elif settings.TASK_RUN_TYPE == TaskRunType.DIRECTORY:
            self.execute_by_directory()
        elif settings.TASK_RUN_TYPE == TaskRunType.DOCKER:
            pass
        self.save_task_result()

    def get_case_from_db(self):
        # 数据库查找用例
        for case in self.case_list:
            filepath = case.filepath
            self.case_filepath_list.append(filepath)

    def execute_by_param(self):
        """命令行拼装路径"""
        os.chdir(self.project_dir)
        path_list = [os.sep.join(x.split(os.sep)[1:]) for x in self.case_filepath_list]
        cmd = f"pytest {' '.join(path_list)} --html={os.path.join(SANDBOX_PATH, self.report_path)} --self-contained-html"
        subprocess.getoutput(cmd)

    def execute_by_directory(self):
        """复制文件到directory目录执行"""
        if not os.path.exists(self.directory_path):
            os.mkdir(self.directory_path)
        if not os.path.exists(self.directory_sub_path):
            os.mkdir(self.directory_sub_path)
        thread_pool = ThreadPoolExecutor()  # 多线程复制用例
        for filepath in self.case_filepath_list:
            args = (self.copy_case, filepath)
            thread_pool.submit(*args).add_done_callback(self.directory_run)

    def directory_run(self, *args):
        """directory执行"""
        self.case_count += 1
        if self.case_count == self.case_num:
            os.chdir(self.directory_sub_path)
            cmd = f"pytest --html={os.path.join(SANDBOX_PATH, self.report_path)} --self-contained-html"
            subprocess.getoutput(cmd)

    def copy_case(self, filepath):
        file_path_abs = os.path.join(SANDBOX_PATH, filepath)
        shutil.copy2(file_path_abs, self.directory_sub_path)

    def save_task_result(self):
        data = {
            "taskId": self.task_id,
            "result": "执行成功",
            "runUserId": self.run_user_id,
            "reportPath": self.report_path
        }
        try:
            instance = TaskResult.objects.get(task_id=self.task_id, run_user_id=self.run_user_id)
            serializer = TaskResultSerializer(data=data, instance=instance)  # 更新
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ObjectDoesNotExist:  # 新增
            serializer = TaskResultSerializer(data=data)
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

    return Response({"msg": "计划运行成功"}, status=status.HTTP_200_OK)
