F5 Ansible Documentation
========================
|Build Status| |Docs Build Status|

Introduction
------------
This project implements a set of Ansible modules for the F5 Networks® BIG-IP®
Users of these modules can create, edit, update, and delete configuration
objects on a BIG-IP®. For more information on the basic principals that the
modules use, see the :doc:`userguide/index`.

Quick Start
-----------
Installation
~~~~~~~~~~~~
.. code:: shell

    $> git clone https://github.com/F5Networks/f5-ansible.git

Basic Example
~~~~~~~~~~~~~
.. code:: yaml

    ---

    - name: Create a VIP, pool, pool members and nodes
      hosts: localhost
      connection: local

      tasks:

       - name: Create node1
         bigip_node:
             host: "10.10.10.10"
             name: "node-1"
             password: "foo"
             server: "big-ip01.internal"
             user: "admin"
             validate_certs: "no"

       - name: Create node2
         bigip_node:
             host: "10.10.10.20"
             name: "node-2"
             password: "foo"
             server: "big-ip01.internal"
             user: "admin"
             validate_certs: "no"

       - name: Create a pool
         bigip_pool:
             lb_method: "ratio_member"
             name: "pool-1"
             password: "foo"
             server: "big-ip01.internal"
             slow_ramp_time: "120"
             user: "admin"
             validate_certs: "no"

       - name: Add nodes to pool
         bigip_pool_member:
             description: "webserver-1"
             host: "{{ item.host }}"
             name: "{{ item.name }}"
             password: "foo"
             pool: "pool-1"
             port: "80"
             server: "big-ip01.internal"
             user: "admin"
             validate_certs: "no"
         with_items:
             - host: "10.10.10.10"
               name: "node-1"
             - host: "10.10.10.20"
               name: "node-2"

       - name: Create a VIP
         bigip_virtual_server:
             description: "foo-vip"
             destination: "172.16.10.108:80"
             password: "foo"
             name: "vip-1"
             pool: "pool-1"
             port: "80"
             server: "big-ip01.internal"
             snat: "Automap"
             user: "admin"
             all_profiles:
                  - "http"
                  - "clientssl"
             validate_certs: "no"

Detailed Documentation
----------------------

.. toctree::
   :maxdepth: 4

   userguide/index
   devguide/index
   F5 Ansible Docs <apidoc/modules>

Copyright
---------
Copyright 2014-2016 F5 Networks Inc.

License
-------
Apache V2.0
~~~~~~~~~~~
Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations
under the License.

.. |Build Status| image:: https://travis-ci.org/F5Networks/f5-ansible.svg?branch=master
    :target: https://travis-ci.org/F5Networks/f5-ansible
    :alt: Build Status

.. |Docs Build Status| image:: http://readthedocs.org/projects/f5-ansible/badge/?version=latest
    :target: http://f5-ansible.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status