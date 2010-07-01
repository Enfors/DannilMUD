#!/bin/sh
# start.sh - Start script for DannilMUD

cd $(dirname $0)

export PYTHONPATH=$PYTHONPATH:$(pwd)

./driver.py
