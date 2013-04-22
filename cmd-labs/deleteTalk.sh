#!/bin/dash
#$ -o /dev/null
#$ -e /dev/null

logfile=/data/project/userdata/nullzero/syslog
echo "$0, Started bot on `hostname` at `date`" >> $logfile
python /data/project/userdata/nullzero/wprobot/scripts/DPL.py -bot:Nullzerobot >> /dev/null 2>&1
echo "$0, Stopped the bot at `date`" >> $logfile
exit 0
