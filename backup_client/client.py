import pyrax, datetime, gzip, hashlib, logging, os, platform, time, sys
from django.conf import settings

class BackupClient(object):
    """ Backup client controlled by cron, reporting to a utility server """

    def __init__(self):
        """Create a logger and setup connection to Rackspace Cloudfiles."""
        # Set up a logger to track what is going on in case there is a problem
        self.logger = logging.getLogger("backup_client")
        handle = logging.FileHandler(settings.BACKUP_LOG_FILE_LOCATION)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handle.setFormatter(formatter)
        self.logger.addHandler(handle)
        self.logger.setLevel(logging.INFO)
        # set name of backup file and its zipped version
        self._hostname = platform.node()
        self._set_backup_file_name()
        self._timestamp = str(datetime.datetime.now())
        # get a cloudfiles connection
        try:
            self.logger.info("********** Start Backup **********")
            self.logger.info("Establishing connection to Cloudfiles")
            # Establish a connection to Rackspace
            pyrax.set_setting("identity_type", "rackspace")
            self.conn = pyrax.set_credentials(
                settings.CLOUDFILES_USER, settings.CLOUDFILES_API_KEY)
            # Get a connection to cloudfiles for reading and writing.
            self.cf = pyrax.cloudfiles
        except:
            msg = "Unable to establish a connection to cloudfiles"
            self.logger.exception(msg)
            raise CloudfileConnectionError(msg)

    def local_backup(self):
        """Make a local export of the database using mysqldump and compress it
        with gzip."""
        if self._free_disk():
            self.logger.info("Disk space is good, creating backup at %s" %
                             self.backup_file_name)
            cmd = ("mysqldump %s --user %s -p%s --single-transaction "
                   "--opt | gzip > %s" % (settings.DATABASES['default']['NAME'],
                   settings.DATABASES['default']['USER'],
                   settings.DATABASES['default']['PASSWORD'],
                   self.zip_file_full_path))
            dump_status = os.system(cmd)
            if dump_status:
                msg = ("mysqldump returned an error, check %s for mysqldump "
                       "command to assist in troubleshooting" %
                       settings.BACKUP_LOG_FILE_LOCATION)
                self.logger.exception(msg)
                self.logger.exception(cmd)
                raise MysqldumpError(msg)

            self.logger.info("Backup started: %s" % cmd)

            self._compressed_size = str(os.stat(self.zip_file_full_path).st_size)
            self.logger.info("gzip compression complete size (bytes): %s" %
                self._compressed_size)
        else:
            msg = "Not enough space on drive to safely create backup, aborting"
            self.logger.exception(msg)
            raise NotEnoughDiskSpaceError(msg)


    def cloudfile_backup(self):
        """write the local compressed backup file to cloudfiles."""
        self.logger.info("Writing file to remote storage")
        try:
            backup = self.cf.upload_file(
                settings.CLOUDFILES_ARCHIVE_CONTAINER, self.zip_file_full_path,
                ttl=86400 * settings.CLOUDFILES_BACKUP_EXPIRY_DAYS)

            # Write the metadata
            metadata = {"timestamp":self._timestamp,
                        "hostname":self._hostname,
                        "compressed-size":self._compressed_size}
            self.cf.set_object_metadata(
                settings.CLOUDFILES_ARCHIVE_CONTAINER, backup, metadata)



        except:
            msg = ("Unable to write to remote storage failed:  %s" %
                 sys.exc_info()[0])
            self.logger.exception(msg)
            raise CloudfileWriteError(msg)


    def clean_up(self):
        """Delete local files (do I want to create a sub-directory in /tmp?)"""
        self.logger.info("Cleaning up local files.")
        try:
            os.remove(self.zip_file_full_path)
            self.logger.info("%s removed" % self.zip_file_full_path)
        except:
            msg = ("A problem has occurred with the removal of %s \n" %
                  self.zip_file_full_path)
            self.logger.exception(msg)
            raise CleanUpTmpFilesError(msg)

    def _free_disk(self):
        """Return true if there is more 10% of available disk space.  This
        is only a quick and dirty check."""
        self.logger.info("Checking available disk space")
        bEnoughSpace = True
        s = os.statvfs("/")
        bytes_available = s.f_bavail * s.f_frsize
        total_available = s.f_blocks * s.f_frsize
        self.logger.info("Bytes available on disk: %s" % str(bytes_available))

        #If less than 10% of disk space is avaialbe there is not enough space
        if bytes_available < 0.1 * total_available:
            bEnoughSpace = False
        return bEnoughSpace


    def _set_backup_file_name(self):
        """Set the local names and paths for the local files."""

        # While unusual, backups may be made on the same day (e.g if a risky
        # maintenance task is taking place, so we will attach a hash for
        # create unique names
        hash = hashlib.md5(str(time.time())).hexdigest()

        # Include a sortable file date in the file name for determining when
        # to remove archives
        now = datetime.datetime.now()
        file_date = now.strftime("%y%m%d")

        # The name of the local file on disk of the logical backup
        self.backup_file_name = ("%s_%s_%s.dmp" % (self._hostname, file_date,
                                                str(hash)[0:6]))
        # full path to the local file.
        self.backup_file_full_path = "%s%s" % (settings.BACKUP_LOCAL_TARGET_DIR,
                                               self.backup_file_name)
        # name of the file after being zipped.  It is this file that gets
        # written to cloudfiles
        self.zip_file_name = "%s.gz" % self.backup_file_name

        # We want to delete this file after
        # it has been written to cloud files.
        self.zip_file_full_path = "%s.gz" % self.backup_file_full_path


class CloudfileConnectionError(Exception):
    pass


class CloudfileWriteError(Exception):
    pass


class MysqldumpError(Exception):
    pass


class NotEnoughDiskSpaceError(Exception):
    pass


class CleanUpTmpFilesError(Exception):
    pass
