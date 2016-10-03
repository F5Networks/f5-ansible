#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
module=$1

# Create role containing all of your future functional tests
mkdir -p ${DIR}/../roles/__${module}/{defaults,tasks}

# Touch the playbook that will run your functional tests
touch ${DIR}/../playbooks/${module}.yaml

# Create default vars to contain any playbook variables
touch ${DIR}/../roles/__${module}/defaults/main.yaml

# Create default tasks file containing all your functional tests
touch ${DIR}/../roles/__${module}/tasks/main.yaml

# Create your new module python file
touch ${DIR}/../library/${module}.py

# Create the documentation link for your module
touch ${DIR}/../docs/modules/${module}.rst

# Stub out the test playbook
cat > ${DIR}/../playbooks/${module}.yaml << EOL
---

# Test the ${module} module
#
# Running this playbook assumes that you have a BIG-IP installation at the
# ready to receive the commands issued in this Playbook.
#
# This module will run tests against a BIG-IP host to verify that the
# ${module} module behaves as expected.
#
# Usage:
#
#    ansible-playbook -i notahost, playbooks/${module}.yaml
#
# Examples:
#
#    Run all tests on the ${module} module
#
#    ansible-playbook -i notahost, playbooks/${module}.yaml
#
# Tested platforms:
#
#    - NA
#

- name: Test the ${module} module
  hosts: f5-test
  connection: local

  roles:
      - __${module}
EOL