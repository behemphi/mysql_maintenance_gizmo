import logging, os, platform

from django.conf import settings
from django.db import connection
from os import rename
from os import system
from os import getenv

class DbMaintenaceClient(object):
    """ Maintenance client controlled by cron, and reporting to utility server
        for the analyze, optimize and check of tables in the customer
        database"""
    _database = settings.DATABASES["default"]["NAME"]

    def __init__(self):
        self._logger = logging.getLogger("db_maintenance_client")
        handle = logging.FileHandler(settings.DB_MAINTENANCE_LOG_FILE_LOCATION)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handle.setFormatter(formatter)
        self._logger.addHandler(handle)
        self._logger.setLevel(logging.INFO)
        # Get a database connection
        try:
            self._logger.info("Establishing connection to MySQL locally")
            self._cur_status = connection.cursor()
        except OperationalError as (errno, strerror):
            msg = "Unable to establish a connection to MySQL locally"
            self._logger.error(msg)
            msg = "Error #: %s:%s" %(errno, strerror)
            self._logger.error(msg)
            raise MysqlConnectionError()


    def _get_tables(self):
        self._cur_status.execute("show tables from " + self._database)
        all_tables = self._cur_status.fetchall()
        table_list = []
        for table in all_tables:
            table_list.append(table[0])

        self._tables = table_list


    def _dict_cursor(self,raw_rs):
        column_name = [x[0] for x in self._cur_status.description]
        rs = []
        for row in raw_rs:
             rs.append(dict(zip(column_name, row)))
        return rs

        
    def _log_response(self, stmt, results):
       # print result
        for result in results:
            if result["Msg_type"] == "status":
                if result["Msg_text"] == "OK":
                    self._logger.info(result)
                else:
                    self._logger.error(
                        "A problem occurred for command: %s" % stmt)
                    self._logger.error(result)


    def optimizer_maintenance(self, command, tables=[]):
        self._logger.info(
            "# --------------------------------------------------")
        self._logger.info("%s operation on tables" % command)
        self._logger.info(
            "# --------------------------------------------------")
        self._get_tables()

        # All tables or a custom list
        if not len(tables):
            self._get_tables()
        else:
            self._tables = tables

        # OK, analyze them and log the results
        for table in self._tables:
            stmt = command + " TABLE %s.%s" % (self._database, table)
            self._cur_status.execute(stmt)
            raw_rs = self._cur_status.fetchall()
            dict_rs =  self._dict_cursor(raw_rs)
            self._log_response(stmt, dict_rs)


    def rotate_slow_query_log(self,hostname=""):
        self._logger.info(
            "# --------------------------------------------------")
        self._logger.info("rotating slow query log")
        self._logger.info(
            "# --------------------------------------------------")
        # check if file exists
        if len(hostname) == 0:
            hostname = platform.node()

        slow_log_path = settings.DB_MAINTENANCE_SLOW_LOG_PATH
        old_log_path = "%s-old" % slow_log_path
        
        try:
            os.rename(slow_log_path,old_log_path)
            self._logger.info("moved file %s to %s" % (
                slow_log_path, old_log_path))
            flush = True
        except:
            self._logger.error("a problem has occurred while rotating the "
                "slow query log")
            self._logger.error("check and see if %s exists" % slow_log_path)
            flush = False
            raise
        
        if flush:
            self._logger.info("flushing logs")
            cmd = "mysqladmin --user %s -p%s flush-logs" % (
                settings.DATABASES["default"]["NAME"],
                settings.DATABASES["default"]["PASSWORD"])
            flush_status = os.system(cmd)
            if flush_status:
                msg = ("mysqladmin returned an error, check %s for "
                       "mysqldump command to assist in troubleshooting" %
                       settings.DB_MAINTENANCE_LOG_FILE_LOCATION)
                self.logger.error(msg)
                self.logger.error(cmd)
                raise MysqladminError(msg)

class MysqlConnectionError(Exception):
    pass


class MysqladminError(Exception):
    pass
