Run your first BIG-IP playbook
==============================

Follow this tutorial to create a pool, add two members to that pool, and assign a virtual
server to serve requests to the members in the pool.

You can create your own yaml file to use as a playbook, or follow along with |site_yaml|.

Creating necessary directories
------------------------------

Ansible expects a certain directory structure when it runs. We'll replicate below what that
structure is and that will set us up for the remainder of this tutorial.

.. code-block:: yaml

   $ mkdir -p ansible/inventory/

The above set of directories includes the top-level ``ansible`` directory. This top-level
directory can be named anything, so we chose to name it ``ansible``.

Under that directory is where we'll put our inventory file.

Creating an inventory file
--------------------------

All Ansible work starts with an inventory file.

For the purposes of this tutorial, it is not necessary to have anything special in the inventory
file because we will be specifying our BIG-IP connection information within the playbook itself.

If you want to see more complete examples of inventory in Ansible, we recommend you refer to
inventory documentation found on Ansible's website.

Let's put the following text in a new file located at ``ansible/inventory/hosts``.

.. code-block:: yaml

   localhost

Creating the playbook
---------------------

Begin by placing the following in your ``playbook.yaml`` file:

.. code-block:: yaml

   ---

   - name: Create a VIP, pool and pool members
     hosts: all
     connection: local

This playbook will iterate over ``all`` hosts defined in our inventory. We only specified a
single host (localhost) so that means that Ansible will connect to localhost to run the tasks.

Remember, for this simple example, we are not going to connect to the BIG-IP via our inventory
information. For simplicity, we will be defining all that in the playbook itself.

.. |site_yaml| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible/blob/devel/examples/0000-getting-started/playbook.yaml" target="_blank">this yaml file</a>

Set connection variables
------------------------

At the time of this writing, the F5 Ansible modules communicate almost exclusively over the
REST API of the F5 device. There is one exception to this rule in the ``bigip_command`` module,
but for now we'll not go into this.

To facilitate a connection to the remote device, we need to specify these connection parameters.

The pattern we use for this is called a **provider**. You will typically see us define this
with an Ansible fact called ``provider``. Let's see this below.

.. code-block:: yaml

   vars:
     provider:
       password: admin
       server: 1.1.1.1
       user: admin
       validate_certs: no
       server_port: 443

The above defines a new fact called ``provider``. That fact is known as a dictionary and it
itself includes some sub-keys; ``password``, ``server``, etc.

The values of those sub-keys are variables (identifiable by their use of ``{{`` and ``}}``).

Those variables are the same variable names that we defined earlier in our inventory file. This
is how Ansible makes use of them in our playbooks.

In the remaining tasks, you will see how the ``provider`` itself is passed to the task so that
it can connect to the BIG-IP.

Add a pool
----------

A pool represents a collection of resources. These resource typically deliver a service that
is identical. By assigning them to a pool, the BIG-IP is able to distribute requests among them.

Add the following to your ``playbook.yaml`` to create a pool called ``web``:

.. code-block:: yaml

   tasks:
     - name: Create a pool
       bigip_pool:
         provider: "{{ provider }}"
         lb_method: ratio-member
         name: web
         slow_ramp_time: 120
       delegate_to: localhost

Add two pool members
--------------------

Now you want to create the pool members in your BIG-IP configuration. Members represent
where the traffic coming through a virtual server will eventually land. They could be physical
gear, VMs, or other devices.

To add the two members, put the following in your ``playbook.yaml`` file:

.. code-block:: yaml

   - name: Add members to pool
     bigip_pool_member:
       provider: "{{ provider }}"
       description: "webserver {{ item.name }}"
       host: "{{ item.host }}"
       name: "{{ item.name }}"
       pool: web
       port: 80
     with_items:
       - host: 10.10.10.10
         name: web01
       - host: 10.10.10.20
         name: web02
     delegate_to: localhost

.. note::

    The remaining tasks must align vertically with the ``Add a pool`` task above. If the
    spacing doesn't line up, Ansible will raise an error.


Add a virtual server
--------------------

Now that you created your pool and the nodes are members of that pool, you want to create
a virtual IP address so that external requests go to the pool members.

The following example uses ``172.16.10.108`` as the external address, so you likely need to
change it for your own environment.

To create a virtual server, add the following to your ``playbook.yaml`` file:

.. code-block:: yaml

   - name: Create a VIP
     bigip_virtual_server:
       provider: "{{ provider }}"
       description: foo-vip
       destination: 172.16.10.108
       name: vip-1
       pool: web
       port: 80
       snat: Automap
       profiles:
         - http
         - clientssl
     delegate_to: localhost

Run the playbook
----------------

We can now run our playbook. We will run this from the top-level ``ansible`` directory.
Refer to the command below.

.. code-block:: bash

   ansible-playbook -i inventory/hosts playbook.yaml

If you followed the above steps correctly, you should see output similar to what is shown below.

.. code-block:: yaml

   PLAY [Create a VIP, pool and pool members] ***********************************************

   TASK [Gathering Facts] *******************************************************************
   ok: [localhost]

   TASK [Create a pool] *********************************************************************
   changed: [localhost -> localhost]

   TASK [Add members to pool] ***************************************************************
   changed: [localhost -> localhost] => (item={u'host': u'10.10.10.10', u'name': u'web01'})
   changed: [localhost -> localhost] => (item={u'host': u'10.10.10.20', u'name': u'web02'})

   TASK [Create a VIP] **********************************************************************
   changed: [localhost -> localhost]

   PLAY RECAP *******************************************************************************
   localhost                  : ok=4    changed=3    unreachable=0    failed=0    skipped=0


Congrats if you've gotten this far!

More info
---------

Curious what else is possible with the current modules? Interested in test-driving the modules
under development? Refer to the sidebar for links relevant to your interests.

Want to know the difference between `delegate_to` and `connection:local`? See
:doc:`connection-local-or-delegate-to`.

Want to know more about Ansible and how you can expand from here? Refer to the Ansible
documentation at https://docs.ansible.com
