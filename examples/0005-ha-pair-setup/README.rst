HA pair setup
=============

This Playbook provides an example of how one can use the modules in Ansible
2.5 to configure an HA pair.

To accomplish this, we use a series of modules and tasks. Some of them affect both
the primary and secondary devices. Others only affect the primary device. Where only
the primary device is affected, the pattern of pinning to a specific play host (via
the ``ansible_play_hosts`` Ansible variable is used.

These playbooks make several assumptions of Self IP names and addresses as well as
other HA related configurations. You will likely need to change them to suite your
environment. This can be done by modifying the files in the ``inventory/host_vars``
directory.

When using these playbooks, ensure that your hosts can actually communicate over the
Self IPs that are configured. If not, then initial configuration sync (the last task)
will fail.

The example here includes modules that are newly released and, therefore, there may
be bugs in them which the F5 development team is not yet aware of.

As always, if you encounter bugs, refer yourself to the Issues page here to report
them.
