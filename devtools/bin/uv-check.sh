#!/bin/bash

MODULE=$1
PYTHON_VER=$2

pip install virtualenv
cd local/ansible
source hacking/env-setup
ansible-test units --python ${PYTHON_VER} ${MODULE}
ansible-test sanity --test import --python ${PYTHON_VER} ${MODULE}
