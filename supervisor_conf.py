import os

from django.conf import settings
from django_supervisor_conf.app_settings import Settings


class SupervisorConfig(object):

    def __init__(self, **options):
        self.verbosity = int(options.get('verbosity', 1))
        self.readonly = options.get('readonly', False)
        self.settings = Settings(settings)

    def load_config(self):
        """
        目前支持 python-manage  uwsgi 命令种类生成  如果为UWSGI 需要在字典中指定其UWSGI路径   其他命令需要全写命令
        配置字典的样例
        SUPERVISOR_CONFIG_DICT = {
            "filename without ini": [
                {"program": "xxx"   # program name  if program then must  group no need
                 "program_type": "python-manage"     # must
                 "command": "without python manage command"  # must
                 "directory": "xxx" # must
                 "stdout_logfile": "in project path"  # must
                 "stderr_logfile": "in project path"  # must
                 .......other conifg
                },
                {"program": "xxx"   # program name  if program then must  group no need
                 "program_type": "uwsgi"     # must
                 "uwsgi_path": ""  # if type is uwsgi then must
                 "command": "without uwsgi command"  # must
                 "directory": "xxx" # must
                 "stdout_logfile": "in project path"  # must
                 "stderr_logfile": "in project path"  # must
                 .......other conifg
                }
                ]
            }
        """
        if self.settings.SUPERVISOR_CONFIG_DICT:
            other_config_defult = {
                "autostart": "true",
                "startsecs": "1",
                "startretries": "3",
                "autorestart": "true",
                "stopsignal": "TERM",
                "stopwaitsecs": "10",
                "stopasgroup": "true",
                "killasgroup": "true",
                "stdout_logfile_maxbytes": "20MB",
                "stderr_logfile_maxbytes": "20MB",
                }
            if not os.path.exists(self.settings.SUPERVISOR_CONFIG_PATH):
                os.mkdir(self.settings.SUPERVISOR_CONFIG_PATH)
            for file_name, configs in self.settings.SUPERVISOR_CONFIG_DICT.items():
                with open(self.settings.SUPERVISOR_CONFIG_PATH + "/" + file_name + ".ini", "w") as f:
                    for config in configs:
                        program = config.pop("program") if "program" in config else None
                        if program:
                            final_conf = other_config_defult.copy()
                            final_conf.update(config)
                            f.write("[program:{}]\n".format(program))
                            program_type = final_conf.pop("program_type")
                            command = final_conf.pop("command", "")
                            if program_type == "python-manage":
                                f.write("command={} {} {}\n".format(self.settings.PYTHON_EXECUTABLE,
                                                          self.settings.DJANGO_MANAGE_PATH,
                                                          command))
                            elif program_type == "uwsgi":
                                uwsgi_path = final_conf.pop("uwsgi_path", "")
                                f.write("{} {}\n".format(uwsgi_path, command))
                            directory = final_conf.pop("directory", "")
                            f.write("directory={}/{}\n".format(self.settings.BASE_DIR, directory))
                            stdout_logfile = final_conf.pop("stdout_logfile", "")
                            f.write("stdout_logfile={}/{}\n".format(self.settings.BASE_DIR, stdout_logfile))
                            stderr_logfile = final_conf.pop("stderr_logfile", "")
                            f.write("stderr_logfile={}/{}\n".format(self.settings.BASE_DIR, stderr_logfile))
                            for key, value in final_conf.items():
                                f.write("{}={}\n".format(key, value))
                            f.write("\n")
                            f.write("\n")
                            continue
                        group = config.pop("group") if "group" in config else None
                        if group:
                            f.write("[group:{}]\n".format(group))
                            for key, value in config.items():
                                f.write("{}={}\n".format(key, value))
                            f.write("\n")
                            f.write("\n")

            if self.verbosity >= 1:
                print("SUCCESS: 已加载配置文件")
