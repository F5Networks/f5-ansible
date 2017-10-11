Connection or Delegation
========================

This question comes up so frequently that I've made a documentation page specifically
for it.

Sometimes people see examples of F5 Ansible playbooks that use the following

.. code-block:: yaml

   - name: This is my play
     hosts: some-host
     connection: local

     tasks:
         ...

Alright, but sometimes instead of that, you will see delegation used. such as the
following,

.. code-block:: yaml

   - name: This is my play
     hosts: some-host

     tasks:
         - name: This is a task
           bigip_command:
             commands:
               - tmsh list ltm virtual
           delegate_to: localhost

See that usage of `delegate_to: localhost` at the bottom there?

What's the difference?
----------------------

There are three major differences between the two,

* `connection: local` applies to all hosts
* `delegate_to` applies to specific hosts
* `delegate_to` runs your task on *one* host in the context of *another* host

Connection local
~~~~~~~~~~~~~~~~

First, `connection: local` applies to **all** hosts in the playbook. Therefore, if you
find yourself mixing and matching BIGIP with things like web servers, it would cause
your legitimate ssh connections to fail. This is because when specifying
`connection: local`, every host is now considered to have 12.0.0.1 as their IP address.
This is likely not what you want.

For example, the playbook below is **not what you want**.

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

The second task is **not what you want** because it will attempt to run the `apt` module
on your local machine. Your playbook, however, is specifically stating that it wants
to upgrade the remote webserver.

Delegation
~~~~~~~~~~

The above is remedied with `delegate_to`. This feature is used primarily when the
`connection` line is set to `ssh` (the default).

Delegation allows you to mix and match remote hosts. You continue to use an SSH
connection for legitimate purposes, such as connecting to remove servers, but for the
devices that support no such option, you delegate for their tasks.

For example, the playbook below will correct your problem above.

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

The `delegate_to` parameter delegates the running of the task to some completely
different machine.

However, instead of the module having access to that totally different machine's
`facts`, it instead has the `facts` of the inventory item where the delegation
happen. We refer to this as *using the context of the host*

Delegation context
~~~~~~~~~~~~~~~~~~

Quiz time.

In the above example, *even though* the 1st and 3rd tasks are running on the Ansible
controller (instead of the remote webserver), what will the value of the
`{{ inventory_hostname }}` variable be?

1. localhost
2. my-web-server
3. something else

If you answered `my-web-server` then DING! DING! DING! WE HAVE A WINNER!

This is *context* the task executed on `localhost` using `my-web-server`'s context,
and therefore, its `facts`.
