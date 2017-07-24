#!/bin/sh

found=''

findings=$(egrep "idempotent check" test/integration/ -R)
if [ "$findings" ]; then
    echo "${findings}"
    found=1
fi

if [ "${found}" ]; then
    echo "One or more file(s) listed above contain misspelled idempotent tasks."
    exit 1
fi
