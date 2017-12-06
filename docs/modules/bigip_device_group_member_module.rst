.. _bigip_device_group_member:


bigip_device_group_member - Manages members in a device group
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages members in a device group. Members in a device group can only be added or removed, never updated. This is because the members are identified by unique name values and changing that name would invalidate the uniqueness.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 2.2.3


Options
-------

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                <tr><td>device_group<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The device group that you want to add the member to.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Specifies the name of the device that you want to add to the device group. Often this will be the hostname of the device. This member must be trusted by the device already. Trusting can be done with the <code>bigip_device_group</code> module and the <code>peer_hostname</code> option to that module.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Add the current device to the "device_trust_group" device group
      bigip_device_group_member:
        name: "{{ inventory_hostname }}"
        device_group: device_trust_group
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
      delegate_to: localhost

    - name: Add the hosts in the current scope to "device_trust_group"
      bigip_device_group_member:
        name: "{{ item }}"
        device_group: device_trust_group
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
      with_items: "{{ hostvars.keys() }}"
      run_once: true
      delegate_to: localhost



Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.