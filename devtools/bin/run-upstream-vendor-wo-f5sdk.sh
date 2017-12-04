#!/bin/bash

# Runs upstream vendor tests
#
# Assumes that you have ansible `git clone`d to `local/ansible`
#
# First parameter is the module
#

MODULE=$1
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && cd .. && pwd )"

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run --rm py2.7-bare ./devtools/bin/uv-check.sh ${MODULE} 2.7
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run --rm py3.5-bare ./devtools/bin/uv-check.sh ${MODULE} 3.5
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run --rm py3.6-bare ./devtools/bin/uv-check.sh ${MODULE} 3.6
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run --rm py2.7-bare /usr/local/bin/nosetests local/ansible/test/units/modules/network/f5/test_${MODULE}.py
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

echo "SUCCESS"
