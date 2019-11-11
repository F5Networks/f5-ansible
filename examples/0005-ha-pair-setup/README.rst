HA pair setup
=============

This playbook provides an example of how to use the F5 Modules for Ansible
in Ansible 2.5 to configure an HA pair.

To accomplish this, we use a series of modules and tasks. Some of them affect both
the primary and secondary devices. Others affect the primary device only. Where only
the primary device is affected, the pattern of pinning to a specific play host (via
the ``ansible_play_hosts`` Ansible variable) is used.

These playbooks make assumptions about self IP names and addresses, as well as other
HA-related configurations. You will likely need to change them to suit your
environment. This can be done by modifying the files in the ``inventory/host_vars``
directory.

When using these playbooks, ensure that your hosts can actually communicate over the
self IPs that are configured. If not, then initial configuration sync (the last task)
will fail.

This example includes modules that are newly released and, therefore, may include bugs
that the F5 development team is not yet aware of.

As always, if you encounter bugs, refer to the Issues page to report them.

Usage
=====

Begin by opening the ``group_vars/f5-test.yaml`` file. Inside this file, you will
find and change (as needed) the following variables.

* ``bigip_username``
* ``bigip_password``
* ``bigip_port``
* ``validate_certs``
* ``ansible_python_interpreter``

Observe the documentation in each file to determine what needs to be changed

Next, open the ``host_vars/bigip01.internal.yaml`` file. Inside this file, you will
find and change the following variables.

* ``ansible_host``
* ``nets``
* ``config_sync_ip``
* ``mirror_primary_address``
* ``unicast_failover``

The Self IPs in this file are organized in the following way

* IP_A1 - This is the IP address that you want to assign (or have already assigned) to
  the first interface on your device. ie, Interface 1.1. The VLAN argument should match
  the name of the VLAN named in the ``vlans`` parameter of ``group_vars/f5-test.yaml``.
* IP_A2 - This is the IP address that you want to assign (or have already assigned) to
  the first interface on your device. ie, Interface 1.2. The VLAN argument should match
  the name of the VLAN named in the ``vlans`` parameter of ``group_vars/f5-test.yaml``.
* IP_A3 - This is the IP address that you want to assign (or have already assigned) to
  the first interface on your device. ie, Interface 1.3. The VLAN argument should match
  the name of the VLAN named in the ``vlans`` parameter of ``group_vars/f5-test.yaml``.
  This address will also be the address used for HA communication.
