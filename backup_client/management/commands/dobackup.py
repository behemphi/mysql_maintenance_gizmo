from django.core.management.base import BaseCommand, CommandError
from backup_client import client

class Command(BaseCommand):
    help = "Run backup client to create mysql backup"

    def handle(self, *args, **options):
        try:
            my_client = client.BackupClient()
            my_client.local_backup()
            my_client.cloudfile_backup()
            my_client.clean_up()
        except:
            raise
