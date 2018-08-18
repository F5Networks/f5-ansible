#!/usr/bin/env bash

set -x

: ${DOC_IMG:=f5devcentral/containthedocs:latest}

exec docker run -i \
  -v $PWD:/here --workdir /here \
  ${DOC_IMG} /bin/bash -s <<EOF
set -e

#echo "Installing project dependencies"
pip install --user -r requirements.readthedocs.txt

# - needed to put the inv command in path
export PATH=$PATH:/root/.local/bin

echo "Checking grammar and style"
write-good \$(find ./docs -name '*.rst') --so --no-illusion --thereIs --cliches

echo "Building docs with Sphinx"
make -C docs/ clean
inv docs.build

echo "Checking links"
make -C docs/ linkcheck
EOF
