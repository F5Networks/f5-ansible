Multi-config example
====================

This playbook shows how to use native Ansible modules to configure a number of common BIG-IP items.

The playbook does the following:

* Provisions ASM
* Creates a data group
* Creates an iRule for the data group to use
* Creates an LTM policy
* Creates an ASM policy
* Creates a rule for the LTM policy that uses the ASM policy
* Creates a pool
* Creates pool members
* Creates a virtual server
* Assigns the pool to the virtual
* Assigns the LTM policy to the virtual
* Assigns the iRule to the virtual

Note: The data sources in the example are fictitious.
