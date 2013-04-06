#!/bin/bash
#$ -l h_rt=1:30:00
#$ -l virtual_free=512M
#$ -l arch=*
#$ -o /dev/null
#$ -e /dev/null
#$ -N topEdits

/usr/bin/python $HOME/wprobot/scripts/topEdits.py -bot:Nullzerobot
