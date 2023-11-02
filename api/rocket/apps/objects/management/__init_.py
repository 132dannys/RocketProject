from django.core.management import BaseCommand

from .commands import demo_db

BaseCommand.register_command(demo_db.Command)
