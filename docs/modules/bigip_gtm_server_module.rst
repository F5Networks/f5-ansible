.. _bigip_gtm_server:


bigip_gtm_server - Manages F5 BIG-IP GTM servers.
+++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage BIG-IP server configuration. This module is able to manipulate the server definitions in a BIG-IP.


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
                <tr><td>link_discovery<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Specifies whether the system auto-discovers the links for this server. When creating a new GTM server, the default value <code>disabled</code> is used.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The name of the server.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Device partition to manage resources on.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The BIG-IP host. This option can be omitted if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                <tr><td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>The BIG-IP server port. This option can be omitted if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                <tr><td>server_type<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>alteon-ace-director</li><li>cisco-css</li><li>cisco-server-load-balancer</li><li>generic-host</li><li>radware-wsd</li><li>windows-nt-4.0</li><li>bigip</li><li>cisco-local-director-v2</li><li>extreme</li><li>generic-load-balancer</li><li>sun-solaris</li><li>cacheflow</li><li>cisco-local-director-v3</li><li>foundry-server-iron</li><li>netapp</li><li>{u'windows-2000-servernotes': None}</li></ul></td>
        <td><div>Specifies the server type. The server type determines the metrics that the system can collect from the server. When creating a new GTM server, the default value <code>bigip</code> is used.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li><li>enabled</li><li>disabled</li></ul></td>
        <td><div>The server state. If <code>absent</code>, an attempt to delete the server will be made. This will only succeed if this server is not in use by a virtual server. <code>present</code> creates the server and enables it. If <code>enabled</code>, enable the server if it exists. If <code>disabled</code>, create the server if needed, and set state to <code>disabled</code>.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. This option can be omitted if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. This option can be omitted if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
                <tr><td>virtual_server_discovery<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Specifies whether the system auto-discovers the virtual servers for this server.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create server "GTM_Server"
      bigip_gtm_server:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          name: 'GTM_Server'
          datacenter: '/Common/New York'
          product: 'bigip'
          link_discovery: 'disabled'
          virtual_server_discovery: 'disabled'
          devices:
            - {'name': 'server_1', 'address': '1.1.1.1'}
            - {'name': 'server_2', 'address': '2.2.2.1', 'translation':'192.168.2.1'}
            - {'name': 'server_2', 'address': '2.2.2.2'}
            - {'name': 'server_3', 'addresses': [{'address':'3.3.3.1'},{'address':'3.3.3.2'}]}
            - {'name': 'server_4', 'addresses': [{'address':'4.4.4.1','translation':'192.168.14.1'}, {'address':'4.4.4.2'}]}
      delegate_to: localhost
    
    - name: Create server "GTM_Server" with expanded keys
      bigip_gtm_server:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          name: 'GTM_Server'
          datacenter: '/Common/New York'
          product: 'bigip'
          link_discovery: 'disabled'
          virtual_server_discovery: 'disabled'
          devices:
            - name: server_1
              address: '1.1.1.1'
            - name: 'server_2',
              address: '2.2.2.1',
              translation:'192.168.2.1'
            - name: 'server_2',
              address: '2.2.2.2'
            - name: 'server_3',
              addresses:
                - address:'3.3.3.1',
                - address:'3.3.3.2'
            - name': 'server_4', 'addresses': [{'address':'4.4.4.1','translation':'192.168.14.1'}, {'address':'4.4.4.2'}]}
      delegate_to: localhost


Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.