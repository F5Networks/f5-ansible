FROM ubuntu:latest
MAINTAINER @caphrim007

RUN apt-get update && apt-get install -y \
    python-dev vim git-core wget curl
RUN rm -rf /var/lib/apt/lists/*

COPY . /opt/f5ansible

WORKDIR /opt/f5ansible
RUN pip install -r dev-requirements.txt

CMD /bin/bash
