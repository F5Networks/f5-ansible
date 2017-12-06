.. __bigip_facts:


_bigip_facts - Collect facts from F5 BIG-IP devices
+++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 1.6


.. contents::
   :local:
   :depth: 2

DEPRECATED
----------

Deprecated in 2.5. Use individual facts modules instead.

Synopsis
--------

* Collect facts from F5 BIG-IP devices via iControl SOAP API


Requirements (on host that executes module)
-------------------------------------------

  * bigsuds


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
                <tr><td>filter<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Shell-style glob matching string used to filter fact keys. Not applicable for software, provision, and system_info fact categories.</div>        </td></tr>
                <tr><td>include<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul><li>address_class</li><li>certificate</li><li>client_ssl_profile</li><li>device</li><li>device_group</li><li>interface</li><li>key</li><li>node</li><li>pool</li><li>provision</li><li>rule</li><li>self_ip</li><li>software</li><li>system_info</li><li>traffic_group</li><li>trunk</li><li>virtual_address</li><li>virtual_server</li><li>vlan</li></ul></td>
        <td><div>Fact category or list of categories to collect</div>        </td></tr>
                <tr><td>session<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td></td>
        <td><div>BIG-IP session support; may be useful to avoid concurrency issues in certain circumstances.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Collect BIG-IP facts
      bigip_facts:
        server: lb.mydomain.com
        user: admin
        password: secret
        include: interface,vlan
      delegate_to: localhost



Notes
-----

.. note::
    - Requires BIG-IP software version >= 11.4
    - F5 developed module 'bigsuds' required (see http://devcentral.f5.com)
    - Best run as a local_action in your playbook
    - Tested with manager and above account privilege level
    - ``provision`` facts were added in 2.2
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.