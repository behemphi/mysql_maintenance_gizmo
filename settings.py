# Django settings for backup project.
import platform
import os

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = True
TEMPLATE_DEBUG = DEBUG
# ------------------------------------------------------------------------------
# Global Settings
# ------------------------------------------------------------------------------
ADMINS = (
    ("Boyd Hemphill", "boyd@feedmagnet.com"),
)

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.mysql",
        "NAME": os.getenv("DATABASE_SCHEMA_NAME"),
        "USER": os.getenv("DATABASE_USERNAME"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": "localhost",
        "PORT": "3306",
    },
}
# ------
# Cloudfiles Details
# ------
# FM Cloudfiles user
CLOUDFILES_USER = os.getenv("CLOUDFILES_USER")
# FM Cloudfiles API key
CLOUDFILES_API_KEY = os.getenv("CLOUDFILES_API_KEY")
# FM Cloudfiles container for db archives
CLOUDFILES_ARCHIVE_CONTAINER = os.getenv(
    "DATABASE_CLOUDFILES_ARCHIVE_CONTAINER")
# Number of days before a backup should expire
CLOUDFILES_BACKUP_EXPIRY_DAYS = 8

# ------- End Local Global Settings --------------------------------------------


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "America/Chicago"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# MEDIA_ROOT = ""

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# MEDIA_URL = ""

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# ADMIN_MEDIA_PREFIX = "/media/"

# Make this unique, and don"t share it with anybody.
# SECRET_KEY = "$wseog_r-+0e81fv!^ysaq1ob2t1%nt$$c79j#k7=g&1o$bh@6"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
#     "django.template.loaders.eggs.Loader",
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
)

ROOT_URLCONF = "backup.urls"

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # 'C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don"t forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    # Uncomment the next line to enable the admin:
    "django.contrib.admin",
    # Uncomment the next line to enable admin documentation:
    "django.contrib.admindocs",
    "backup_client",
    "db_maintenance_client",
)


# ------------------------------------------------------------------------------
# Backup Client Section
# ------------------------------------------------------------------------------
# Absolute path of the log file.  Note the slash after feedmagnet that is
# required
BACKUP_LOG_FILE_LOCATION = ("/var/log/%s_backup_client.log"
    % platform.node())
# Directory the local backup will be written to
# must have trailing slash
BACKUP_LOCAL_TARGET_DIR = "/tmp/"

# ------------------------------------------------------------------------------
# DB Maintenance Section
# ------------------------------------------------------------------------------
# Absolute path of the log file.  Note the slash after feedmagnet that is
# required
DB_MAINTENANCE_LOG_FILE_LOCATION = ("/var/log/feedmagnet/"
    "%s_db_maintenance_client.log" % platform.node())
