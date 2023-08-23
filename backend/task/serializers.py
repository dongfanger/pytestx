#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  2020/12/24 14:50
@Desc    :  
"""

from rest_framework import serializers

from task.models import Project, Task
from user.models import User


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    gitRepository = serializers.CharField(source="git_repository", required=False, allow_blank=True)
    gitBranch = serializers.CharField(source="git_branch", required=False, allow_blank=True)

    class Meta:
        model = Project
        fields = ["id", "name", "gitRepository", "gitBranch"]


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    projectId = serializers.CharField(source="project_id")
    isRegular = serializers.CharField(source="is_regular")
    runUserNickname = serializers.SerializerMethodField(required=False)
    runTime = serializers.SerializerMethodField(required=False)
    runUserId = serializers.CharField(source="run_user_id", required=False)
    reportPath = serializers.CharField(source="report_path", required=False)

    class Meta:
        model = Task
        fields = ["id", "name", "directory", "projectId", "isRegular", "crontab",
                  "status", "runUserNickname", "runTime", "runUserId", "reportPath"]

    def get_runUserNickname(self, instance):
        return User.objects.get(id=instance.run_user_id).nickname if instance.run_user_id else ""

    def get_runTime(self, instance):
        return instance.run_time.strftime("%Y-%m-%d %H:%M:%S") if instance.run_time else ""
