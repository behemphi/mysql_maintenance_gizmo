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
> git clone git@github.com:behemphi/mysql_maintenance_gizmo.git
```

Remember that it will _not_ work unless you are the mm_gizmo user, or you have decided to do the configuration 
for another user.

## Usage
From the command line, switch to the home directory of MySQL Mainteance Gizmo:

```bash
> cd /opt/mysql_maintenance_gizmo
```

### Creating a Logical Database Backup
MM Gizmo performs the following actions to backup your database:
* Creates a non-locking (--single-transaction) logical (mysqldump) backup the specified schema to the /tmp directory
* Zips this file
* Ships this file with an expiry header to Rackspace Cloudfiles
* deletes the files in /tmp
* logs its steps along the way to the file specified in the configuration above
 
```bash
> ./manage.py dobackup
```

Note that while the database is available during the backup, load is placed on the server.  Understand what your
machine is capable of and what your business requirements are for data retention and uptime.  Any backup process can 
bring down a busy machine, this one is no exception.

### Rotating the Slow Query Log
If you have the slow query log on it is a fair statement that if you haven't looked in the last _n_ days where _n_ is
the usual number of days between releases, then likely it is not worth caring what is in this log.  

The `rotateslowquerylog` job:
* moves the existing slow query log to the the same file name with `-old` appended
* uses mysqladmin to issue a `flush logs` command and reopening the slow log

If you have need of further use of your old file, be sure to move it as MM Gizmo will overwrite it the next time
the `rotateslowquerylog` job is run.

### Table Optimization
Tables in most databases should be optimized on a regular basis. MM Gizmo facilitates this by:
* getting a list of tables for the specified schema
* Issuing the indicated command 
* Logging its actions and MySQL's response to the file specified in the configuration above

To analyze all tables in the schema use the command like this:
```bash
> ./manage.py dooptimizermaintenance --analyze=all
```
To analyze only specific tables in the schema list tables separated by commas with no spaces
```bash
> ./manage.py dooptimizermaintenance --analyze=table1,table2,table3
```

The `optimize` and `check` commands are also available.  Check the MySQL documentation for the effect of
these commands for your version and storage engine.  

Again, a word of warning.  Optimize and Check are _very_ heavy operations that can cause queries on to 
wait while they do their job (i.e. the get a write lock on a whole table).  Be sure you think about what 
you are doing and when you are doing it before issuing the command.


