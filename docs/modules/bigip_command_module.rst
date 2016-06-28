.. _bigip_command:


bigip_command - Run commands on a BIG-IP via tmsh
+++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Run commands on a BIG-IP via tmsh. This module is similar to the ansible ``command`` module, but specifically supports all BIG-IPs via the paramiko python extension. For some operations on the BIG-IP, there is not a SOAP or REST endpoint that is available and the operation can only be accomplished via ``tmsh``. The Ansible ``command`` module should be able to perform this, however, older releases of BIG-IP do not have sufficient python versions to support Ansible. By using this module, there is no need for python to exist on the remote BIG-IP. Additionally, this module can detect the presence of Appliance Mode on a BIG-IP and adjust the provided command to take this feature into account. Finally, the output of this module provides more Ansible-friendly data formats than could be accomplished by the ``command`` module alone.


Requirements (on host that executes module)
-------------------------------------------

  * paramiko
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
    <td>command<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>tmsh command to run on the remote host</div></td></tr>
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

    - name: Load the default system configuration
      bigip_command:
          server: "bigip.localhost.localdomain"
          user: "admin"
          password: "admin"
          command: "tmsh load sys config default"
          validate_certs: "no"
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
        <td> command </td>
        <td> The command specified by the user </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> tmsh list auth user </td>
    </tr>
            <tr>
        <td> app_mode_cmd </td>
        <td> The command as it would have been run in Appliance mode </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> list auth user </td>
    </tr>
            <tr>
        <td> app_mode </td>
        <td> Whether or not Appliance mode was detected for the user </td>
        <td align=center> changed </td>
        <td align=center> boolean </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> stderr </td>
        <td> The stderr output from running the given command </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center>  </td>
    </tr>
            <tr>
        <td> stdout </td>
        <td> The stdout output from running the given command </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center>  </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note:: Requires the paramiko Python package on the ansible host. This is as easy as pip install paramiko


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

