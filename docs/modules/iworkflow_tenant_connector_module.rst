.. _iworkflow_tenant_connector:


iworkflow_tenant_connector - Manage connectors associated with tenants in iWorkflow
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage connectors associated with tenants in iWorkflow.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 2.3.0
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
                <tr><td>connector<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Connector that you want to associate with the tenant</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Whether the managed device should exist, or not, in iWorkflow.</div>        </td></tr>
                <tr><td>tenant<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Tenant that you wish to modify.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Register connector to tenant
      iworkflow_tenant_connector:
          tenant: "tenant-foo"
          connector: "connector-foo"
          server: "iwf.mydomain.com"
          user: "admin"
          password: "secret"
          validate_certs: "no"
          state: "present"

    - name: Register multiple connectors to tenant
      iworkflow_tenant_connector:
          tenant: "tenant-foo"
          connector: "{{ item }}"
          server: "iwf.mydomain.com"
          user: "admin"
          password: "secret"
          validate_certs: "no"
          state: "present"
      with_items:
          - "connector-one"
          - "connector-two"

    - name: Unregister connector from tenant
      iworkflow_tenant_connector:
          tenant: "tenant-foo"
          connector: "connector-foo"
          server: "iwf.mydomain.com"
          user: "admin"
          password: "secret"
          validate_certs: "no"
          state: "absent"



Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - Tenants are not useful unless you associate them with a connector using the ``iworkflow_tenant_connector`` module.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.