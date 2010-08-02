#!/bin/sh

find . -name "*.py" | grep -v attic | grep -v dml.py \
    | grep -v __init__.py | xargs wc -l
