.. _bigip_remote_syslog:


bigip_remote_syslog - Manipulate remote syslog settings on a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manipulate remote syslog settings on a BIG-IP.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 2.2.0
  * netaddr


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
                <tr><td>local_ip<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the local IP address of the system that is logging. To provide no local IP, specify the value <code>none</code>. When creating a remote syslog, if this parameter is not specified, the default value <code>none</code> is used.</div>        </td></tr>
                <tr><td>remote_host<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Specifies the IP address, or hostname, for the remote system to which the system sends log messages.</div>        </td></tr>
                <tr><td>remote_port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the port that the system uses to send messages to the remote logging server. When creating a remote syslog, if this parameter is not specified, the default value <code>514</code> is used.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Add a remote syslog server to log to
      bigip_remote_syslog:
        remote_host: 10.10.10.10
        password: secret
        server: lb.mydomain.com
        user: admin
        validate_certs: no
      delegate_to: localhost

    - name: Add a remote syslog server on a non-standard port to log to
      bigip_remote_syslog:
        remote_host: 10.10.10.10
        remote_port: 1234
        password: secret
        server: lb.mydomain.com
        user: admin
        validate_certs: no
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
        <td> remote_port </td>
        <td> New remote port of the remote syslog server. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 514 </td>
    </tr>
            <tr>
        <td> local_ip </td>
        <td> The new local IP of the remote syslog server </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 10.10.10.10 </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - Requires the netaddr Python package on the host. This is as easy as pip install netaddr.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.