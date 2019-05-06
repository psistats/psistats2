#!/bin/bash
set -e
set -v
set -x

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
PROJECT_DIR="$( realpath $SCRIPT_DIR/../.. )"

echo "Script: $SCRIPT_DIR"
echo "Project: $PROJECT_DIR"

FPM_OPTS="--python-bin python3 -s python -t deb"
FPM_OPTS="$FPM_OPTS --python-package-name-prefix=python3"

cd $PROJECT_DIR

while IFS= read -r var
do
    echo "$var"
    fpm $FPM_OPTS $var
done < "requirements.txt"

