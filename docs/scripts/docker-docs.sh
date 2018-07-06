#!/usr/bin/env bash

set -x

: ${DOC_IMG:=f5devcentral/containthedocs:latest}

exec docker run -i \
  -v $PWD:/here --workdir /here \
  ${DOC_IMG} "$@"
