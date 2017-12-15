.. _f5_support_upload:


f5_support_upload - Manage BIG-IP partitions
++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage BIG-IP partitions


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
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>The description to attach to the Partition</div>        </td></tr>
                <tr><td>route_domain<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>The default Route Domain to assign to the Partition. If no route domain is specified, then the default route domain for the system (typically zero) will be used only when creating a new partition. <code>route_domain</code> and <code>route_domain_id</code> are mutually exclusive.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create a ...
      {{ module }}:
        name: foo
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
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
        <td> param2 </td>
        <td> The new param2 value of the resource. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> Foo is bar </td>
    </tr>
            <tr>
        <td> param1 </td>
        <td> The new param1 value of the resource. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> True </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the bigsuds Python package on the host if using the iControl interface. This is as easy as pip install bigsuds
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.