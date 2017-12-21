Connection or delegation
========================

Sometimes you might see examples of F5 Ansible playbooks that use ``connection: local``:

.. code-block:: yaml

   - name: This is my play
     hosts: some-host
     connection: local

     tasks:
         ...

But other times, you will see ``delegate_to`` used. For example:

.. code-block:: yaml

   - name: This is my play
     hosts: some-host

     tasks:
         - name: This is a task
           bigip_command:
             commands:
               - tmsh list ltm virtual
           delegate_to: localhost

See the usage of ``delegate_to: localhost`` at the bottom?

What's the difference?
----------------------

There are three major differences between ``connection: local`` and ``delegate_to: localhost``:

* ``connection: local`` applies to all hosts
* ``delegate_to`` applies to specific hosts
* ``delegate_to`` runs your task on *one* host, in the context of *another* host

Connection: local
-----------------

First, ``connection: local`` applies to **all** hosts in the playbook. If you find yourself mixing and matching BIG-IP
hosts with things like web servers, it would cause your legitimate ssh connections to fail.

This is because when you specify ``connection: local``, every host is now considered to have 127.0.0.1 as their IP address.

This is likely not what you want.

For example, the following playbook is **not what you want**.
*(Common login variables omitted)*

.. code-block:: yaml

   - name: This is my play
     hosts: my-web-server
     connection: local

     tasks:
         - name: Disable pool member for upgrading
           bigip_pool_member:
             pool: foo
             name: "{{ inventory_hostname }}"
             state: disabled

         - name: Upgrade the webserver
           apt:
             name: apache2
             state: latest

         - name: Re-enable pool member after upgrading
           bigip_pool_member:
             pool: foo
             name: "{{ inventory_hostname }}"
             state: enabled

The second task is **not what you want** because it attempts to run the ``apt`` module on your local machine. Your playbook,
however, specifically states that it wants to upgrade the **remote** webserver.

Delegation
----------

You can remedy this situation with ``delegate_to``. For the most part, you will use this feature when the ``connection`` line
is ``ssh`` (the default).

Delegation allows you to mix and match remote hosts. You continue to use an SSH connection for legitimate purposes, such
as connecting to remove servers, but for the devices that don't support this option, you delegate their tasks.

For example, this playbook will correct your problem:

.. code-block:: yaml

   - name: This is my play
     hosts: my-web-server

     tasks:
         - name: Disable pool member for upgrading
           bigip_pool_member:
             pool: foo
             name: "{{ inventory_hostname }}"
             state: disabled
           delegate_to: localhost

         - name: Upgrade the webserver
           apt:
             name: apache2
             state: latest

         - name: Re-enable pool member after upgrading
           bigip_pool_member:
             pool: foo
             name: "{{ inventory_hostname }}"
             state: enabled
           delegate_to: localhost

The ``delegate_to`` parameter delegates the running of the task to some completely different machine.

However, instead of the module having access to that totally different machine's ``facts``, it instead has the ``facts``
of the inventory item where the delegation happened. This is *using the context of the host*.

Summary
-------

Quiz time.

In the above example, *even though* the first and third tasks are running on the Ansible controller (instead of the
remote webserver), what is the value of the ``{{ inventory_hostname }}`` variable?

1. localhost
2. my-web-server
3. something else

If you answered ``my-web-server`` then you are correct.

This is **context**. The task executes on ``localhost`` using ``my-web-server``'s context, and therefore, its ``facts``.
