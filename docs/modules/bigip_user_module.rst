.. _bigip_user:


bigip_user - Manage user accounts and user attributes on a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage user accounts and user attributes on a BIG-IP. Typically this module operates only on the REST API users and not the CLI users. There is one exception though and that is if you specify the ``username_credential`` of ``root``. When specifying ``root``, you may only change the password. Your other parameters will be ignored in this case. Changing the ``root`` password is not an idempotent operation. Therefore, it will change it every time this module attempts to change it.


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
                <tr><td>full_name<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Full name of the user.</div>        </td></tr>
                <tr><td>partition_access<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the administrative partition to which the user has access. <code>partition_access</code> is required when creating a new account. Should be in the form "partition:role". Valid roles include <code>acceleration-policy-editor</code>, <code>admin</code>, <code>application-editor</code>, <code>auditor</code> <code>certificate-manager</code>, <code>guest</code>, <code>irule-manager</code>, <code>manager</code>, <code>no-access</code> <code>operator</code>, <code>resource-admin</code>, <code>user-manager</code>, <code>web-application-security-administrator</code>, and <code>web-application-security-editor</code>. Partition portion of tuple should be an existing partition or the value 'all'.</div>        </td></tr>
                <tr><td>password_credential<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Set the users password to this unencrypted value. <code>password_credential</code> is required when creating a new account.</div>        </td></tr>
                <tr><td>shell<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>bash</li><li>none</li><li>tmsh</li></ul></td>
        <td><div>Optionally set the users shell.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Whether the account should exist or not, taking action if the state is different from what is stated.</div>        </td></tr>
                <tr><td>update_password<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>on_create</td>
        <td><ul><li>always</li><li>on_create</li></ul></td>
        <td><div><code>always</code> will allow to update passwords if the user chooses to do so. <code>on_create</code> will only set the password for newly created users. When <code>username_credential</code> is <code>root</code>, this value will be forced to <code>always</code>.</div>        </td></tr>
                <tr><td>username_credential<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Name of the user to create, remove or modify. There is a special case that exists for the user <code>root</code>.</div></br>
    <div style="font-size: small;">aliases: name<div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Add the user 'johnd' as an admin
      bigip_user:
        server: lb.mydomain.com
        user: admin
        password: secret
        username_credential: johnd
        password_credential: password
        full_name: John Doe
        partition_access: all:admin
        update_password: on_create
        state: present
      delegate_to: localhost

    - name: Change the user "johnd's" role and shell
      bigip_user:
        server: lb.mydomain.com
        user: admin
        password: secret
        username_credential: johnd
        partition_access: NewPartition:manager
        shell: tmsh
        state: present
      delegate_to: localhost

    - name: Make the user 'johnd' an admin and set to advanced shell
      bigip_user:
        server: lb.mydomain.com
        user: admin
        password: secret
        name: johnd
        partition_access: all:admin
        shell: bash
        state: present
      delegate_to: localhost

    - name: Remove the user 'johnd'
      bigip_user:
        server: lb.mydomain.com
        user: admin
        password: secret
        name: johnd
        state: absent
      delegate_to: localhost

    - name: Update password
      bigip_user:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        username_credential: johnd
        password_credential: newsupersecretpassword
      delegate_to: localhost

    # Note that the second time this task runs, it would fail because
    # The password has been changed. Therefore, it is recommended that
    # you either,
    #
    #   * Put this in its own playbook that you run when you need to
    #   * Put this task in a `block`
    #   * Include `ignore_errors` on this task
    - name: Change the Admin password
      bigip_user:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: present
        username_credential: admin
        password_credential: NewSecretPassword
      delegate_to: localhost

    - name: Change the root user's password
      bigip_user:
        server: lb.mydomain.com
        user: admin
        password: secret
        username_credential: root
        password_credential: secret
        state: present
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

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - Requires BIG-IP versions >= 12.0.0
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.