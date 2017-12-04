#!/bin/bash

# Runs tests for a module using all harnesses and python versions.
#
# This is only relevant for your local device when suing VirtualBox VMs.
# It expects that you have created the VMs with Vagrant, waited for the
# to boot, and created Snapshots of them.
#

MODULE=$1
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && cd .. && pwd )"
HARNESS=(
    bigip-12.0.0 bigip-12.1.0 bigip-12.1.0-hf1 bigip-12.1.0-hf2
    bigip-12.1.1 bigip-12.1.1-hf1 bigip-12.1.1-hf2 bigip-12.1.2
    bigip-12.1.2-hf1 bigip-13.0.0 bigip-13.0.0-hf1 bigip-13.0.0-hf2
    )
PYTHONS=( py2.7 py3.5 py3.6)
HOST="localhost"
PORT="10443"
SNAPSHOT="Snapshot 1"

for i in "${HARNESS[@]}"
do
    VBoxManage controlvm ${i} poweroff
    VBoxManage snapshot ${i} restore "${SNAPSHOT}"
    sleep 3
    VBoxManage startvm ${i} --type headless

    for x in $(seq 1 10); do
        curl -k https://${HOST}:${PORT}/
        if [ $? -eq 0 ]; then
            break
        fi
        sleep 6
    done

    echo "Ready"

    for k in "${PYTHONS[@]}"
    do
        docker-compose -f "${DIR}/devtools/docker-compose.yaml" run --rm ${k} make $MODULE
        if [ $? -ne 0 ]; then
            VBoxManage controlvm ${i} poweroff
            echo "FAILED: ${k} - ${i}"
            exit 1
        fi
    done
    VBoxManage controlvm ${i} poweroff
done

echo "SUCCESS"
