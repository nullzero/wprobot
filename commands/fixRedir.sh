#!/bin/bash
#$ -l h_rt=1:00:00
#$ -l virtual_free=20M
#$ -l arch=*
#$ -o $HOME/fixRedir.o.log
#$ -e $HOME/fixRedir.e.log
#$ -N fixRedir

/usr/bin/python $HOME/rewrite/pwb.py $HOME/rewrite/scripts/redirect.py both -fullscan -moves -always -dir:$HOME/wprobot/bots/Nullzerobot
/usr/bin/python $HOME/rewrite/pwb.py $HOME/rewrite/scripts/redirect.py broken -always -dir:$HOME/wprobot/bots/Nullzerobot
/usr/bin/python $HOME/rewrite/pwb.py $HOME/rewrite/scripts/redirect.py double -always -dir:$HOME/wprobot/bots/Nullzerobot
