from __future__ import print_function

import json
import os
import sys

from importlib import import_module


class Settings():
    def __init__(self, settings):
        # got django project name
        self.DJANGO_PROJECT_NAME = getattr(settings, 'SUPERVISOR_DJANGO_PROJECT_NAME', os.environ['DJANGO_SETTINGS_MODULE'].split('.')[0])

        self.DJANGO_SETTINGS_MODULE = getattr(settings, 'SUPERVISOR_DJANGO_SETTINGS_MODULE', None)

        if hasattr(settings, 'SUPERVISOR_DJANGO_MANAGE_PATH'):
            self. DJANGO_MANAGE_PATH = settings.SUPERVISOR_DJANGO_MANAGE_PATH
            # check if it's really there
            if not os.path.exists(self.DJANGO_MANAGE_PATH):
                print('ERROR: No manage.py file found at "%s". Check settings.SUPERVISOR_DJANGO_MANAGE_PATH!' % self.DJANGO_MANAGE_PATH)
        else:
            def ext(fpath):
                return os.path.splitext(fpath)[0] + '.py'
            try:  # Django 1.3
                self.DJANGO_MANAGE_PATH = ext(import_module(self.DJANGO_PROJECT_NAME + '.manage').__file__)
            except ImportError:
                try:  # Django 1.4+
                    self.DJANGO_MANAGE_PATH = ext(import_module('manage').__file__)
                except ImportError:
                    print('ERROR: Can\'t find your manage.py - please define settings.SUPERVISOR_DJANGO_MANAGE_PATH')

        self.PYTHON_EXECUTABLE = getattr(settings, 'SUPERVISOR_PYTHON_EXECUTABLE', sys.executable)

        self.COMMAND_PREFIX = getattr(settings, 'SUPERVISOR_COMMAND_PREFIX', '')
        self.COMMAND_SUFFIX = getattr(settings, 'SUPERVISOR_COMMAND_SUFFIX', '')
        self.BASE_DIR = settings.BASE_DIR
        self.SUPERVISOR_CONFIG_PATH = settings.BASE_DIR + "/supervisor.d"

        if hasattr(settings, "SUPERVISOR_CONFIG_PATH"):
            self.SUPERVISOR_CONFIG_PATH = settings.SUPERVISOR_CONFIG_PATH
            if not os.path.exists(self.SUPERVISOR_CONFIG_PATH):
                print("ERROR: supervisor指定配置目录不存在 -->{}".format(self.SUPERVISOR_CONFIG_PATH))

        self.SUPERVISOR_CONFIG_DICT = {}

        if hasattr(settings, "SUPERVISOR_CONFIG_JSON"):
            self.SUPERVISOR_CONFIG_JSON = settings.SUPERVISOR_CONFIG_JSON
            if not os.path.exists(self.SUPERVISOR_CONFIG_JSON):
                print("ERROR: supervisor指定配置JSON文件不存在 -->{}".format(self.SUPERVISOR_CONFIG_JSON))
            else:
                with open(self.SUPERVISOR_CONFIG_JSON, "rb") as cj:
                    self.SUPERVISOR_CONFIG_DICT = json.loads(cj.read())
        elif hasattr(settings, "SUPERVISOR_CONFIG_DICT"):
            self.SUPERVISOR_CONFIG_DICT = settings.SUPERVISOR_CONFIG_DICT

        if not self.SUPERVISOR_CONFIG_DICT:
            print("ERROR: 未获取到supervisor 配置")
        self.SUPERVISOR_EXEC_PATH = ""
        if hasattr(settings, "SUPERVISOR_EXEC_PATH"):
            self.SUPERVISOR_EXEC_PATH = settings.SUPERVISOR_EXEC_PATH
