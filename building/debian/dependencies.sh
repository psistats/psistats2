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
FPM_OPTS="$FPM_OPTS --python-install-lib=/usr/local/lib/python3/dist-packages"

cd $PROJECT_DIR
rm -rf $PROJECT_DIR/dist

mkdir $PROJECT_DIR/dist
mkdir $PROJECT_DIR/dist/debian_dependencies

cd $PROJECT_DIR/dist/debian_dependencies

while IFS= read -r var
do
    PKG_VERSION="$(echo $var | awk -F'>=' '{print $2}')"

    PKG_VERSION="$PKG_VERSION~psikon"
    PKG_VERSION="$PKG_VERSION$BUILD_NUMBER"

    echo "Version: $PKG_VERSION"
    echo "$var"
    fpm $FPM_OPTS --version $PKG_VERSION $var
done < "$PROJECT_DIR/requirements.txt"

