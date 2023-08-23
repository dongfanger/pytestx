# Create your views here.

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from task.models import Project
from task.serializers import ProjectSerializer


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
