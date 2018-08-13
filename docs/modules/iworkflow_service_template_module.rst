:source: iworkflow_service_template.py

:orphan:

.. _iworkflow_service_template_module:


iworkflow_service_template - Manages Service Templates on iWorkflow
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manages Service Templates on iWorkflow. Service templates are created by the iWorkflow administrator and are consumed by iWorkflow tenants in the form of L4/L7 services. The Service Template can be configured to allow tenants to change certain values of the template such as the IP address of a VIP, or the port that a Virtual Server listens on.



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
                    <b>base_template</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The iApp template that you want to base this Service Template off of. Note that, while iWorkflow&#x27;s UI also allows you to specify another Service Template for the <code>base_template</code>, this module does not yet let you do that. This option is required when <code>state</code> is <code>present</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>connector</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The cloud connector associated with this Service Template. If you want to have this Service Template associated with all clouds, then specify a <code>connector</code> of <code>all</code>. When creating a new Service Template, if no connector is specified, then <code>all</code> clouds will be the default.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Name of the service template.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>parameters</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>A dictionary containing the values of input parameters that the Service Template contains. You will see these in iWorkflow&#x27;s UI labeled as &quot;Application Tier Information&quot; and &quot;Sections&quot;. This is the way by which you customize the Service Template and specify which values are tenant editable. Since this value can be particularly large, the recommended practice is to put it in an external file and include it with the Ansible <code>file</code> or <code>template</code> lookup plugins. This option is required when <code>state</code> is <code>present</code>.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - Requires the deepdiff Python package on the Ansible controller host. This is as easy as pip install deepdiff.


Examples
--------

.. code-block:: yaml

    
    - name: Create a ...
      iworkflow_service_template:
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

