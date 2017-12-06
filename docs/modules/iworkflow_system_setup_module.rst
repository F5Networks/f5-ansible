.. _iworkflow_system_setup:


iworkflow_system_setup - Manage system setup related configuration on iWorkflow
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage system setup related configuration on iWorkflow.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 2.2.2
  * iWorkflow >= 2.1.0


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
                <tr><td>dns_search_domains<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Default search domain that should be used for DNS queries</div>        </td></tr>
                <tr><td>dns_servers<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>List of DNS servers to set on the iWorkflow device for name resolution.</div>        </td></tr>
                <tr><td>hostname<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Sets the hostname of the iWorkflow device</div>        </td></tr>
                <tr><td>management_address<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Management address of the iWorkflow instance.</div>        </td></tr>
                <tr><td>ntp_servers<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>[u'pool.ntp.org']</td>
        <td></td>
        <td><div>List of NTP servers to set on the iWorkflow device for time synchronization.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Disable iWorkflow setup screen and set accounts as unchanged
      iworkflow_system_setup:
          is_admin_password_changed: "no"
          is_root_password_changed: "no"
          is_system_setup: "yes"
          password: "secret"
          server: "iwf.mydomain.com"
          user: "admin"
      delegate_to: localhost



Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - Required the netaddr Python package on the host. This is as easy as pip install netaddr.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.