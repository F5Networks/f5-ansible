.. _bigip_security_port_list:


bigip_security_port_list - Manage port lists on BIG-IP AFM.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages the AFM port lists on a BIG-IP. This module can be used to add and remove port list entries.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.4


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
    <td></td>
        <td></td>
        <td><div>Description of the port list</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Specifies the name of the port list.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Device partition to manage resources on.</div>        </td></tr>
                <tr><td>port_lists<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Simple list of existing port lists to add to this list. Port lists can be specified in either their fully qualified name (/Common/foo) or their short name (foo). If a short name is used, the <code>partition</code> argument will automatically be prepended to the short name.</div>        </td></tr>
                <tr><td>port_ranges<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>A list of port ranges where the range starts with a port number, is followed by a dash (-) and then a second number.</div><div>If the first number is greater than the second number, the numbers will be reversed so-as to be properly formatted. ie, 90-78 would become 78-90.</div>        </td></tr>
                <tr><td>ports<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Simple list of port values to add to the list</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create a simple port list
      bigip_security_port_list:
        name: foo
        ports:
          - 80
          - 443
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
      delegate_to: localhost

    - name: Override the above list of ports with a new list
      bigip_security_port_list:
        name: foo
        ports:
          - 3389
          - 8080
          - 25
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
      delegate_to: localhost

    - name: Create port list with series of ranges
      bigip_security_port_list:
        name: foo
        port_ranges:
          - 25-30
          - 80-500
          - 50-78
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
      delegate_to: localhost

    - name: Use multiple types of port arguments
      bigip_security_port_list:
        name: foo
        port_ranges:
          - 25-30
          - 80-500
          - 50-78
        ports:
          - 8080
          - 443
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
      delegate_to: localhost

    - name: Remove port list
      bigip_security_port_list:
        name: foo
        password: secret
        server: lb.mydomain.com
        state: absent
        user: admin
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
        <td> port_ranges </td>
        <td> The new list of port ranges applied to the port list </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['80-100', '200-8080'] </td>
    </tr>
            <tr>
        <td> ports </td>
        <td> The new list of ports applied to the port list </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> [80, 443] </td>
    </tr>
            <tr>
        <td> port_lists </td>
        <td> The new list of port list names applied to the port list </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['/Common/list1', '/Common/list2'] </td>
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