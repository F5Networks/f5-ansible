HA pair setup
=============

This playbook provides an example of how to use the F5 Modules for Ansible
in Ansible 2.5 to configure an HA pair.

To accomplish this, we use a series of modules and tasks. Some of them affect both
the primary and secondary devices. Others affect the primary device only. Where only
the primary device is affected, the pattern of pinning to a specific play host (via
the ``ansible_play_hosts`` Ansible variable) is used.

These playbooks make assumptions about self IP names and addresses, as well as other HA-related configurations. You will likely need to change them to suit your
environment. This can be done by modifying the files in the ``inventory/host_vars``
directory.

When using these playbooks, ensure that your hosts can actually communicate over the
self IPs that are configured. If not, then initial configuration sync (the last task)
will fail.

This example includes modules that are newly released and, therefore, may include bugs that the F5 development team is not yet aware of.

As always, if you encounter bugs, refer to the Issues page to report them.
