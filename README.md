# Summary

Mysql Maintenance Gizmo is a quick and dirty tool written for the Rackspace Cloud in Python/Django to do 
* logical backups (saved to cloudfiles)
* slow query log rotation
* table maintenance (i.e. analyze, optimize, check)

The code is in python using the Django framework.  It is intended to be run from like this:

```bash
> ./manage.py dobackup
```

Configuration is done via a set of environment variables

```bash
export CLOUDFILES_USERNAME="myName"
```

In this file you will learn how to manually setup 

## Configuration

### Installation
It is assumed this code will be installed in /opt/mysql_maintenance_gizmo.  If this is not the case be 
sure to adjust accordingly.  It is assumed that the project home is on the same host as the database server.

First create the mm_gizmo, user, their directory and group.  Note the below is from a Ubuntu 10.04 session,
but the various flavors of *nix and *bsd, do this command very differently, so:

```bash
> sudo useradd -mU -d /home/mm_gizmo -g mysql -G mm_gizmo -s /bin/bash mm_gizmo
```

The user does not need a password.

The configuration of the system is done via the environment variables of the mm_gizmo user.  It is 
suggested that these show up as export commands in .profile, .bashrc or .bash_profile depending on
your flavor of operating system and prefereces.  A section at the end of the approriate file might 
look like:

```bash
# Exports for database connection
export DATABASE_SCHEMA_NAME="mySchema"
export DATABASE_USERNAME="mm_gizmo"
export DATABASE_PASSWORD="Secretshhhhh"
export DATABASE_HOST="localhost"
export DATABASE_PORT="3306"

# Exports for cloudfiles connections
export CLOUDFILES_USER="MyUser"
export CLOUDFILES_API_KEY="927defcdc23e2a74f3edef9ccb4b5aa"
export DATABASE_CLOUDFILES_ARCHIVE_CONTAINER="client-db-backup"

# specific to the MysqlMaintenanceGizmo
export MM_GIZMO_SECRET_KEY="(c$m7(405v@asd52^emb5o6hack$fubar-@*m-r)@m-hc0&mmm"
export MM_GIZMO_BACKUP_LOG_PATH="/var/log/mm_gizmo/mm_gizmo_backup.log"
export MM_GIZMO_MAINTENANCE_LOG_PATH="/var/log/mm_gizmo/mm_gizmo_maintenance.log"
export MM_GIZMO_SLOW_LOG_PATH="/var/log/mysql/slow_query.log"
```

Once you have put these variables in the file, save it and logout.  Log back in as the user and check the 
environment for the presence of your settings.

```bash
> sudo su -l mm_gizmo
> env
```

Next a mysql user specific to the task should be created:

```sql
mysql > grant insert,select,reload on *.* to 'mm_gizmo'@'localhost' identified by 'Secretshhhhh'
```

After issuing the grant, log out of MySQL and then log in as the mm_gizmo user

```bash
> mysql -umm_gizmo -pSecretshhhhh
```

Once verified that the suer 

Notice that the mysql user and password from the grant statement match those specified in the `DATABASE_USERNAME` 
and `DATABASE_PASSWORD` of the bash example.

### Installation
Just clone the repo to `/opt`.

```bash
> cd /opt
> git clone 
```




## Usage
