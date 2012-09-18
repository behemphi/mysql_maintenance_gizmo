from db_maintenance_client import client
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

class Command(BaseCommand):
    # List of options accepted by this command
    option_list = BaseCommand.option_list + (
        make_option("--analyze",
            dest="analyze",
            default=False,
            help=("Analyze tables to update optimizer statistics. "
                 "Use 'all' to analyze all tables, or a comma separated"
                 "list to specify one or more tables")
        ),
        make_option("--check",
            dest="check",
            default=False,
            help=("Check indexes against tables and data/indexes "
                 "for corruption.  "
                 "Use 'all' to analyze all tables, or a comma separated"
                 "list to specify one or more tables")
        ),
        make_option("--optimize",
            dest="optimize",
            default=False,
            help=("Rebuild the table to update index statistics and "
                 "free unused space in the clustered index."
                 "Use 'all' to analyze all tables, or a comma separated"
                 "list to specify one or more tables")
        ),
    )
    # General help message displayed when running:
    # manage.py dooptimizermaintenance -h
    help = ("Causes the database tables to be analyzed, checked or "
           "optimized as specified by the options")
    # Short description of options for usage message
    args = ("[--analyze=comma separated list of tables] "
           "[--check=comma=separated list of tables] "
           "[--optimize=comma separated list of tables]")


    def _get_table_list(self,args):
        if args == "all":
            args = ""
        else:
            args = args.split(",")
        
        return args


    def handle(self, analyze, optimize, check, **options):
        try:
            c = client.DbMaintenaceClient()
            if analyze:
                args = self._get_table_list(analyze)
                c.optimizer_maintenance("analyze", args)

            if check:
                args = self._get_table_list(check)
                c.optimizer_maintenance("check", args)

            if optimize:
                args = self._get_table_list(optimize)
                c.optimizer_maintenance("optimize", args)

        except:
            raise
