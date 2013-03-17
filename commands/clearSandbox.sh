#!/bin/bash
#$ -l h_rt=0:05:00
#$ -l virtual_free=20M
#$ -l arch=*
#$ -l fs-user-store=1

/usr/bin/python $HOME/rewrite/pwb.py $HOME/wprobot/script/clearSandbox.py
