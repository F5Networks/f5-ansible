.. _bigip_gtm_server:


bigip_gtm_server - Manages F5 BIG-IP GTM servers
++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage BIG-IP server configuration. This module is able to manipulate the server definitions in a BIG-IP.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.9


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
                <tr><td>datacenter<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Data center the server belongs to. When creating a new GTM server, this value is required.</div>        </td></tr>
                <tr><td>devices<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Lists the self IP addresses and translations for each device. When creating a new GTM server, this value is required. This list is a complex list that specifies a number of keys. There are several supported keys.</div><div>The <code>name</code> key specifies a name for the device. The device name must be unique per server. This key is required.</div><div>The <code>address</code> key contains an IP address, or list of IP addresses, for the destination server. This key is required.</div><div>The <code>translation</code> key contains an IP address to translate the <code>address</code> value above to. This key is optional.</div><div>Specifying duplicate <code>name</code> fields is a supported means of providing device addresses. In this scenario, the addresses will be assigned to the <code>name</code>&#x27;s list of addresses.</div>        </td></tr>
                <tr><td>link_discovery<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li><li>enabled-no-delete</li></ul></td>
        <td><div>Specifies whether the system auto-discovers the links for this server. When creating a new GTM server, if this parameter is not specified, the default value <code>disabled</code> is used.</div><div>If you set this parameter to <code>enabled</code> or <code>enabled-no-delete</code>, you must also ensure that the <code>virtual_server_discovery</code> parameter is also set to <code>enabled</code> or <code>enabled-no-delete</code>.</div>        </td></tr>
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
        <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div></br>
    <div style="font-size: small;">aliases: pass, pwd<div>        </td></tr>
                <tr><td rowspan="2">provider<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>A dict object containing connection details.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object provider</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>ssh_keyfile<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>        </td></tr>
                    <tr><td>timeout<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>10</td>
                <td></td>
                <td><div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>        </td></tr>
                    <tr><td>server<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                    <tr><td>user<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                    <tr><td>server_port<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>443</td>
                <td></td>
                <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                    <tr><td>password<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                    <tr><td>validate_certs<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>True</td>
                <td><ul><li>yes</li><li>no</li></ul></td>
                <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
                    <tr><td>transport<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td>cli</td>
                <td><ul><li>rest</li><li>cli</li></ul></td>
                <td><div>Configures the transport connection to use when connecting to the remote device.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                <tr><td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                <tr><td>server_type<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>alteon-ace-director</li><li>cisco-css</li><li>cisco-server-load-balancer</li><li>generic-host</li><li>radware-wsd</li><li>windows-nt-4.0</li><li>bigip</li><li>cisco-local-director-v2</li><li>extreme</li><li>generic-load-balancer</li><li>sun-solaris</li><li>cacheflow</li><li>cisco-local-director-v3</li><li>foundry-server-iron</li><li>netapp</li><li>windows-2000-server</li></ul></td>
        <td><div>Specifies the server type. The server type determines the metrics that the system can collect from the server. When creating a new GTM server, the default value <code>bigip</code> is used.</div></br>
    <div style="font-size: small;">aliases: product<div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li><li>enabled</li><li>disabled</li></ul></td>
        <td><div>The server state. If <code>absent</code>, an attempt to delete the server will be made. This will only succeed if this server is not in use by a virtual server. <code>present</code> creates the server and enables it. If <code>enabled</code>, enable the server if it exists. If <code>disabled</code>, create the server if needed, and set state to <code>disabled</code>.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
                <tr><td>virtual_server_discovery<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li><li>enabled-no-delete</li></ul></td>
        <td><div>Specifies whether the system auto-discovers the virtual servers for this server. When creating a new GTM server, if this parameter is not specified, the default value <code>disabled</code> is used.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create server "GTM_Server"
      bigip_gtm_server:
        server: lb.mydomain.com
        user: admin
        password: secret
        name: GTM_Server
        datacenter: /Common/New York
        server_type: bigip
        link_discovery: disabled
        virtual_server_discovery: disabled
        devices:
          - {'name': 'server_1', 'address': '1.1.1.1'}
          - {'name': 'server_2', 'address': '2.2.2.1', 'translation':'192.168.2.1'}
          - {'name': 'server_2', 'address': '2.2.2.2'}
          - {'name': 'server_3', 'addresses': [{'address':'3.3.3.1'},{'address':'3.3.3.2'}]}
          - {'name': 'server_4', 'addresses': [{'address':'4.4.4.1','translation':'192.168.14.1'}, {'address':'4.4.4.2'}]}
      delegate_to: localhost

    - name: Create server "GTM_Server" with expanded keys
      bigip_gtm_server:
        server: lb.mydomain.com
        user: admin
        password: secret
        name: GTM_Server
        datacenter: /Common/New York
        server_type: bigip
        link_discovery: disabled
        virtual_server_discovery: disabled
        devices:
          - name: server_1
            address: 1.1.1.1
          - name: server_2
            address: 2.2.2.1
            translation: 192.168.2.1
          - name: server_2
            address: 2.2.2.2
          - name: server_3
            addresses:
              - address: 3.3.3.1
              - address: 3.3.3.2
          - name: server_4
            addresses:
              - address: 4.4.4.1
                translation: 192.168.14.1
              - address: 4.4.4.2
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
        <td> link_discovery </td>
        <td> The new C(link_discovery) configured on the remote device. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> enabled </td>
    </tr>
            <tr>
        <td> server_type </td>
        <td> The new type of the server. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> bigip </td>
    </tr>
            <tr>
        <td> virtual_server_discovery </td>
        <td> The new C(virtual_server_discovery) name for the trap destination. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> disabled </td>
    </tr>
            <tr>
        <td> datacenter </td>
        <td> The new C(datacenter) which the server is part of. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> datacenter01 </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as ``pip install f5-sdk``.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.