Run your first BIG-IP playbook
==============================

Follow this tutorial to create a pool, add two nodes to that pool, and  assign a virtual server to serve requests to the nodes in the pool.

You can create your own yaml file to use as a playbook, or follow along with |site_yaml|.

Begin by placing the following in your ``playbook.yaml`` file:

.. code-block:: yaml

   ---

   - name: Create a VIP, pool, pool members, and nodes
     hosts: big-ip01.internal
     connection: local

Your BIG-IP is probably not called ``big-ip01.internal``. It might be a different hostname or even an IP address. Whichever it is, place it in the hosts line.

.. |site_yaml| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible/blob/devel/examples/0000-getting-started/playbook.yaml" target="_blank">this yaml file</a>

Add a pool
----------

A pool represents a collection of resources. These resource typically deliver a service that is identical. By assigning them to a pool, the BIG-IP is able to distribute requests among them.

Add the following to your ``playbook.yaml`` to create a pool called ``web``:

.. code-block:: yaml

    tasks:
       - name: Create a pool
         bigip_pool:
             lb_method: "ratio-member"
             name: "web"
             password: "admin"
             server: "big-ip01.internal"
             slow_ramp_time: "120"
             user: "admin"
             validate_certs: "no"
         delegate_to: localhost

Add two nodes
-------------

Now you want to create the nodes in your BIG-IP configuration. Nodes represent the actual devices on your network. They could be physical gear, VMs, or other devices.

To add the two nodes, put the following in your ``playbook.yaml`` file:

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

    The remaining tasks must align vertically with the ``Add a pool`` task above. If the spacing doesn't line up, Ansible will raise an error.

Add the nodes to the pool
-------------------------

With the pool created and your nodes in place, you now want to add those nodes to the pool. At this point, you can refer to the nodes as pool members.

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
--------------------

Now that you created your pool and the nodes are members of that pool, you want to create a virtual IP address so that external requests go to the pool members.

The following example uses ``172.16.10.108`` as the external address, so you likely need to change it for your own environment.

To create a virtual server, add the following to your ``playbook.yaml`` file:

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

Curious what else is possible with the current modules? Interested in test-driving the modules under development? Refer to the sidebar for links relevant to your interests.

Want to know the difference between `delegate_to` and `connection:local`? See :doc:`connection-local-or-delegate-to`.
