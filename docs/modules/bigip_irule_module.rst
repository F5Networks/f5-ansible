.. _bigip_irule:


bigip_irule - Manage iRules across different modules on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage iRules across different modules on a BIG-IP


Requirements (on host that executes module)
-------------------------------------------

  * bigsuds
  * requests


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
    <td>connection<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>smart</td>
        <td><ul><li>rest</li><li>soap</li></ul></td>
        <td><div>The connection used to interface with the BIG-IP</div></td></tr>
            <tr>
    <td>content<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>When used instead of 'src', sets the contents of an iRule directly to the specified value. This is for simple values, but can be used with lookup plugins for anything complex or with formatting. Either one of <code>src</code> or <code>content</code> must be provided.</div></td></tr>
            <tr>
    <td>module<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul><li>ltm</li><li>gtm</li><li>pem</li></ul></td>
        <td><div>The BIG-IP module to add the iRule to</div></td></tr>
            <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The name of the iRule</div></td></tr>
            <tr>
    <td>partition<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Common</td>
        <td><ul></ul></td>
        <td><div>The partition to create the iRule on</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP password</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP host</div></td></tr>
            <tr>
    <td>src<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The iRule file to interpret and upload to the BIG-IP. Either one of <code>src</code> or <code>content</code> must be provided.</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Whether the iRule should exist or not</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP username</div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td><ul></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: Add the iRule contained in templated irule.tcl to the LTM module
      bigip_irule:
          content: "{{ lookup('template', 'irule-template.tcl') }}"
          module: "ltm"
          name: "MyiRule"
          password: "secret"
          server: "lb.mydomain.com"
          state: "present"
          user: "admin"
      delegate_to: localhost
    
    - name: Add the iRule contained in static file irule.tcl to the LTM module
      bigip_irule:
          module: "ltm"
          name: "MyiRule"
          password: "secret"
          server: "lb.mydomain.com"
          src: "irule-static.tcl"
          state: "present"
          user: "admin"
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
        <td> full_name </td>
        <td> Full name of the user </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> John Doe </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note:: Requires the bigsuds Python package on the host if using the iControl interface. This is as easy as pip install bigsuds
.. note:: Requires the requests Python package on the host. This is as easy as pip install requests


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

