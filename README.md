# mysql_maintenance_gizmo

A quick and dirty tool written for the Rackspace Cloud in Python/Django to do quick and dirty logical backups, log rotation, and table maintenance.  

## Setup

### Installation
It is assumed this code will be installed in /home/mysql_maintenance_gizmo.  If this is not the case be sure to adjust accordingly.

Need to create the user mm_gizmo as an ssh user on your system (no password or login privileges)
Need to grant privileges to this user to make a mysql dump:

```sql
mysql > grant insert,select on *.* to 'mm_gizmo'@'localhost' identified by 'MySuperSecretPassword'
```





## Usage
