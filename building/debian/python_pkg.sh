#!/bin/bash

set -e
set -v
set -x

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
PROJECT_DIR="$( realpath $SCRIPT_DIR/../.. )"

echo "Script: $SCRIPT_DIR"
echo "Project: $PROJECT_DIR"

cd $PROJECT_DIR

PKG_NAME=psistats2
PKG_VERSION="$( python setup.py --version )"
PKG_TARBALL=$PKG_NAME-$PKG_VERSION.tar.gz
PKG_FULLNAME=$PKG_NAME-$PKG_VERSION


FPM_OPTS="--python-bin python3 --no-python-fix-name --verbose"
FPM_OPTS="$FPM_OPTS --python-package-name-prefix=python3"
FPM_OPTS="$FPM_OPTS --python-obey-requirements-txt -s python"
FPM_OPTS="$FPM_OPTS --config-files etc/psistats2.conf"
FPM_OPTS="$FPM_OPTS --before-install packaging/linux/preinstall.sh"
FPM_OPTS="$FPM_OPTS --python-install-bin /usr/local/bin"
FPM_OPTS="$FPM_OPTS --after-remove packaging/linux/postuninstall.sh"
FPM_OPTS="$FPM_OPTS --deb-systemd packaging/linux/psistats2.service"
FPM_OPTS="$FPM_OPTS -t deb ./setup.py"

rm -rf dist
python setup.py sdist
cd dist
tar -xzf $PKG_TARBALL
cd $PKG_FULLNAME
fpm $FPM_OPTS

