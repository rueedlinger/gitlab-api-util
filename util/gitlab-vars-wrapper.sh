#!/bin/sh
#SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCRIPT_DIR="/usr/src/app"
python $SCRIPT_DIR/gitlab_vars.py $@