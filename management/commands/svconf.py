from __future__ import print_function

from django.core.management.base import BaseCommand

from django_supervisor_conf.supervisor_conf import SupervisorConfig


class Command(BaseCommand):
    help = 'run this command to load the supervisor configs'

    def add_arguments(self, parser):
        parser.add_argument('subcommand', choices=["load_config"])

    def handle(self, *args, **options):
        """
        Dispatches by given subcommand
        """
        if options['subcommand'] == 'load_config':
            SupervisorConfig(**options).load_config()

        else:
            print(self.help)
