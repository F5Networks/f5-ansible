Dealing with "replace all"
==========================

You may want to use Ansible modules to mimic the behavior of the "replace-all-with" `tmsh` functionality.

Challenges
----------

By its nature, Ansible is not designed to support something like `replace-all-with`.

Ansible modules are normally designed to run per-device and therefore should, in most cases, accept a single item of configuration and apply it on that device.

For example:

.. code-block:: yaml

   tasks:
       - name: Create SNAT pools
         bigip_snat_pool:
             name: "{{ ansible_host }}"
             members:
                 - 11.11.11.11
                 - 22.22.22.22

This task, iterated per host, creates a number of SNAT pools. However, you may want to remove all of the existing pools and replace them with a new list.

If you did not know what the existing SNAT pools were, how would you remove the existing pools to add new ones?

This pattern of "unit of work per host" becomes an anti-pattern when applied to `replace-all-with`. This is because there is no way to reliably tell the module to:

- Delete all the existing
- Add what I give you

Because the module only knows about what it receives at time of execution and not about what the play is doing as a whole (or even that it's in a loop) you cannot specify, for example a `replace_all_with` parameter.

It's also unacceptable to have something like an `append` parameter because, again, the module is not aware that it is in a loop or what the greater play is doing.

There may be some ability to make the module aware by specifying these list squashing modules in Ansible's default `squash_actions` configuration variable, but this is an untenable solution because we would be either:

- Changing core code
- Asking users to create custom `ansible.cfg` files every time they use BIG-IPs

Proposals
---------

What I propose is to provide the user with the ability to know what exists so that they can use the `absent` state of a module to remove all existing instances. You would do this by using a `*_facts` module for the manipulation module in question.

Using the above example of `bigip_snat_pool`, the facts module would be `bigip_snat_pool_facts`. The user could provide filtering params such as those they can supply to the `bigip_snat_pool` module to return only values that meet those criteria.

The user can then store those returned values using a `register` variable and then loop over the values to delete them all before adding new ones.

For example:

.. code-block:: yaml

   tasks:
       - name: Get SNAT pool facts
         bigip_snat_pool_facts:
         register: result

       - name: Remove all SNAT pools
         bigip_snat_pool:
             name: "{{ item.name }}"
             state: "absent"
         with_items: result

Future additions
----------------

Additionally, I would like to pursue the development of modules to support transactions, such as:

- bigip_transaction

You could use this to ensure that the above example would tolerate a failure between deleting and re-creating SNAT pools. Thus, the `replace-all-with` functionality would essentially be retained.

For example:

.. code-block:: yaml

   tasks:
       - block:
             - name: Start transaction
               bigip_transaction:
                   state: "open"
               register: tx

             - name: Get SNAT pool facts
               bigip_snat_pool_facts:
                   transaction: "{{ tx.id }}"
               register: result

             - name: Remove all SNAT pools
               bigip_snat_pool:
                   name: "{{ item.name }}"
                   state: "absent"
                   transaction: "{{ tx.id }}"
               with_items: result

             - name: Commit transaction
               bigip_transaction:
                   state: "commit"
                   transaction: "{{ tx.id }}"
         rescue:
             - name: Rollback transaction
               bigip_transaction:
                   state: rollback
                   transaction: "{{ tx.id }}"
         environment:
             F5_SERVER: "{{ ansible_host }}"
             F5_USER: "{{ bigip_username }}"
             F5_PASSWORD: "{{ bigip_password }}"
             F5_SERVER_PORT: "{{ bigip_port }}"
             F5_VALIDATE_CERTS: "{{ validate_certs }}"

Note the addition of Transactions above. This new functionality would go in the `f5_utils` module_utils code inside of Ansible, so it would be supported across all modules.

For modules that do not support it, you would define a `@property` to return only `None`.

For example:

.. code-block:: python

   class Parameters(AnsibleF5Parameters):
       ...

       @property
       def transaction(self):
           return None

This is similar in how the `bigip_partition` module always returns `None` for the `partition` parameter because you cannot create partitions inside of partitions.
