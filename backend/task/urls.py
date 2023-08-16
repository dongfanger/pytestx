#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Don
@Date    :  2020/11/24 11:01
@Desc    :  
"""

from django.urls import path

from task.views import project_view, run_view, task_view, mock_view, scaffold_view

urlpatterns = [
    path(r"scaffold", scaffold_view.startproject),  # 项目脚手架

    path(r"mock/searchSku", mock_view.search_sku),
    path(r"mock/addCart", mock_view.add_cart),
    path(r"mock/order", mock_view.order),
    path(r"mock/pay", mock_view.pay),

    # ------------------项目开始------------------
    path(r"projects", project_view.ProjectViewSet.as_view({
        "get": "list",
        "post": "create"
    })),
    path(r"projects/<int:pk>", project_view.ProjectViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    })),
    path(r"projects/cur", project_view.project_cur),  # 项目环境下拉框选项
    path(r"projects/<int:pk>/gitSync", project_view.git_sync),
    # ------------------项目结束------------------

    # ------------------任务开始------------------
    path(r"", task_view.TaskViewSet.as_view({
        "get": "list",
        "post": "create"
    })),
    path(r"<int:pk>", task_view.TaskViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    })),
    path(r"cases", task_view.cases),
    path(r"<int:task_id>/cases", task_view.TaskCaseView.as_view({
        "get": "list",
        "post": "add",
    })),
    path(r"<int:task_id>/cases/<int:case_id>", task_view.TaskCaseView.as_view({
        "delete": "remove"
    })),
    path(r"<int:task_id>/run", run_view.run_task),
    path(r"<int:task_id>/result", task_view.result),
    path(r"<int:task_id>/cases/<int:case_id>/result", task_view.case_result),
    path(r"<int:task_id>/<int:user_id>/report", task_view.report),
    # ------------------任务结束------------------
]
