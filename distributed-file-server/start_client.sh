#!/usr/bin/env bash
# Get the script path so it can be called from other directories
CURRENT_DIRECTORY=$(dirname $0)

python ${CURRENT_DIRECTORY}/client_main.py
find . -name '*.pyc' -delete
