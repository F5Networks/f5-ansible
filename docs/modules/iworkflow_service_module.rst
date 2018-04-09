:source: modules/iworkflow_service.py

.. _iworkflow_service:


iworkflow_service - Manages L4/L7 Services on iWorkflow
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manages L4/L7 Service on iWorkflow. Services can only be created and otherwise managed by tenants on iWorkflow. Since all of the F5 modules assume the use of the administrator account, the user of this module will need to include the `tenant` option if they want to use this module with the admin account.



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- iWorkflow >= 2.1.0


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
                <tr>
            <th class="head"><div class="cell-border">Parameter</div></th>
            <th class="head"><div class="cell-border">Choices/<font color="blue">Defaults</font></div></th>
                        <th class="head" width="100%"><div class="cell-border">Comments</div></th>
        </tr>
                    <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>connector</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The cloud connector associated with this L4/L7 service. This option is required when <code>state</code> is <code>present</code>.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>name</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Name of the L4/L7 service.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>parameters</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>A dictionary containing the values of input parameters that the service administrator has made available for tenant editing.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>service_template</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The Service Template that you want to base this L4/L7 Service off of. This option is required when <code>state</code> is <code>present</code>.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>tenant</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                        <b>Default:</b><br/><div style="color: blue">None</div>
                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>The tenant whose service is going to be managed. This is a required option when using the system&#x27;s <code>admin</code> account as the admin is not a tenant, and therefore cannot manipulate any of the L4/L7 services that exist. If the <code>user</code> option is not the <code>admin</code> account, then this tenant option is assumed to be the user who is connecting to the BIG-IP. This assumption can always be changed by setting this option to whatever tenant you wish.</div>
                                                                                                </div>
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



This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Tim Rupp (@caphrim007)

