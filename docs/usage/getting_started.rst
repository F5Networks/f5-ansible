Getting Started
===============

This document will show you how to begin using the F5 Ansible modules.
You will create a pool, add two nodes to that pool, and finally assign a
virtual server to serve requests to the nodes in the pool.

First, obtain `Python 2.7`_ and `Ansible`_ if you do not already have them.

The version of Ansible that is required is at least 2.2.0. At the time of
this writing, that version is still in development. Below, I've included
steps to install Ansible in a virtualenv for you to use until such time
as Ansible 2.2.0 is released

Installing Ansible
------------------

At this time, an unreleased version of Ansible is required to make full
use of these modules; 2.2.0.

Let's install Ansible in a virtualenv to make it possible to use the
modules.

First, make sure `virtualenv` is installed.

    pip install virtualenv

This will make available to you a `virtualenv` command. You can use that
it make a virtual environment for your Ansible installation.

    virtualenv ansible2

In your current working directory, you will find a new directory called
`ansible2`. In this directory resides a copy of Python that is configured
to install any modules inside of that local directory. Via this method,
we can install Python modules without stomping on the system wide ones.

To use this new location, you must `activate` it.

    . ansible2/bin/activate

You should see your prompt change so that the name of the virtualenv is
prefixing the normal prompt. For example.

    (ansible2)SEA-ML-RUPP1:f5 trupp$

Now that our `virtualenv` is active, all future Python commands (such as
`pip`) will install modules into the virtualenv. So let's install the
development copy of ansible.

    pip install git+git://github.com/ansible/ansible.git@devel

You should be able to verify that you are running the new version of
Ansible by using the `--version` argument to the `ansible` command, like
so.

    ansible --version

You should be presented with output that resembles the following

    (test1)SEA-ML-RUPP1:virtualenv trupp$ ansible --version
    ansible 2.2.0
      config file =
      configured module search path = Default w/o overrides

With this ready, you can create your first playbook. We'll write the remainder
of our Ansible playbooks in a file called ``site.yaml``

Playbook
--------

Let's begin by placing the following in your ``site.yaml``:

.. code-block:: yaml

    ---

    - name: Create a VIP, pool, pool members and nodes
      hosts: big-ip01.internal
      connection: local

Your BIG-IP is probably not called ``big-ip01.internal``. It might be a
different hostname or even IP address. Whichever it is, place it in the hosts
line.

Add a pool
~~~~~~~~~~

A pool represents a collection of resources. These resource typically deliver
a service that is identical. By assigning them to a pool, the BIG-IP is able
to distribute requests amongst all of them.

Add the following to your ``site.yaml`` to create a pool called ``web``:

.. code-block:: yaml

    - tasks:
       - name: Create a pool
         bigip_pool:
             lb_method: "ratio_member"
             name: "web"
             password: "admin"
             server: "big-ip01.internal"
             slow_ramp_time: "120"
             user: "admin"
             validate_certs: "no"

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

       - name: Create node2
         bigip_node:
             host: "10.10.10.20"
             name: "node-2"
             password: "admin"
             server: "big-ip01.internal"
             user: "admin"
             validate_certs: "no"

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
             destination: "172.16.10.108:80"
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

More info
---------

Curious what else is possible with the current modules? Interested in
test-driving the modules under development? Refer to the sidebar for
links relevant to your interests.

.. _Ansible: http://docs.ansible.com/ansible/intro_installation.html
.. _Python 2.7: http://www.python.org/