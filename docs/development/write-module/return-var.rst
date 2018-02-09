RETURN variable
===============

When a module finishes running, F5 always uses the module's parameters to return the changes.

Some exceptions to this rule apply. For example, where the ``state`` variable contains more
states than just ``absent`` and ``present``, such as in the ``bigip_virtual_server`` module.

For the sample module, these values include:

- ``banner``
- ``banner_text``
- ``inactivity_timeout``
- ``log_level``
- ``login``

The ``RETURN`` variable describes these values, specifies when they're returned, and
provides examples of what the values returned might look like.

When the Ansible module documentation generates, these values are output in a table.
