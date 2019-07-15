import os

from django.conf import settings

from django_supervisor_conf.app_settings import Settings


class SupervisorCTL(object):

    def __init__(self, **options):
        self.verbosity = int(options.get('verbosity', 1))
        self.readonly = options.get('readonly', False)
        self.settings = Settings(settings)
        self.options = options

    def start(self):
        thicommand = self.options.get("thicommand", "")
        command = "start " + (thicommand if thicommand is not None else "all")
        self.exec(command)

    def stop(self):
        thicommand = self.options.get("thicommand", "")
        command = "stop " + (thicommand if thicommand is not None else "all")
        self.exec(command)

    def restart(self):
        thicommand = self.options.get("thicommand", "")
        command = "restart " + (thicommand if thicommand is not None else "all")
        self.exec(command)

    def reload(self):
        thicommand = self.options.get("thicommand", "")
        command = "reload " + (thicommand if thicommand is not None else "all")
        self.exec(command)

    def exec(self, command):
        print(command)
        exec_path = self.settings.SUPERVISOR_EXEC_PATH
        if not exec_path:
            exec_path = "./"
        final_command = "cd {} && supervisorctl {}".format(exec_path, command)
        if os.system(final_command) != 0:
            print("执行系统命令失败,command - {}".format(final_command))
