:source: bigip_vcmp_guest.py

:orphan:

.. _bigip_vcmp_guest_module:


bigip_vcmp_guest - Manages vCMP guests on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manages vCMP guests on a BIG-IP. This functionality only exists on actual hardware and must be enabled by provisioning ``vcmp`` with the ``bigip_provision`` module.



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- f5-sdk >= 3.0.9


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                    <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="2">
                    <b>allowed_slots</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.7)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Contains those slots that the guest is allowed to be assigned to.</div>
                                                    <div>When the host determines which slots this guest should be assigned to, only slots in this list will be considered.</div>
                                                    <div>This is a good way to force guests to be assigned only to particular slots, or, by configuring disjoint <code>allowed_slots</code> on two guests, that those guests are never assigned to the same slot.</div>
                                                    <div>By default this list includes every available slot in the cluster. This means, by default, the guest may be assigned to any slot.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>cores_per_slot</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the number of cores that the system allocates to the guest.</div>
                                                    <div>Each core represents a portion of CPU and memory. Therefore, the amount of memory allocated per core is directly tied to the amount of CPU. This amount of memory varies per hardware platform type.</div>
                                                    <div>The number you can specify depends on the type of hardware you have.</div>
                                                    <div>In the event of a reboot, the system persists the guest to the same slot on which it ran prior to the reboot.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>delete_virtual_disk</b>
                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>state</code> is <code>absent</code>, will additionally delete the virtual disk associated with the vCMP guest. By default, this value is <code>no</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>initial_image</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the base software release ISO image file for installing the TMOS hypervisor instance and any licensed BIG-IP modules onto the guest&#x27;s virtual disk. When creating a new guest, this parameter is required.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>mgmt_address</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the IP address, and subnet or subnet mask that you use to access the guest when you want to manage a module running within the guest. This parameter is required if the <code>mgmt_network</code> parameter is <code>bridged</code>.</div>
                                                    <div>When creating a new guest, if you do not specify a network or network mask, a default of <code>/24</code> (<code>255.255.255.0</code>) will be assumed.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>mgmt_network</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>bridged</li>
                                                                                                                                                                                                <li>isolated</li>
                                                                                                                                                                                                <li>host only</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the method by which the management address is used in the vCMP guest.</div>
                                                    <div>When <code>bridged</code>, specifies that the guest can communicate with the vCMP host&#x27;s management network.</div>
                                                    <div>When <code>isolated</code>, specifies that the guest is isolated from the vCMP host&#x27;s management network. In this case, the only way that a guest can communicate with the vCMP host is through the console port or through a self IP address on the guest that allows traffic through port 22.</div>
                                                    <div>When <code>host only</code>, prevents the guest from installing images and hotfixes other than those provided by the hypervisor.</div>
                                                    <div>If the guest setting is <code>isolated</code> or <code>host only</code>, the <code>mgmt_address</code> does not apply.</div>
                                                    <div>Concerning mode changing, changing <code>bridged</code> to <code>isolated</code> causes the vCMP host to remove all of the guest&#x27;s management interfaces from its bridged management network. This immediately disconnects the guest&#x27;s VMs from the physical management network. Changing <code>isolated</code> to <code>bridged</code> causes the vCMP host to dynamically add the guest&#x27;s management interfaces to the bridged management network. This immediately connects all of the guest&#x27;s VMs to the physical management network. Changing this property while the guest is in the <code>configured</code> or <code>provisioned</code> state has no immediate effect.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>mgmt_route</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the gateway address for the <code>mgmt_address</code>.</div>
                                                    <div>If this value is not specified when creating a new guest, it is set to <code>none</code>.</div>
                                                    <div>The value <code>none</code> can be used during an update to remove this value.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>min_number_of_slots</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.7)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the minimum number of slots that the guest must be assigned to in order to deploy.</div>
                                                    <div>This field dictates the number of slots that the guest must be assigned to.</div>
                                                    <div>If at the end of any allocation attempt the guest is not assigned to at least this many slots, the attempt fails and the change that initiated it is reverted.</div>
                                                    <div>A guest&#x27;s <code>min_number_of_slots</code> value cannot be greater than its <code>number_of_slots</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The name of the vCMP guest to manage.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>number_of_slots</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.7)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the number of slots for the system to use for creating the guest.</div>
                                                    <div>This value dictates how many cores a guest is allocated from each slot that it is assigned to.</div>
                                                    <div>Possible values are dependent on the type of blades being used in this cluster.</div>
                                                    <div>The default value depends on the type of blades being used in this cluster.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>partition</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">Common</div>
                                    </td>
                                                                <td>
                                                                        <div>Device partition to manage resources on.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>password</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: pass, pwd</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>provider</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>A dict object containing connection details.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>password</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: pass, pwd</div>
                                    </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>server_port</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">443</div>
                                    </td>
                                                                <td>
                                                                        <div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>user</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>validate_certs</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>timeout</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">10</div>
                                    </td>
                                                                <td>
                                                                        <div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>ssh_keyfile</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>transport</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>rest</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>cli</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Configures the transport connection to use when connecting to the remote device.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>server_port</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">443</div>
                                    </td>
                                                                <td>
                                                                        <div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>state</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>configured</li>
                                                                                                                                                                                                <li>disabled</li>
                                                                                                                                                                                                <li>provisioned</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>absent</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The state of the vCMP guest on the system. Each state implies the actions of all states before it.</div>
                                                    <div>When <code>configured</code>, guarantees that the vCMP guest exists with the provided attributes. Additionally, ensures that the vCMP guest is turned off.</div>
                                                    <div>When <code>disabled</code>, behaves the same as <code>configured</code> the name of this state is just a convenience for the user that is more understandable.</div>
                                                    <div>When <code>provisioned</code>, will ensure that the guest is created and installed. This state will not start the guest; use <code>deployed</code> for that. This state is one step beyond <code>present</code> as <code>present</code> will not install the guest; only setup the configuration for it to be installed.</div>
                                                    <div>When <code>present</code>, ensures the guest is properly provisioned and starts the guest so that it is in a running state.</div>
                                                    <div>When <code>absent</code>, removes the vCMP from the system.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>user</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>validate_certs</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.0)</div>                </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>vlans</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>VLANs that the guest uses to communicate with other guests, the host, and with the external network. The available VLANs in the list are those that are currently configured on the vCMP host.</div>
                                                    <div>The order of these VLANs is not important; in fact, it&#x27;s ignored. This module will order the VLANs for you automatically. Therefore, if you deliberately re-order them in subsequent tasks, you will find that this module will <b>not</b> register a change.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - This module can take a lot of time to deploy vCMP guests. This is an intrinsic limitation of the vCMP system because it is booting real VMs on the BIG-IP device. This boot time is very similar in length to the time it takes to boot VMs on any other virtualization platform; public or private.
    - When BIG-IP starts, the VMs are booted sequentially; not in parallel. This means that it is not unusual for a vCMP host with many guests to take a long time (60+ minutes) to reboot and bring all the guests online. The BIG-IP chassis will be available before all vCMP guests are online.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as ``pip install f5-sdk``.


Examples
--------

.. code-block:: yaml

    
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
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
                                                        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="1">
                    <b>vlans</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The VLANs assigned to the vCMP guest, in their full path format.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;/Common/vlan1&#x27;, &#x27;/Common/vlan2&#x27;]</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>


Status
------



This module is **stableinterface** which means that the maintainers for this module guarantee that no backward incompatible interface changes will be made.




Author
~~~~~~

- Tim Rupp (@caphrim007)

