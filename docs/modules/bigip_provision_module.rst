.. _bigip_provision:


bigip_provision - Manage BIG-IP module provisioning
+++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage BIG-IP module provisioning. This module will only provision at the standard levels of Dedicated, Nominal, and Minimum.


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
                <tr><td>level<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>nominal</td>
        <td><ul><li>dedicated</li><li>nominal</li><li>minimum</li></ul></td>
        <td><div>Sets the provisioning level for the requested modules. Changing the level for one module may require modifying the level of another module. For example, changing one module to <code>dedicated</code> requires setting all others to <code>none</code>. Setting the level of a module to <code>none</code> means that the module is not activated.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul><li>am</li><li>afm</li><li>apm</li><li>asm</li><li>avr</li><li>fps</li><li>gtm</li><li>ilx</li><li>lc</li><li>ltm</li><li>pem</li><li>sam</li><li>swg</li><li>vcmp</li></ul></td>
        <td><div>The module to provision in BIG-IP.</div></br>
    <div style="font-size: small;">aliases: module<div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>The state of the provisioned module on the system. When <code>present</code>, guarantees that the specified module is provisioned at the requested level provided that there are sufficient resources on the device (such as physical RAM) to support the provisioned module. When <code>absent</code>, de-provision the module.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Provision PEM at "nominal" level
      bigip_provision:
        server: lb.mydomain.com
        module: pem
        level: nominal
        password: secret
        user: admin
        validate_certs: no
      delegate_to: localhost

    - name: Provision a dedicated SWG. This will unprovision every other module
      bigip_provision:
        server: lb.mydomain.com
        module: swg
        password: secret
        level: dedicated
        user: admin
        validate_certs: no
      delegate_to: localhost


Return Values
-------------

Common return values are `documented here <http://docs.ansible.com/ansible/latest/common_return_values.html>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">name</th>
    <th class="head">description</th>
    <th class="head">returned</th>
    <th class="head">type</th>
    <th class="head">sample</th>
    </tr>

        <tr>
        <td> level </td>
        <td> The new provisioning level of the module. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> minimum </td>
    </tr>
        
    </table>
    </br></br>

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