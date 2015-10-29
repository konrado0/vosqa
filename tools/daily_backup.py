#!/usr/bin/python
from subprocess import check_output, CalledProcessError
import shlex, os
from datetime import date, datetime

BACKUP_DIR = '/home/dressbook/backup'
NUMBER_OF_DAILY_BACKUPS = 3
NUMBER_OF_WEEKLY_BACKUPS = 2
NUMBER_OF_MONTHLY_BACKUPS = 2

def get_backup(directory, filename):
    os.chdir(directory)
    try:
        cmd = "ssh dressbook@151.236.220.50 'pg_dump osqa > /home/dressbook/Programming/dressbook/osqa/forum/upfiles/osqadb.sql'"
        check_output(shlex.split(cmd))
    except CalledProcessError as e:
        print "Failed to create backup: ", e.output
        exit(1)
    try:
        cmd = "rsync -ahvz --exclude 'upfiles/cache/*' --delete dressbook@45.56.103.67:/home/dressbook/Programming/dressbook/osqa/forum/upfiles ."
        check_output(shlex.split(cmd))
    except CalledProcessError as e:
        print "Failed to download backup: ", e.output
        exit(1)
    try:
        cmd = "tar -cjf %s upfiles" % filename
        check_output(shlex.split(cmd))
    except CalledProcessError as e:
        print "Failed to download backup: ", e.output
        exit(1)

def create_directory_structure(directory):
    if not os.path.isdir(directory):
        print "Directory ", directory, " does not exist, will create it"
        os.mkdir(directory)
    if not os.path.isdir(directory+'/daily'):
        os.mkdir(directory+'/daily')
    if not os.path.isdir(directory+'/monthly'):
        os.mkdir(directory+'/monthly')
    if not os.path.isdir(directory+'/weekly'):
        os.mkdir(directory+'/weekly')

daily_backup_format = "%s/daily/%s.tar.bz2"
daily_backup = "%s/daily/%s"
weekly_backup_format = "%s/weekly/%s.tar.bz2"
weekly_backup = "%s/weekly/%s"
monthly_backup_format = "%s/monthly/%s.tar.bz2"
monthly_backup = "%s/monthly/%s"

def save_today_backup(directory):
    today = date.today()
    today_backup = daily_backup_format % (directory, str(today))
    if os.path.exists(today_backup):
        print "Today backup already saved"
    else:
        get_backup(directory, today_backup)
    return today_backup
    
def update_backups_structure(directory, today_backup):
    today = date.today()
    files = os.walk(directory+"/daily/").next()[2]
    if len(files) > NUMBER_OF_DAILY_BACKUPS:
        os.remove(daily_backup % (directory, min(files)))
        
    #weekly
    files = os.walk(directory+"/weekly/").next()[2]
    if len(files) == 0:
        os.link(today_backup, weekly_backup_format %(directory,str(today)))
    else:
        last_weekly_date = datetime.strptime(max(files).replace('.tar.bz2',''), '%Y-%m-%d').date()
        if (today-last_weekly_date).days >= 7:
            os.link(today_backup, weekly_backup_format %(directory,str(today)))
            if len(files) == NUMBER_OF_WEEKLY_BACKUPS:
                os.remove(weekly_backup % (directory, min(files)))
    
    #monthly
    files = os.walk(directory+"/monthly/").next()[2]
    if len(files) == 0:
        os.link(today_backup, monthly_backup_format %(directory,str(today)))
    else:
        last_monthly_date = datetime.strptime(max(files).replace('.tar.bz2',''), '%Y-%m-%d').date()
        if (today-last_monthly_date).days >= 30:
            os.link(today_backup, monthly_backup_format %(directory,str(today)))
            if len(files) == NUMBER_OF_MONTHLY_BACKUPS:
                os.remove(monthly_backup % (directory, min(files)))

if __name__ == '__main__':
    print "Creating daily backup on ", str(date.today())
    create_directory_structure(BACKUP_DIR)
    today_backup = save_today_backup(BACKUP_DIR)
    update_backups_structure(BACKUP_DIR, today_backup)
    print "Backup saved succesfully in ", BACKUP_DIR
    