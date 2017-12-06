.. _bigip_dns_record:


bigip_dns_record - Manage DNS resource records on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage DNS resource records on a BIG-IP


Requirements (on host that executes module)
-------------------------------------------

  * bigsuds
  * distutils


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
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>BIG-IP password</div>        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td>localhost</td>
        <td></td>
        <td><div>BIG-IP host</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>Whether the record should exist.  When <code>absent</code>, removes the record.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>BIG-IP username</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Add an A record to organization.com zone
      bigip_dns_record:
        user: admin
        password: secret
        hostname: lb.mydomain.com
        type: A
        zone: organization.com
        state: present
        options:
          hostname: elliot.organization.com
          ip_address: 10.1.1.1
      delegate_to: localhost

    - name: Add an A record to organization.com zone
      local_action:
        module: bigip_dns_record
        user: admin
        password: secret
        hostname: lb.mydomain.com
        type: A
        zone: organization.com
        state: present
        ttl: 10
        options:
          domain_name: elliot.organization.com
          ip_address: 10.1.1.1



Notes
-----

.. note::
    - Requires the bigsuds Python package on the remote host. This is as easy as pip install bigsuds



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.