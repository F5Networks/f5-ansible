#!/usr/bin/env bash

set -x

: ${DOC_IMG:=f5devcentral/containthedocs:latest}

LOCAL_USER_ID=`id -u`
if [ $LOCAL_USER_ID -eq 0 ]; then
    LOCAL_USER_ID=10443
fi

exec docker run -i \
  -v $PWD:/here --workdir /here \
  ${DOC_IMG} /bin/bash -s <<EOF
set -e

#echo "Installing project dependencies"
pip install --user -r requirements.readthedocs.txt

echo "Building docs with Sphinx"
make -C clean || true
make docs || true

echo "Checking grammar and style"
write-good \$(find ./docs -name '*.rst') --passive --so --no-illusion --thereIs --cliches 2>&1 > /dev/null || true

echo "Checking links"
make -C docs linkcheck || true
EOF
