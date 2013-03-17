#!/bin/bash
#$ -l h_rt=0:05:00
#$ -l virtual_free=20M
#$ -l arch=*
#$ -l fs-user-store=1
#$ -N clearSandbox

/usr/bin/python $HOME/rewrite/pwb.py $HOME/wprobot/script/clearSandbox.py -dir:$HOME/wprobot/bots/Nullzerobot
#/usr/bin/python $HOME/rewrite/pwb.py $HOME/rewrite/scripts/replace.py -page:วิกิพีเดีย:ทดลองเขียน -regex "(?s)^.*$" "$RANDOM" -dir:$HOME/wprobot/bots/Nullzerobot -always
