#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  2021/2/7 9:35
@Desc    :  
"""
import os.path

from apscheduler.jobstores.base import JobLookupError
from apscheduler.triggers.cron import CronTrigger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from pytestx.settings import REPORT_PATH
from task.models import Task
from task.serializers import TaskSerializer
from task.views.run_view import TaskRunner
from task.views.schedule import scheduler


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        try:
            task = Task.objects.get(name=name)
            return Response(f"task {task.name} existed", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ObjectDoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            task = Task.objects.get(name=request.data.get("name"))
            project_id = request.data.get("projectId")
            is_regular = request.data.get("isRegular")
            task_crontab = request.data.get("taskCrontab")
            task_added = ""
            if is_regular == "1":
                run_user_nickname = "定时任务"
                user_id = "task"
                task_runner = TaskRunner(task.id, user_id)
                task_added = scheduler.add_job(func=task_runner.run,
                                               trigger=CronTrigger.from_crontab(task_crontab),
                                               id=str(task.id),
                                               args=[project_id, task.id, run_user_nickname, user_id],
                                               max_instances=1,
                                               replace_existing=True)
            data = serializer.data
            data["taskAdded"] = str(task_added)
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        name = request.data.get("name")
        task_id = kwargs["pk"]
        try:
            task = Task.objects.get(name=name)
            if task_id != task.id:
                return Response(f"task {task.name} existed ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ObjectDoesNotExist:
            pass

        project_id = request.data.get("projectId")
        is_regular = request.data.get("isRegular")
        task_crontab = request.data.get("taskCrontab")
        task_updated = ""

        if is_regular == "1":
            run_user_nickname = "定时任务"
            user_id = "task"
            task_runner = TaskRunner(task.id, user_id)
            task_updated = scheduler.add_job(func=task_runner.run,
                                             trigger=CronTrigger.from_crontab(task_crontab),
                                             id=str(task_id),
                                             args=[project_id, task_id, run_user_nickname, user_id],
                                             max_instances=1,
                                             replace_existing=True)
        if is_regular == "0":
            try:
                task_updated = scheduler.remove_job(str(task_id))
            except JobLookupError:
                task_updated = "task removed"

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        data = serializer.data
        data["taskUpdated"] = str(task_updated)
        return Response(data)

    def list(self, request, *args, **kwargs):
        project_id = request.GET.get("projectId")
        query = Q(project_id=project_id)
        task_name = request.GET.get("name")
        if task_name:
            query &= Q(name__icontains=task_name)
        queryset = Task.objects.filter(query).order_by('-id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        task_id = kwargs["pk"]
        try:
            scheduler.remove_job(str(task_id))
        except JobLookupError:
            pass
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


def report(request, *args, **kwargs):
    task_id = kwargs["task_id"]
    task = Task.objects.get(id=task_id)
    report_path = task.report_path

    with open(os.path.join(REPORT_PATH, report_path), 'r', encoding="utf8") as f:
        html_content = f.read()

    return HttpResponse(html_content, content_type='text/html')
