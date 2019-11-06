#!/bin/sh
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


found=''

findings=$(egrep "default: None" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

if [ "${found}" ]; then
    echo "One or more file(s) listed above contain an unnecessary 'default: None'."
    exit 1
fi
