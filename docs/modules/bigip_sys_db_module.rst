.. _bigip_sys_db:


bigip_sys_db - Manage BIG-IP system database variables
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage BIG-IP system database variables


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk


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
                <tr><td>key<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The database variable to manipulate.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>reset</li></ul></td>
        <td><div>The state of the variable on the system. When <code>present</code>, guarantees that an existing variable is set to <code>value</code>. When <code>reset</code> sets the variable back to the default value. At least one of value and state <code>reset</code> are required.</div>        </td></tr>
                <tr><td>value<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The value to set the key to. At least one of value and state <code>reset</code> are required.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Set the boot.quiet DB variable on the BIG-IP
      bigip_sys_db:
        user: admin
        password: secret
        server: lb.mydomain.com
        key: boot.quiet
        value: disable
      delegate_to: localhost

    - name: Disable the initial setup screen
      bigip_sys_db:
        user: admin
        password: secret
        server: lb.mydomain.com
        key: setup.run
        value: false
      delegate_to: localhost

    - name: Reset the initial setup screen
      bigip_sys_db:
        user: admin
        password: secret
        server: lb.mydomain.com
        key: setup.run
        state: reset
      delegate_to: localhost


Return Values
-------------

Common return values are :doc:`documented here <http://docs.ansible.com/ansible/latest/common_return_values.html>`, the following are the fields unique to this module:

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
        <td> default_value </td>
        <td> The default value of the key </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> name </td>
        <td> The key in the system database that was specified </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> setup.run </td>
    </tr>
            <tr>
        <td> value </td>
        <td> The value that you set the key to </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> False </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - Requires BIG-IP version 12.0.0 or greater
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.