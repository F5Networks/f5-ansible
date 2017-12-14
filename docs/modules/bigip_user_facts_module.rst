.. _bigip_user_facts:


bigip_user_facts - Retrieve user account attributes from a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Retrieve user account attributes from a BIG-IP


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
                <tr><td>username_credential<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Name of the user to retrieve facts for</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Gather facts about user 'johnd'
      bigip_user_facts:
        name: johnd
        password: secret
        server: lb.mydomain.com
        user: admin
        validate_certs: no
      delegate_to: localhost

    - name: Display the user facts
      debug:
        var: bigip


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
        <td> encrypted_password </td>
        <td> The encrypted value of the password </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> $6$/cgtFz0....yzv465uAJ/ </td>
    </tr>
            <tr>
        <td> username_credential </td>
        <td> The username beign searched for </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> jdoe </td>
    </tr>
            <tr>
        <td> description </td>
        <td> The description of the user </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> John Doe </td>
    </tr>
            <tr>
        <td> partition_access </td>
        <td> Access permissions for the account </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> [{'role': 'admin', 'name': 'all-partitions'}] </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk
    - Facts are placed in the ``bigip`` variable
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.