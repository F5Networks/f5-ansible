.. _bigip_selfip:


bigip_selfip - Manage Self-IPs on a BIG-IP system
+++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage Self-IPs on a BIG-IP system.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.9
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
                <tr><td>address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The IP addresses for the new self IP. This value is ignored upon update as addresses themselves cannot be changed after they are created.</div>        </td></tr>
                <tr><td>allow_service<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Configure port lockdown for the Self IP. By default, the Self IP has a &quot;default deny&quot; policy. This can be changed to allow TCP and UDP ports as well as specific protocols. This list should contain <code>protocol</code>:<code>port</code> values.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td>Value of C(address)</td>
        <td></td>
        <td><div>The self IP to create.</div>        </td></tr>
                <tr><td>netmask<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The netmask for the self IP. When creating a new Self IP, this value is required.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Device partition to manage resources on. You can set different partitions for Self IPs, but the address used may not match any other address used by a Self IP. In that sense, Self IPs are not isolated by partitions as other resources on a BIG-IP are.</div>        </td></tr>
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
                <tr><td>route_domain<br/><div style="font-size: small;"> (added in 2.3)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The route domain id of the system. When creating a new Self IP, if this value is not specified, a default value of <code>0</code> will be used.</div>        </td></tr>
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
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>absent</li><li>present</li></ul></td>
        <td><div>When <code>present</code>, guarantees that the Self-IP exists with the provided attributes.</div><div>When <code>absent</code>, removes the Self-IP from the system.</div>        </td></tr>
                <tr><td>traffic_group<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The traffic group for the Self IP addresses in an active-active, redundant load balancer configuration. When creating a new Self IP, if this value is not specified, the default of <code>/Common/traffic-group-local-only</code> will be used.</div>        </td></tr>
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
                <tr><td>vlan<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The VLAN that the new self IPs will be on. When creating a new Self IP, this value is required.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create Self IP
      bigip_selfip:
        address: 10.10.10.10
        name: self1
        netmask: 255.255.255.0
        password: secret
        server: lb.mydomain.com
        user: admin
        validate_certs: no
        vlan: vlan1
      delegate_to: localhost

    - name: Create Self IP with a Route Domain
      bigip_selfip:
        server: lb.mydomain.com
        user: admin
        password: secret
        validate_certs: no
        name: self1
        address: 10.10.10.10
        netmask: 255.255.255.0
        vlan: vlan1
        route_domain: 10
        allow_service: default
      delegate_to: localhost

    - name: Delete Self IP
      bigip_selfip:
        name: self1
        password: secret
        server: lb.mydomain.com
        state: absent
        user: admin
        validate_certs: no
      delegate_to: localhost

    - name: Allow management web UI to be accessed on this Self IP
      bigip_selfip:
        name: self1
        password: secret
        server: lb.mydomain.com
        state: absent
        user: admin
        validate_certs: no
        allow_service:
          - tcp:443
      delegate_to: localhost

    - name: Allow HTTPS and SSH access to this Self IP
      bigip_selfip:
        name: self1
        password: secret
        server: lb.mydomain.com
        state: absent
        user: admin
        validate_certs: no
        allow_service:
          - tcp:443
          - tcp:22
      delegate_to: localhost

    - name: Allow all services access to this Self IP
      bigip_selfip:
        name: self1
        password: secret
        server: lb.mydomain.com
        state: absent
        user: admin
        validate_certs: no
        allow_service:
          - all
      delegate_to: localhost

    - name: Allow only GRE and IGMP protocols access to this Self IP
      bigip_selfip:
        name: self1
        password: secret
        server: lb.mydomain.com
        state: absent
        user: admin
        validate_certs: no
        allow_service:
          - gre:0
          - igmp:0
      delegate_to: localhost

    - name: Allow all TCP, but no other protocols access to this Self IP
      bigip_selfip:
        name: self1
        password: secret
        server: lb.mydomain.com
        state: absent
        user: admin
        validate_certs: no
        allow_service:
          - tcp:0
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
        <td> netmask </td>
        <td> The netmask of the Self IP </td>
        <td align=center> changed and created </td>
        <td align=center> string </td>
        <td align=center> 255.255.255.0 </td>
    </tr>
            <tr>
        <td> name </td>
        <td> The name of the Self IP </td>
        <td align=center> created, changed and deleted </td>
        <td align=center> string </td>
        <td align=center> self1 </td>
    </tr>
            <tr>
        <td> address </td>
        <td> The address for the Self IP </td>
        <td align=center> created </td>
        <td align=center> string </td>
        <td align=center> 192.0.2.10 </td>
    </tr>
            <tr>
        <td> traffic_group </td>
        <td> The traffic group that the Self IP is a member of </td>
        <td align=center> changed and created </td>
        <td align=center> string </td>
        <td align=center> traffic-group-local-only </td>
    </tr>
            <tr>
        <td> vlan </td>
        <td> The VLAN set on the Self IP </td>
        <td align=center> changed and created </td>
        <td align=center> string </td>
        <td align=center> vlan1 </td>
    </tr>
            <tr>
        <td> allow_service </td>
        <td> Services that allowed via this Self IP </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['igmp:0', 'tcp:22', 'udp:53'] </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the netaddr Python package on the host.
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