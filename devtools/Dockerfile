FROM python:2.7
MAINTAINER @caphrim007

RUN apt-get update && apt-get install -y \
    python-dev python-pip vim git-core wget curl \
    libffi-dev libssl-dev libxml2-dev libxslt1-dev \
    libjpeg62-turbo-dev zlib1g-dev
RUN rm -rf /var/lib/apt/lists/*

COPY . /opt/f5-ansible

WORKDIR /opt/f5-ansible
RUN pip install -r requirements.test.txt

CMD /bin/bash
