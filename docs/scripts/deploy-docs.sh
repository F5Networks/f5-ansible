#!/usr/bin/env bash

# Don't set -x
# we need to keep the secrets AWS variables out of the logs

env | grep -E "^(PATH=)" > .env_travis
env | grep -E "^(AWS_)" >> .env_travis

exec docker run --rm -i -v $PWD:$PWD --workdir $PWD --env-file=.env_travis f5devcentral/containthedocs "$@"
