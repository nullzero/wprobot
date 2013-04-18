#!/bin/bash
#$ -l h_rt=INFINITY
#$ -l virtual_free=20M
#$ -l arch=*
#$ -o /dev/null
#$ -e /dev/null
#$ -N notifyDisam

/usr/bin/python $HOME/wprobot/scripts/notifyDisam.py -bot:Nullzerobot
