:source: bigip_dns_record.py

:orphan:

.. _bigip_dns_record_module:


bigip_dns_record - Manage DNS resource records on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage DNS resource records on a BIG-IP



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- bigsuds
- distutils


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
                                                                                                                                                                        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="1">
                    <b>password</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>BIG-IP password</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">localhost</div>
                                    </td>
                                                                <td>
                                                                        <div>BIG-IP host</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>state</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>absent</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Whether the record should exist.  When <code>absent</code>, removes the record.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <b>user</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>BIG-IP username</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - Requires the bigsuds Python package on the remote host. This is as easy as pip install bigsuds


Examples
--------

.. code-block:: yaml

    
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





Status
------



This module is **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Tim Rupp (@caphrim007)

