FROM ubuntu:latest
MAINTAINER @caphrim007

RUN apt-get update && apt-get install -y \
    python-dev python-pip vim git-core wget curl \
    libffi-dev libssl-dev libxml2-dev libxslt1-dev \
    libjpeg8-dev zlib1g-dev
RUN rm -rf /var/lib/apt/lists/*

COPY . /opt/f5ansible

WORKDIR /opt/f5ansible
RUN pip install -r dev-requirements.txt

CMD /bin/bash
