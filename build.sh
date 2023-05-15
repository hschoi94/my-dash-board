#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install --upgrade pip

pip install -r requirements.txt

# #!/bin/sh
# grep ^VER= $PWD/.env | . /dev/stdin
# echo "$VER"  # => alpine
# echo 'PARAM:' $0
# RELATIVE_DIR=`dirname "$0"`
# echo 'Dir:' $RELATIVE_DIR

# cd $RELATIVE_DIR
# SHELL_PATH=`pwd -P`
# echo $SHELL_PATH

# # docker build -t 192.168.219.101:5010/node-container:v1.0 .
# docker build -t node-container:$VER .
# echo "builder"
# # docker push 192.168.219.101:5010/node-container:v.10
