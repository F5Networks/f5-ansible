#!/bin/bash

# Runs upstream vendor tests
#
# Assumes that you have ansible `git clone`d to `local/ansible`
#
# First parameter is the module
#

MODULE=$1
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && cd .. && pwd )"

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run --rm py2.7 pycodestyle library/${MODULE}.py
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run --rm py2.7 pycodestyle test/unit/test_${MODULE}.py
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run --rm py2.7 ./devtools/bin/uv-check.sh ${MODULE} 2.7
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run --rm py3.5 ./devtools/bin/uv-check.sh ${MODULE} 3.5
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run --rm py3.6 ./devtools/bin/uv-check.sh ${MODULE} 3.6
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run --rm py2.7 ./devtools/bin/uv-check2.sh
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run --rm py2.7 bash test/ansible/sanity/integration-test-idempotent-names.sh
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

docker-compose -f "${DIR}/devtools/docker-compose.yaml" run --rm py2.7 python test/ansible/sanity/short-description-ends-with-period.py
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
fi

echo "SUCCESS"
