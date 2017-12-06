.. _iworkflow_service_template:


iworkflow_service_template - Manages Service Templates on iWorkflow
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages Service Templates on iWorkflow. Service templates are created by the iWorkflow administrator and are consumed by iWorkflow tenants in the form of L4/L7 services. The Service Template can be configured to allow tenants to change certain values of the template such as the IP address of a VIP, or the port that a Virtual Server listens on.


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
                <tr><td>base_template<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The iApp template that you want to base this Service Template off of. Note that, while iWorkflow's UI also allows you to specify another Service Template for the <code>base_template</code>, this module does not yet let you do that. This option is required when <code>state</code> is <code>present</code>.</div>        </td></tr>
                <tr><td>connector<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The cloud connector associated with this Service Template. If you want to have this Service Template associated with all clouds, then specify a <code>connector</code> of <code>all</code>. When creating a new Service Template, if no connector is specified, then <code>all</code> clouds will be the default.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Name of the service template.</div>        </td></tr>
                <tr><td>parameters<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>A dictionary containing the values of input parameters that the Service Template contains. You will see these in iWorkflow's UI labeled as "Application Tier Information" and "Sections". This is the way by which you customize the Service Template and specify which values are tenant editable. Since this value can be particularly large, the recommended practice is to put it in an external file and include it with the Ansible <code>file</code> or <code>template</code> lookup plugins. This option is required when <code>state</code> is <code>present</code>.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    




Notes
-----

.. note::
    - Requires the f5-sdk Python package on the remote host. This is as easy as pip install f5-sdk
    - Requires the deepdiff Python package on the Ansible controller host. This is as easy as pip install deepdiff.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.