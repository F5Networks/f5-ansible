:source: iworkflow_service.py

:orphan:

.. _iworkflow_service_module:


iworkflow_service - Manages L4/L7 Services on iWorkflow
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manages L4/L7 Service on iWorkflow. Services can only be created and otherwise managed by tenants on iWorkflow. Since all of the F5 modules assume the use of the administrator account, the user of this module will need to include the ``tenant`` option if they want to use this module with the admin account.



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- iWorkflow >= 2.1.0


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
                                                                                                                                                                                                        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="1">
                    <b>connector</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The cloud connector associated with this L4/L7 service. This option is required when <code>state</code> is <code>present</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Name of the L4/L7 service.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>parameters</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>A dictionary containing the values of input parameters that the service administrator has made available for tenant editing.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>service_template</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The Service Template that you want to base this L4/L7 Service off of. This option is required when <code>state</code> is <code>present</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>tenant</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>The tenant whose service is going to be managed. This is a required option when using the system&#x27;s <code>admin</code> account as the admin is not a tenant, and therefore cannot manipulate any of the L4/L7 services that exist. If the <code>user</code> option is not the <code>admin</code> account, then this tenant option is assumed to be the user who is connecting to the BIG-IP. This assumption can always be changed by setting this option to whatever tenant you wish.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - L4/L7 Services cannot be updated once they have been created. Instead, you must first delete the service and then re-create it.


Examples
--------

.. code-block:: yaml

    
    - name: Create a ...
      iworkflow_service:
        name: foo
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
      delegate_to: localhost





Status
------



This module is **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Tim Rupp (@caphrim007)

