from db_maintenance_client import client
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    # General help message displayed when running:
    # manage.py dooptimizermaintenance -h
    help = ("Move the existing slow query log and cause the server to "
           "flush logs")

    def handle(self, *args, **options):
        try:
            my_client = client.DbMaintenaceClient()
            my_client.rotate_slow_query_log()
        except:
            raise
