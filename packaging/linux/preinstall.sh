#!/bin/bash

set -x
set -v


PKG_USER=psistats2
PKG_GROUP=psistats2

getent group $PKG_GROUP > /dev/null
if [ $? -eq 0 ]; then
    echo "$PKG_GROUP group exists"
else
    echo "$PKG_GROUP does not exist"
    addgroup $PKG_GROUP
fi

getent passwd $PKG_USER > /dev/null
if [ $? -eq 0 ]; then
    echo "$PKG_USER user exists"
else
    echo "$PKG_USER does not exist"
    adduser --system --ingroup $PKG_GROUP $PKG_USER
fi
