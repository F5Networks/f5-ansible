FROM ubuntu

WORKDIR /root

RUN apt-get update && apt-get install -y python-pip
RUN pip install ansible
RUN mkdir f5-ansible

COPY . f5-ansible/

WORKDIR /root/fs-ansible