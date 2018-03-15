Multi-config example
====================

This playbook provides an example of how to use native Ansible modules to configure a number of common items.

The following use cases are configured

* Provision ASM
* Create a data group
* Create an iRule for the data group to use
* Create an LTM policy
* Create an ASM policy
* Create a rule for the LTM policy which uses the ASM policy
* Create a pool
* Create pool members
* Create a virtual server
* Assign the pool to the virtual
* Assign the LTM policy to the virtual
* Assign the iRule to the virtual

Note: Data sources are contrived to protect the innocent.
