.. _bigip_snat_pool:


bigip_snat_pool - Manage SNAT pools on a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage SNAT pools on a BIG-IP.


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
                <tr><td>members<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>List of members to put in the SNAT pool. When a <code>state</code> of present is provided, this parameter is required. Otherwise, it is optional.</div></br>
    <div style="font-size: small;">aliases: member<div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The name of the SNAT pool.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Device partition to manage resources on.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Whether the SNAT pool should exist or not.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Add the SNAT pool 'my-snat-pool'
      bigip_snat_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        name: my-snat-pool
        state: present
        members:
          - 10.10.10.10
          - 20.20.20.20
      delegate_to: localhost

    - name: Change the SNAT pool's members to a single member
      bigip_snat_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        name: my-snat-pool
        state: present
        member: 30.30.30.30
      delegate_to: localhost

    - name: Remove the SNAT pool 'my-snat-pool'
      bigip_snat_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        name: johnd
        state: absent
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
        <td> members </td>
        <td> ['List of members that are part of the SNAT pool.'] </td>
        <td align=center> changed and success </td>
        <td align=center> list </td>
        <td align=center> ['10.10.10.10'] </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk
    - Requires the netaddr Python package on the host. This is as easy as pip install netaddr
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.