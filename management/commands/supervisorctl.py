from django.core.management import BaseCommand

from django_supervisor_conf.supervisor import SupervisorCTL


class Command(BaseCommand):
    help = 'run this command to start stop restart update  supervisor'

    def add_arguments(self, parser):
        parser.add_argument('subcommand', choices=["start", "stop", "restart", "update"])
        parser.add_argument('thicommand', nargs='?')

    def handle(self, *args, **options):
        """
        Dispatches by given subcommand
        """
        if options['subcommand'] == 'start':
            SupervisorCTL(**options).start()
        elif options['subcommand'] == 'stop':
            SupervisorCTL(**options).stop()
        elif options['subcommand'] == 'restart':
            SupervisorCTL(**options).restart()
        elif options['subcommand'] == 'update':
            SupervisorCTL(**options).reload()
        else:
            print(self.help)
