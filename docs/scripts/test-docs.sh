#!/usr/bin/env bash

set -e

#echo "Installing project dependencies"
#make requirements

echo "Building docs with Sphinx"
make -C clean || true
make docs

echo "Checking grammar and style"
write-good `find ./docs -name '*.rst'` --passive --so --no-illusion --thereIs --cliches

echo "Checking links"
make -C docs linkcheck
