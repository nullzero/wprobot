#!/bin/bash
#$ -l h_rt=0:05:00
#$ -l virtual_free=20M
#$ -l arch=*
#$ -o $HOME/clearSandbox.log
#$ -e $HOME/clearSandbox.log
#$ -N clearSandbox

/usr/bin/python $HOME/wprobot/scripts/clearSandbox.py -bot:Nullzerobot
