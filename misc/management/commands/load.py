from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

import os


class Command(BaseCommand):
    help = "Load test data."

    def handle(self, *args, **options):
        call_command('loaddata', *tuple(os.listdir(os.path.join(settings.BASE_DIR, 'misc', 'fixtures'))))
        self.stdout.write(self.style.SUCCESS("[OK] - Load initial data."))
