#!/bin/sh
#
# Copyright (c) 2017 F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


found=''

findings=$(egrep "self.want = Parameters\(self.module.params\)" ansible_collections/f5networks/f5_modules/plugins/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "Changes\(changed" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "ReportableChanges\(self.changes." library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "ApiParameters\(result\)" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "Parameters\(dict\(d" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "ApiParameters\(changed\)" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "Parameters\(resource.attrs\)" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "= ApiParameters\(params\)" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "= ModuleParameters\(args\)" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "Parameters\(changed\)" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "ApiParameters\(args\)" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "NetworkedParameters\(args\)" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "NonNetworkedParameters\(args\)" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "ApiParameters\(load_fixture" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "Parameters\(load_fixture" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

findings=$(egrep "Parameters\(result\)" library/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

if [ "${found}" ]; then
    echo "One or more file(s) listed above contain a Parameters without keywords."
    exit 1
fi
