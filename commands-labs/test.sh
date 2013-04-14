#!/bin/dash
# replace all variables for your need
logfile=/data/project/userdata/nullzero/syslog

echo "Started bot on `hostname` at `date`" >> $logfile

#here is a startup for your bot - example is bellow, commented
python /data/project/userdata/nullzero/scripts/test.py -bot:Nullzerobot >> $logfile 2>&1

echo "Stopped the bot at `date`" >> $logfile
exit 0
