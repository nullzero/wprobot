#!/bin/bash
#$ -l h_rt=INFINITY
#$ -l virtual_free=20M
#$ -l arch=*
#$ -o $HOME/wprobot/tmp/out
#$ -e /dev/null
#$ -N DYKCheck

/usr/bin/python $HOME/wprobot/scripts/DYKCheck.py -bot:Nullzerobot
