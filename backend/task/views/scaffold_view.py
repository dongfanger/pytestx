#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  dongfanger
@Date    :  7/23/2020 8:12 PM
@Desc    :  项目脚手架
"""

import os
import shutil
import uuid
import zipfile

from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view

from pytestx import settings
from pytestx.settings import TEP_PROJECT_GIT_URL, EXPORT_PATH
from task.utils.git_util import git_pull


def make_zip(source_dir, zip_filename):
    zip_ = zipfile.ZipFile(zip_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, _, filenames in os.walk(source_dir):
        for filename in filenames:
            path = os.path.join(parent, filename)
            arcname = path[pre_len:].strip(os.path.sep)
            zip_.write(path, arcname)
    zip_.close()


def file_iterator(file_path, chunk_size=512):
    with open(file_path, mode='rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def copy_folder(source_folder, destination_folder, ignore_folders):
    shutil.copytree(source_folder, destination_folder, ignore=shutil.ignore_patterns(*ignore_folders))


def create_scaffold(temp_dir,):
    scaffold_path = os.path.join(EXPORT_PATH, "scaffold")
    git_pull(TEP_PROJECT_GIT_URL, "master", scaffold_path)
    tep_project_name = "tep-project"
    tep_dir = os.path.join(scaffold_path, tep_project_name)
    copy_folder(tep_dir, temp_dir, ignore_folders=[".idea", ".pytest_cache", "venv", "__pycache__", ".git"])
