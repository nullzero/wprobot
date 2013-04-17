#!/bin/dash
# replace all variables for your need
logfile=/data/project/userdata/nullzero/moveCategory.log

echo "Started bot on `hostname` at `date`" >> $logfile

#here is a startup for your bot - example is bellow, commented
python /data/project/userdata/nullzero/wprobot/scripts/moveCategory.py -bot:Nullzerobot >> /dev/null 2>&1

echo "Stopped the bot at `date`" >> $logfile
exit 0
