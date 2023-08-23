from django.db import models


# Create your models here.
class BaseTable(models.Model):
    class Meta:
        abstract = True
        db_table = 'BaseTable'

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)


class Project(BaseTable):
    class Meta:
        db_table = "project"

    name = models.CharField("项目名称", unique=True, max_length=100, null=False)
    git_repository = models.CharField("Git仓库", max_length=100, null=True, blank=True)
    git_branch = models.CharField("Git分支", max_length=100, null=True, blank=True)


class Task(models.Model):
    class Meta:
        db_table = "task"

    name = models.CharField("任务名称", max_length=50, null=False)
    directory = models.CharField("执行目录", max_length=200, null=False)
    project_id = models.IntegerField("项目id", null=False)
    is_regular = models.CharField("定时开关", max_length=1, null=True, blank=True, default="0")
    crontab = models.CharField("crontab表达式", max_length=20, null=True, blank=True, default="")
    status = models.CharField("运行状态", max_length=1, null=True, blank=True, default="0")
    run_time = models.DateTimeField("运行时间", auto_now=True)
    run_user_id = models.IntegerField("运行人员", null=False, default=0)
    report_path = models.CharField("测试报告", max_length=300, null=False, default="")
