#!/bin/bash


set -x

cd local/ansible
source hacking/env-setup
ansible-test sanity --test validate-modules
ansible-test sanity --test pep8
