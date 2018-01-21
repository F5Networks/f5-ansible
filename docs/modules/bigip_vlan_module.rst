.. _bigip_vlan:


bigip_vlan - Manage VLANs on a BIG-IP system
++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manage VLANs on a BIG-IP system


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
                <tr><td>cmp_hash<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies how the traffic on the VLAN will be disaggregated. The value selected determines the traffic disaggregation method. You can choose to disaggregate traffic based on <code>source-address</code> (the source IP address), <code>destination-address</code> (destination IP address), or <code>default</code>, which specifies that the default CMP hash uses L4 ports.</div><div>When creating a new VLAN, if this parameter is not specified, the default of <code>default</code> is used.</div>        </td></tr>
                <tr><td>dag_round_robin<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>Specifies whether some of the stateless traffic on the VLAN should be disaggregated in a round-robin order instead of using a static hash. The stateless traffic includes non-IP L2 traffic, ICMP, some UDP protocols, and so on.</div><div>When creating a new VLAN, if this parameter is not specified, the default of (no) is used.</div>        </td></tr>
                <tr><td>dag_tunnel<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies how the disaggregator (DAG) distributes received tunnel-encapsulated packets to TMM instances. Select <code>inner</code> to distribute packets based on information in inner headers. Select <code>outer</code> to distribute packets based on information in outer headers without inspecting inner headers.</div><div>When creating a new VLAN, if this parameter is not specified, the default of <code>outer</code> is used.</div><div>This parameter is not supported on Virtual Editions of BIG-IP.</div>        </td></tr>
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>The description to give to the VLAN.</div>        </td></tr>
                <tr><td>mtu<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the maximum transmission unit (MTU) for traffic on this VLAN. When creating a new VLAN, if this parameter is not specified, the default value used will be <code>1500</code>.</div><div>This number must be between 576 to 9198.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The VLAN to manage. If the special VLAN <code>ALL</code> is specified with the <code>state</code> value of <code>absent</code> then all VLANs will be removed.</div>        </td></tr>
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
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>absent</li><li>present</li></ul></td>
        <td><div>The state of the VLAN on the system. When <code>present</code>, guarantees that the VLAN exists with the provided attributes. When <code>absent</code>, removes the VLAN from the system.</div>        </td></tr>
                <tr><td>tag<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Tag number for the VLAN. The tag number can be any integer between 1 and 4094. The system automatically assigns a tag number if you do not specify a value.</div>        </td></tr>
                <tr><td>tagged_interfaces<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies a list of tagged interfaces and trunks that you want to configure for the VLAN. Use tagged interfaces or trunks when you want to assign a single interface or trunk to multiple VLANs.</div></br>
    <div style="font-size: small;">aliases: tagged_interface<div>        </td></tr>
                <tr><td>untagged_interfaces<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies a list of untagged interfaces and trunks that you want to configure for the VLAN.</div></br>
    <div style="font-size: small;">aliases: untagged_interface<div>        </td></tr>
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
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create VLAN
      bigip_vlan:
          name: "net1"
          password: "secret"
          server: "lb.mydomain.com"
          user: "admin"
          validate_certs: "no"
      delegate_to: localhost

    - name: Set VLAN tag
      bigip_vlan:
          name: "net1"
          password: "secret"
          server: "lb.mydomain.com"
          tag: "2345"
          user: "admin"
          validate_certs: "no"
      delegate_to: localhost

    - name: Add VLAN 2345 as tagged to interface 1.1
      bigip_vlan:
          tagged_interface: 1.1
          name: "net1"
          password: "secret"
          server: "lb.mydomain.com"
          tag: "2345"
          user: "admin"
          validate_certs: "no"
      delegate_to: localhost

    - name: Add VLAN 1234 as tagged to interfaces 1.1 and 1.2
      bigip_vlan:
          tagged_interfaces:
              - 1.1
              - 1.2
          name: "net1"
          password: "secret"
          server: "lb.mydomain.com"
          tag: "1234"
          user: "admin"
          validate_certs: "no"
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
        <td> tag </td>
        <td> The ID of the VLAN. </td>
        <td align=center> changed </td>
        <td align=center> int </td>
        <td align=center> 2345 </td>
    </tr>
            <tr>
        <td> description </td>
        <td> The description set on the VLAN. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> foo VLAN </td>
    </tr>
            <tr>
        <td> cmp_hash </td>
        <td> New traffic disaggregation method. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> source-address </td>
    </tr>
            <tr>
        <td> interfaces </td>
        <td> Interfaces that the VLAN is assigned to. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['1.1', '1.2'] </td>
    </tr>
            <tr>
        <td> partition </td>
        <td> The partition that the VLAN was created on. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> Common </td>
    </tr>
            <tr>
        <td> dag_tunnel </td>
        <td> The new DAG tunnel setting. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> outer </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires BIG-IP versions >= 12.0.0
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