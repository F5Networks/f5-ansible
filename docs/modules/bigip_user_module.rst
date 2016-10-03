.. _bigip_user:


bigip_user - Manage user accounts and user attributes on a BIG-IP.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage user accounts and user attributes on a BIG-IP.


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
    <td>append<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>yes</code>, will only add groups, not set them to just the list in groups.</div></td></tr>
            <tr>
    <td>full_name<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Full name of the user.</div></td></tr>
            <tr>
    <td>partition_access<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>all:no-access</td>
        <td><ul></ul></td>
        <td><div>Specifies the administrative partition to which the user has access. Should be in the form "partition:role". Valid roles include <code>acceleration-policy-editor</code>, <code>admin</code>, <code>application-editor</code>, <code>auditor</code> <code>certificate-manager</code>, <code>guest</code>, <code>irule-manager</code>, <code>manager</code>, <code>no-access</code> <code>operator</code>, <code>resource-admin</code>, <code>user-manager</code>, <code>web-application-security-administrator</code>, and <code>web-application-security-editor</code>. Partition portion of tuple should be an existing partition or the value 'all'.</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The password for the user account used to connect to the BIG-IP.</div></td></tr>
            <tr>
    <td>password_credential<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>Optionally set the users password to this unencrypted value. <code>password_credential</code> is required when creating a new account.</div></td></tr>
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
    <td>shell<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul><li>bash</li><li>none</li><li>tmsh</li></ul></td>
        <td><div>Optionally set the users shell.</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Whether the account should exist or not, taking action if the state is different from what is stated.</div></td></tr>
            <tr>
    <td>update_password<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>always</td>
        <td><ul><li>always</li><li>on_create</li></ul></td>
        <td><div><code>always</code> will update passwords if they differ. <code>on_create</code> will only set the password for newly created users.</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device.</div></td></tr>
            <tr>
    <td>username_credential<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Name of the user to create, remove or modify.</div></br>
        <div style="font-size: small;">aliases: user<div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: Add the user 'johnd' as an admin
      bigip_user:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          username_credential: "johnd"
          password_credential: "password"
          full_name: "John Doe"
          partition_access: "all:admin"
          state: "present"
      delegate_to: localhost
    
    - name: Change the user "johnd's" role and shell
      bigip_user:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          username_credential: "johnd"
          partition_access: "NewPartition:manager"
          shell: "tmsh"
          state: "present"
      delegate_to: localhost
    
    - name: Make the user 'johnd' an admin and set to advanced shell
      bigip_user:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          name: "johnd"
          partition_access: "all:admin"
          shell: "bash"
          state: "present"
      delegate_to: localhost
    
    - name: Remove the user 'johnd'
      bigip_user:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          name: "johnd"
          state: "absent"
      delegate_to: localhost
    
    - name: Update password
      bigip_user:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          state: "present"
          username_credential: "johnd"
          password_credential: "newsupersecretpassword"
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
        <td> shell </td>
        <td> The shell assigned to the user account </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> tmsh </td>
    </tr>
            <tr>
        <td> full_name </td>
        <td> Full name of the user </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> John Doe </td>
    </tr>
            <tr>
        <td> partition_access </td>
        <td> ['List of strings containing the user\'s roles and which partitions they are applied to. They are specified in the form "partition:role".'] </td>
        <td align=center> changed and success </td>
        <td align=center> list </td>
        <td align=center> ['all:admin'] </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note:: Requires the requests Python package on the host. This is as easy as pip install requests
.. note:: Requires BIG-IP versions >= 13.0.0


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

