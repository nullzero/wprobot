#!/bin/dash
#$ -o /dev/null
#$ -e /dev/null

logfile=/data/project/userdata/nullzero/syslog
echo "Started bot on `hostname` at `date`" >> $logfile

python /data/project/pywikipedia/rewrite/pwb.py /data/project/pywikipedia/rewrite/scripts/redirect.py both -fullscan -moves -always -log -dir:/data/project/userdata/nullzero/wprobot/bots/Nullzerobot >> /dev/null 2>&1
python /data/project/pywikipedia/rewrite/pwb.py /data/project/pywikipedia/rewrite/scripts/redirect.py broken -always -log -dir:/data/project/userdata/nullzero/wprobot/bots/Nullzerobot >> /dev/null 2>&1
python /data/project/pywikipedia/rewrite/pwb.py /data/project/pywikipedia/rewrite/scripts/redirect.py double -always -log -dir:/data/project/userdata/nullzero/wprobot/bots/Nullzerobot >> /dev/null 2>&1

echo "Stopped the bot at `date`" >> $logfile
exit 0
