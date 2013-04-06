#!/bin/bash
#$ -l h_rt=4:00:00
#$ -l virtual_free=20M
#$ -l arch=*
#$ -o /dev/null
#$ -e /dev/null
#$ -N moveCategory

/usr/bin/python $HOME/wprobot/scripts/moveCategory.py -bot:Nullzerobot
