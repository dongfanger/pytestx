# Generated by Django 3.1.3 on 2023-08-23 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='项目名称')),
                ('git_repository', models.CharField(blank=True, max_length=100, null=True, verbose_name='Git仓库')),
                ('git_branch', models.CharField(blank=True, max_length=100, null=True, verbose_name='Git分支')),
            ],
            options={
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='任务名称')),
                ('directory', models.CharField(max_length=200, verbose_name='执行目录')),
                ('project_id', models.IntegerField(verbose_name='项目id')),
                ('is_regular', models.CharField(blank=True, default='0', max_length=1, null=True, verbose_name='定时开关')),
                ('crontab', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='crontab表达式')),
                ('status', models.CharField(blank=True, default='0', max_length=1, null=True, verbose_name='运行状态')),
                ('run_time', models.DateTimeField(auto_now=True, verbose_name='运行时间')),
                ('run_user_id', models.IntegerField(default=0, verbose_name='运行人员')),
                ('report_path', models.CharField(default='', max_length=300, verbose_name='测试报告')),
            ],
            options={
                'db_table': 'task',
            },
        ),
    ]
