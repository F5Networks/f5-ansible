#!/usr/bin/env bash

set -x

: ${DOC_IMG:=f5devcentral/containthedocs:latest}

LOCAL_USER_ID=`id -u`
if [ $LOCAL_USER_ID -eq 0 ]; then
    LOCAL_USER_ID=10443
fi

exec docker run -i \
  -v $PWD:/here --workdir /here \
  -e "LOCAL_USER_ID=${LOCAL_USER_ID}" \
  ${DOC_IMG} "$@"
