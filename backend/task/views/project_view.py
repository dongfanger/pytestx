# Create your views here.
import os
import time

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from pytestx.settings import SANDBOX_PATH
from task.models import Project, Case, TaskCase
from task.serializers import ProjectSerializer, CaseSerializer
from task.utils.git_util import git_pull


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        # 重写create方法
        try:
            Project.objects.get(name=request.data.get("name"))
            return Response("存在同名项目", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ObjectDoesNotExist:  # 如果不存在会抛异常
            pass

        # ------------复用现成代码开始----------------
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # ------------复用现成代码结束----------------

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET'])
def project_cur(request, *args, **kwargs):
    data = {"projectList": [], "curProject": {}}
    projects = Project.objects.all()
    if not projects:
        return Response(data, status=status.HTTP_200_OK)
    for project in projects:
        data["projectList"].append({"projectId": str(project.id),
                                    "projectName": project.name})
    data["curProject"] = {"curProjectId": str(projects[0].id),
                          "curProjectName": projects[0].name}
    return Response(data, status=status.HTTP_200_OK)


class GitSyncConfig:
    project_id = ""
    project_name = ""


def pull():
    project = Project.objects.get(id=GitSyncConfig.project_id)
    repository = project.git_repository
    branch = project.git_branch
    GitSyncConfig.project_name = git_pull(repository, branch, SANDBOX_PATH)


def save():
    git_files = []
    tests_dir = os.path.join(SANDBOX_PATH, GitSyncConfig.project_name, "tests")
    for root, _, files in os.walk(tests_dir):
        for file in files:
            abs_path = os.path.join(root, file)
            if os.path.isfile(abs_path):
                if (file.startswith("test_") or file.endswith("_test")) and file.endswith(".py"):
                    filename = abs_path.replace(tests_dir, "").strip(os.sep)
                    filepath = abs_path.replace(SANDBOX_PATH, "").strip(os.sep)
                    git_files.append((filename, filepath))
    git_files = set(git_files)

    project_id = GitSyncConfig.project_id
    cases = Case.objects.filter(project_id=project_id)
    db_files = set((case.filename, case.filepath) for case in cases)

    to_delete_cases = db_files - git_files
    to_add_cases = git_files - db_files
    to_update_cases = git_files & db_files

    for _, filepath in to_delete_cases:
        case = Case.objects.get(project_id=project_id, filepath=filepath)
        case.delete()
        task_case_list = TaskCase.objects.filter(case_id=case.id)  # 同时删除所有任务关联的用例
        for task_case in task_case_list:
            task_case.delete()

    data = {
        "desc": "desc",
        "creator_id": 1,  # todo 根据当前登录用户设置
        "projectId": GitSyncConfig.project_id,
        "filename": "",
        "filepath": ""
    }
    for filename, filepath in to_add_cases:
        data["desc"] = filename
        data["filename"] = filename
        data["filepath"] = filepath
        serializer = CaseSerializer(data=data)
        serializer.is_valid()
        serializer.save()

    for filename, filepath in to_update_cases:
        data["desc"] = filename
        data["filename"] = filename
        data["filepath"] = filepath
        case = Case.objects.get(project_id=project_id, filepath=filepath)
        serializer = CaseSerializer(instance=case, data=data)
        serializer.is_valid()
        serializer.save()


@api_view(['POST'])
def git_sync(request, *args, **kwargs):
    # todo Windows同步项目后，保存的文件路径，在切换到Mac时，不兼容（当前只能手动重新同步）
    project_id = kwargs["pk"]
    GitSyncConfig.project_id = project_id
    pull()
    save()
    project = Project.objects.get(id=project_id)
    project.last_sync_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    project.save()
    return Response({"msg": "同步成功", "lastSyncTime": project.last_sync_time}, status=status.HTTP_200_OK)
