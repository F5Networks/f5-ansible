.. _iworkflow_service:


iworkflow_service - Manages L4/L7 Services on iWorkflow.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages L4/L7 Service on iWorkflow. Services can only be created and otherwise managed by tenants on iWorkflow. Since all of the F5 modules assume the use of the administrator account, the user of this module will need to include the ``tenant`` option if they want to use this module with the admin account.


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
            <tr>
    <td>connector<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>The cloud connector associated with this L4/L7 service. This option is required when <code>state</code> is <code>present</code>.</div></td></tr>
            <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Name of the L4/L7 service.</div></td></tr>
            <tr>
    <td>parameters<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>A dictionary containing the values of input parameters that the service administrator has made available for tenant editing.</div></td></tr>
            <tr>
    <td>service_template<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>The Service Template that you want to base this L4/L7 Service off of. This option is required when <code>state</code> is <code>present</code>.</div></td></tr>
            <tr>
    <td>tenant<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>The tenant whose service is going to be managed. This is a required option when using the system's <code>admin</code> account as the admin is not a tenant, and therefore cannot manipulate any of the L4/L7 services that exist. If the <code>user</code> option is not the <code>admin</code> account, then this tenant option is assumed to be the user who is connecting to the BIG-IP. This assumption can always be changed by setting this option to whatever tenant you wish.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    


Notes
-----

.. note:: Requires the f5-sdk Python package on the remote host. This is as easy as pip install f5-sdk.
.. note:: L4/L7 Services cannot be updated once they have been created. Instead, you must first delete the service and then re-create it.


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

