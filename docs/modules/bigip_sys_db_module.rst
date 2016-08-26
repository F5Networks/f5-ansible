.. _bigip_sys_db:


bigip_sys_db - Manage BIG-IP system database variables
++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage BIG-IP system database variables


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
            <tr>
    <td>key<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The database variable to manipulate.</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The password for the user account used to connect to the BIG-IP.</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The BIG-IP host.</div></td></tr>
            <tr>
    <td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td><ul></ul></td>
        <td><div>The BIG-IP server port.</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>reset</li></ul></td>
        <td><div>The state of the variable on the system. When <code>present</code>, guarantees that an existing variable is set to <code>value</code>. When <code>reset</code> sets the variable back to the default value. At least one of value and state <code>reset</code> are required.</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device.</div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div></td></tr>
            <tr>
    <td>value<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The value to set the key to. At least one of value and state <code>reset</code> are required.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: Set the boot.quiet DB variable on the BIG-IP
      bigip_sys_db:
          user: "admin"
          password: "secret"
          server: "lb.mydomain.com"
          key: "boot.quiet"
          value: "disable"
      delegate_to: localhost
    
    - name: Disable the initial setup screen
      bigip_sys_db:
          user: "admin"
          password: "secret"
          server: "lb.mydomain.com"
          key: "setup.run"
          value: "false"
      delegate_to: localhost
    
    - name: Reset the initial setup screen
      bigip_sys_db:
          user: "admin"
          password: "secret"
          server: "lb.mydomain.com"
          key: "setup.run"
          state: "reset"
      delegate_to: localhost

Return Values
-------------

Common return values are documented here :doc:`common_return_values`, the following are the fields unique to this module:

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
        <td align=center> true </td>
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
        <td align=center> false </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note:: Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
.. note:: Requires BIG-IP version 12.0.0 or greater


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

