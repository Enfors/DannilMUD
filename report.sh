#!/bin/sh

find . -name "*.py" | grep -v attic | grep -v dml.py \
    | grep -v __init__.py | grep -v /test/ | xargs wc
