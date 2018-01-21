.. _bigip_vcmp_guest:


bigip_vcmp_guest - Manages vCMP guests on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages vCMP guests on a BIG-IP. This functionality only exists on actual hardware and must be enabled by provisioning ``vcmp`` with the ``bigip_provision`` module.


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
                <tr><td>cores_per_slot<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the number of cores that the system allocates to the guest.</div><div>Each core represents a portion of CPU and memory. Therefore, the amount of memory allocated per core is directly tied to the amount of CPU. This amount of memory varies per hardware platform type.</div><div>The number you can specify depends on the type of hardware you have.</div><div>In the event of a reboot, the system persists the guest to the same slot on which it ran prior to the reboot.</div>        </td></tr>
                <tr><td>delete_virtual_disk<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>When <code>state</code> is <code>absent</code>, will additionally delete the virtual disk associated with the vCMP guest. By default, this value is <code>no</code>.</div>        </td></tr>
                <tr><td>initial_image<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the base software release ISO image file for installing the TMOS hypervisor instance and any licensed BIG-IP modules onto the guest&#x27;s virtual disk. When creating a new guest, this parameter is required.</div>        </td></tr>
                <tr><td>mgmt_address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the IP address, and subnet or subnet mask that you use to access the guest when you want to manage a module running within the guest. This parameter is required if the <code>mgmt_network</code> parameter is <code>bridged</code>.</div><div>When creating a new guest, if you do not specify a network or network mask, a default of <code>/24</code> (<code>255.255.255.0</code>) will be assumed.</div>        </td></tr>
                <tr><td>mgmt_network<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>bridged</li><li>isolated</li><li>host only</li></ul></td>
        <td><div>Specifies the method by which the management address is used in the vCMP guest.</div><div>When <code>bridged</code>, specifies that the guest can communicate with the vCMP host&#x27;s management network.</div><div>When <code>isolated</code>, specifies that the guest is isolated from the vCMP host&#x27;s management network. In this case, the only way that a guest can communicate with the vCMP host is through the console port or through a self IP address on the guest that allows traffic through port 22.</div><div>When <code>host only</code>, prevents the guest from installing images and hotfixes other than those provided by the hypervisor.</div><div>If the guest setting is <code>isolated</code> or <code>host only</code>, the <code>mgmt_address</code> does not apply.</div><div>Concerning mode changing, changing <code>bridged</code> to <code>isolated</code> causes the vCMP host to remove all of the guest&#x27;s management interfaces from its bridged management network. This immediately disconnects the guest&#x27;s VMs from the physical management network. Changing <code>isolated</code> to <code>bridged</code> causes the vCMP host to dynamically add the guest&#x27;s management interfaces to the bridged management network. This immediately connects all of the guest&#x27;s VMs to the physical management network. Changing this property while the guest is in the <code>configured</code> or <code>provisioned</code> state has no immediate effect.</div>        </td></tr>
                <tr><td>mgmt_route<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the gateway address for the <code>mgmt_address</code>.</div><div>If this value is not specified when creating a new guest, it is set to <code>none</code>.</div><div>The value <code>none</code> can be used during an update to remove this value.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The name of the vCMP guest to manage.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"></div></td>
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
        <td><ul><li>configured</li><li>disabled</li><li>provisioned</li><li>present</li><li>absent</li></ul></td>
        <td><div>The state of the vCMP guest on the system. Each state implies the actions of all states before it.</div><div>When <code>configured</code>, guarantees that the vCMP guest exists with the provided attributes. Additionally, ensures that the vCMP guest is turned off.</div><div>When <code>disabled</code>, behaves the same as <code>configured</code> the name of this state is just a convenience for the user that is more understandable.</div><div>When <code>provisioned</code>, will ensure that the guest is created and installed. This state will not start the guest; use <code>deployed</code> for that. This state is one step beyond <code>present</code> as <code>present</code> will not install the guest; only setup the configuration for it to be installed.</div><div>When <code>present</code>, ensures the guest is properly provisioned and starts the guest so that it is in a running state.</div><div>When <code>absent</code>, removes the vCMP from the system.</div>        </td></tr>
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
                <tr><td>vlans<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>VLANs that the guest uses to communicate with other guests, the host, and with the external network. The available VLANs in the list are those that are currently configured on the vCMP host.</div><div>The order of these VLANs is not important; in fact, it&#x27;s ignored. This module will order the VLANs for you automatically. Therefore, if you deliberately re-order them in subsequent tasks, you will find that this module will <b>not</b> register a change.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create a vCMP guest
      bigip_vcmp_guest:
        name: foo
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
        mgmt_network: bridge
        mgmt_address: 10.20.30.40/24
      delegate_to: localhost

    - name: Create a vCMP guest with specific VLANs
      bigip_vcmp_guest:
        name: foo
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
        mgmt_network: bridge
        mgmt_address: 10.20.30.40/24
        vlans:
          - vlan1
          - vlan2
      delegate_to: localhost

    - name: Remove vCMP guest and disk
      bigip_vcmp_guest:
        name: guest1
        state: absent
        delete_virtual_disk: yes
      register: result


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
        <td> vlans </td>
        <td> The VLANs assigned to the vCMP guest, in their full path format. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['/Common/vlan1', '/Common/vlan2'] </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - This module can take a lot of time to deploy vCMP guests. This is an intrinsic limitation of the vCMP system because it is booting real VMs on the BIG-IP device. This boot time is very similar in length to the time it takes to boot VMs on any other virtualization platform; public or private.
    - When BIG-IP starts, the VMs are booted sequentially; not in parallel. This means that it is not unusual for a vCMP host with many guests to take a long time (60+ minutes) to reboot and bring all the guests online. The BIG-IP chassis will be available before all vCMP guests are online.
    - netaddr
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