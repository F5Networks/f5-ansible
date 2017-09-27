#!/bin/bash


set -x
MODULE=$1
PYTHON_VER=$2

cd local/ansible
source hacking/env-setup
ansible-test units --python ${PYTHON_VER} ${MODULE}
