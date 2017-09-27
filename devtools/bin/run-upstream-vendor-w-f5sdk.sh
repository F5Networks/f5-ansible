#!/bin/bash

# Runs upstream vendor tests
#
# Assumes that you have ansible `git clone`d to `local/ansible`
#
# First parameter is the module
#

set -x
MODULE=$1
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && cd .. && pwd )"

# Put the module to be merged in the upstream code
docker-compose -f "${DIR}/devtools/docker-compose.yaml" run py2.7.10 \
    ./scripts/copy-upstream.py ${MODULE}

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run py2.7.10 ./devtools/bin/uv-check.sh ${MODULE} 2.7
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run py3.5.4 ./devtools/bin/uv-check.sh ${MODULE} 3.5
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run py3.6.2 ./devtools/bin/uv-check.sh ${MODULE} 3.6
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run py2.7.10 ./devtools/bin/uv-check2.sh
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run py2.7.10 bash test/ansible/sanity/integration-test-idempotent-names.sh
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi


echo "SUCCESS"
