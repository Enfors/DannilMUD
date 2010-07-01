#!/bin/sh
# start.sh - Start script for DannilMUD

gamedir=$(dirname $0)
dmdir=$(cd $gamedir/..; pwd)

export PYTHONPATH=$PYTHONPATH:$dmdir
echo PYTHONPATH=$PYTHONPATH

$gamedir/driver.py
