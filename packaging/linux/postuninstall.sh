#!/bin/bash

set -x
set -v

PKG_USER=psistats2
PKG_GROUP=psistats2

getent passwd $PKG_USER > /dev/null
if [ $? -eq 0 ]; then
    echo "$PKG_USER user exists"
    deluser $PKG_USER
else
    echo "$PKG_USER user does not exist"
fi


getent group $PKG_GROUP > /dev/null
if [ $? -eq 0 ]; then
    echo "$PKG_GROUP group exists"
    delgroup $PKG_GROUP
else
    echo "$PKG_GROUP group does not exist"
fi

