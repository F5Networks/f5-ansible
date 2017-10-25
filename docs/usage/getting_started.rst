Getting Started
===============

This document explains how to begin using the F5 Ansible modules.

You will create a pool, add two nodes to that pool, and finally assign a
virtual server to serve requests to the nodes in the pool.

**Note:** F5 Ansible modules are not supported by F5.

First, obtain `Python 2.7`_ and `Ansible`_ if you do not already have them.

Ansible 2.2.0 is the minimum required version.

Installing Ansible
------------------

Please see the Ansible documentation for how to install Ansible:

* http://docs.ansible.com/ansible/latest/intro_installation.html
  
Installing via virtualenv/pip is encouraged if you are testing out f5-ansible in your development and/or personal device.  For an example please see :doc:`virtualenv`.

*  http://docs.ansible.com/ansible/latest/intro_installation.html#latest-releases-via-pip
 
.. note:: You are strongly encouraged to install Ansible from `pip` to ensure that you are using a version of Ansible that we can assist you with.

Installing Dependencies
------------------------

In addition to Ansible a few additional Python modules are required.  At minimum you should add the `f5-sdk`.  A common set of modules to start with would be.

* f5-sdk
* bigsuds
* netaddr
* deepdiff

You can install these via pip (either globally or within a virtual environment).

.. code-block:: terminal
  
  (myansible) $ pip install f5-sdk bigsuds netaddr deepdiff

Playbook
--------

The remainder of this tutorial will walk you through the various steps of
adding tasks to your playbook.

.. note:: I've broken each task into its own section
          to better explain it. This might lead to confusion though, so if you
          just want to get the whole file and then follow along, you can
          `download it here`_.

Let's begin by placing the following in your ``site.yaml``:

.. code-block:: yaml

    ---

    - name: Create a VIP, pool, pool members and nodes
      hosts: big-ip01.internal
      connection: local

Your BIG-IP is probably not called ``big-ip01.internal``. It might be a
different hostname or even IP address. Whichever it is, place it in the hosts
line.

.. _download it here: https://github.com/F5Networks/f5-ansible/blob/master/examples/getting-started.yaml

Add a pool
~~~~~~~~~~

A pool represents a collection of resources. These resource typically deliver
a service that is identical. By assigning them to a pool, the BIG-IP is able
to distribute requests amongst all of them.

Add the following to your ``site.yaml`` to create a pool called ``web``:

.. code-block:: yaml

    tasks:
       - name: Create a pool
         bigip_pool:
             lb_method: "ratio_member"
             name: "web"
             password: "admin"
             server: "big-ip01.internal"
             slow_ramp_time: "120"
             user: "admin"
             validate_certs: "no"
         delegate_to: localhost

Add two nodes
~~~~~~~~~~~~~

Now we want to create the nodes in our BIG-IP configuration. These represent
the actual devices on your network. They could be physical gear, VMs, or
other devices.

To add the two nodes, we'll put the following in our ``site.yaml``

.. code-block:: yaml

       - name: Create node1
         bigip_node:
             host: "10.10.10.10"
             name: "node-1"
             password: "admin"
             server: "big-ip01.internal"
             user: "admin"
             validate_certs: "no"
         delegate_to: localhost

       - name: Create node2
         bigip_node:
             host: "10.10.10.20"
             name: "node-2"
             password: "admin"
             server: "big-ip01.internal"
             user: "admin"
             validate_certs: "no"
         delegate_to: localhost

.. note::

    It is important that you correctly space over this and the remaining
    tasks so that they align vertically with the ``Create a pool`` task
    above. If you do not do this, Ansible will raise an error.

Add the nodes to the pool
~~~~~~~~~~~~~~~~~~~~~~~~~

With the pool created and your nodes in place, you not want to add those
nodes to the pool. At this point we would refer to those nodes as pool
members.

.. code-block:: yaml

       - name: Add nodes to pool
         bigip_pool_member:
             description: "webserver-1"
             host: "{{ item.host }}"
             name: "{{ item.name }}"
             password: "admin"
             pool: "web"
             port: "80"
             server: "big-ip01.internal"
             user: "admin"
             validate_certs: "no"
         delegate_to: localhost
         with_items:
             - host: "10.10.10.10"
               name: "node-1"
             - host: "10.10.10.20"
               name: "node-2"

Add a virtual server
~~~~~~~~~~~~~~~~~~~~

Now that our pool is set up and the nodes are members of that pool, we next
want to create a VIP so that external requests can be delivered to the pool
members.

The below example uses ``172.16.10.108`` as the external address, so you may
need to change it for your own environment

To create a virtual server, add the following to you ``site.yaml``:

.. code-block:: yaml

       - name: Create a VIP
         bigip_virtual_server:
             description: "foo-vip"
             destination: "172.16.10.108"
             password: "admin"
             name: "vip-1"
             pool: "web"
             port: "80"
             server: "big-ip01.internal"
             snat: "Automap"
             user: "admin"
             all_profiles:
                  - "http"
                  - "clientssl"
             validate_certs: "no"
         delegate_to: localhost

More info
---------

Curious what else is possible with the current modules? Interested in
test-driving the modules under development? Refer to the sidebar for
links relevant to your interests.

.. _Ansible: http://docs.ansible.com/ansible/intro_installation.html
.. _Python 2.7: http://www.python.org/

