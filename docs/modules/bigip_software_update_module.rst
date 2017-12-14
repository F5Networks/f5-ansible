.. _bigip_software_update:


bigip_software_update - Manage the software update settings of a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage the software update settings of a BIG-IP.


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
                <tr><td>auto_check<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>Specifies whether to automatically check for updates on the F5 Networks downloads server.</div>        </td></tr>
                <tr><td>frequency<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul><li>daily</li><li>monthly</li><li>weekly</li></ul></td>
        <td><div>Specifies the schedule for the automatic update check.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Enable automatic update checking
      bigip_software_update:
        auto_check: yes
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
      delegate_to: localhost



Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host This is as easy as pip install f5-sdk
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.