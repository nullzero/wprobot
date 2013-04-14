#!/bin/bash
#$ -l h_rt=0:05:00
#$ -l virtual_free=20M
#$ -l arch=*
#$ -o /dev/null
#$ -e /dev/null
#$ -N requestArts

/usr/bin/python $HOME/wprobot/scripts/requestArts.py -bot:Nullzerobot
