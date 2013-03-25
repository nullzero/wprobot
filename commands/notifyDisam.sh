#!/bin/bash
#$ -l h_rt=INFINITY
#$ -l virtual_free=20M
#$ -l arch=*
#$ -o $HOME/notifyDisam.o.log
#$ -e $HOME/notifyDisam.e.log
#$ -N notifyDisam

/usr/bin/python $HOME/wprobot/scripts/notifyDisam.py -bot:Nullzerobot
