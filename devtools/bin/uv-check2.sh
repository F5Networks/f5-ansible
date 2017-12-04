#!/bin/bash

cd local/ansible
source hacking/env-setup
ansible-test sanity --test validate-modules
ansible-test sanity --test pep8 2>&1 | grep '/f5/'
