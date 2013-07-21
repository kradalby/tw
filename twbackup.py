#!/bin/python

import sys, os
from datetime import datetime


#Server settings
HOSTNAME = "<removed>"
USERNAME = "<removed>"
REMOTEBACKUPDIR = "/storage/backup/klatrerosen/"

DATE = datetime.now()
FILENAME = "tupo_backup"
BACKUPDIR = "/home/kontor/backup/"
#DIRS = "/home/kontor/test"
DIRS = "/home/home/data/tupo"
WEEKDAY = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
MONTH = ("january","february","march","april","may","june","july","august","september","october","november","december")

def validate_arg(arg):
    if arg == "--week" or arg == "--weekday" or arg == "--month":
        return True
    else:
        return False

def getweek(date):
    if date.day >= 1 and date.day <= 7:
        return "week1"
    elif date.day >= 8 and date.day <= 14:
        return "week2"
    elif date.day >= 15 and date.day <= 21:
        return "week3"
    elif date.day >= 22 and date.day <= 28:
        return "week4"
    elif date.day >= 29 and date.day <= 31:
        return "week5"
        
def getweekday(date):
    return str(WEEKDAY[date.weekday()])

def getmonth(date):
    return str(MONTH[date.month-1])

def backup(x):
    if x in ("week1","week2","week3","week4","week5"):
        filename = FILENAME+"_"+x+".tar"
        try:
            os.remove(BACKUPDIR+filename+".bz2")
        except OSError:
            print "File is not here, duh"
    else:
        filename = FILENAME+"_"+x+"_"+DATE.strftime("%d_%m_%Y")+".tar"
    os.system("tar -cv %s > %s" % (DIRS, BACKUPDIR+filename))
    os.system("bzip2 -9 %s" % BACKUPDIR+filename)


#this is not finished as the server is not up and running.
def ship():
    os.system("rsync -azv --progress " + BACKUPDIR + "* -e ssh " + USERNAME + "@" + HOSTNAME + ":" + REMOTEBACKUPDIR)

def main():
    if (len(sys.argv) > 1) and validate_arg(str(sys.argv[1])):
        arg = str(sys.argv[1])
        if arg == "--week":
            backup(getweek(DATE))
        elif arg == "--weekday":
            backup(getweekday(DATE))
        elif arg == "--month":
            backup(getmonth(DATE))
        ship()
    else:
        print "This is not a valid argument, valid arguments are: --week, --weekday and --month"

main()

