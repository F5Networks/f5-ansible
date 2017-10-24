.. _iworkflow_tenant:


iworkflow_tenant - Manage tenants in iWorkflow
++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage tenants in iWorkflow.


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
                <tr><td>contact_address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>An optional contact address associated with the tenant.</div>        </td></tr>
                <tr><td>contact_email<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>An optional contact email address associated with the tenant.</div>        </td></tr>
                <tr><td>contact_phone<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>An optional contact phone number associated with the tenant.</div>        </td></tr>
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>An optional description for the tenant.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Name of the tenant that you want to manage.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The BIG-IP host. This option can be omitted if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                <tr><td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>The BIG-IP server port. This option can be omitted if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>When <code>state</code> is <code>present</code>, ensures that the tenant exists. When <code>state</code> is <code>absent</code>, ensures that the tenant is removed.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. This option can be omitted if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. This option can be omitted if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    


Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - Tenants are not useful unless you associate them with a connector using the ``iworkflow_tenant_connector`` module.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.