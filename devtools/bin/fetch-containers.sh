#!/bin/bash

DOCKER_REGISTRY=dockerhub

docker pull ${DOCKER_REGISTRY}/f5ansible/py2.7.10:devel
docker tag  ${DOCKER_REGISTRY}/f5ansible/py2.7.10:devel f5ansible/py2.7.10:devel
docker pull ${DOCKER_REGISTRY}/f5ansible/py2.7.10-bare:devel
docker tag  ${DOCKER_REGISTRY}/f5ansible/py2.7.10-bare:devel f5ansible/py2.7.10-bare:devel
docker pull ${DOCKER_REGISTRY}/f5ansible/py3.5.4:devel
docker tag  ${DOCKER_REGISTRY}/f5ansible/py3.5.4:devel f5ansible/py3.5.4:devel
docker pull ${DOCKER_REGISTRY}/f5ansible/py3.5.4-bare:devel
docker tag  ${DOCKER_REGISTRY}/f5ansible/py3.5.4-bare:devel f5ansible/py3.5.4-bare:devel
docker pull ${DOCKER_REGISTRY}/f5ansible/py3.6.2:devel
docker tag  ${DOCKER_REGISTRY}/f5ansible/py3.6.2:devel f5ansible/py3.6.2:devel
docker pull ${DOCKER_REGISTRY}/f5ansible/py3.6.2-bare:devel
docker tag  ${DOCKER_REGISTRY}/f5ansible/py3.6.2-bare:devel f5ansible/py3.6.2-bare:devel
