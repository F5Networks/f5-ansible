#!/usr/bin/env bash

set -x

: ${DOC_IMG:=f5devcentral/containthedocs:latest}

exec docker run -it \
  -v $PWD:$PWD --workdir $PWD \
  -e "LOCAL_USER_ID=$(id -u)" \
  ${DOC_IMG} "$@"
