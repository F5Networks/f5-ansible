:source: bigiq_device_discovery.py

:orphan:

.. _bigiq_device_discovery_module:


bigiq_device_discovery - Manage BIG-IP devices through BIG-IQ
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.8

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Discovers and imports BIG-IP device configuration on the BIG-IQ.




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
                    <b>access_conflict_policy</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>use_bigiq</li>
                                                                                                                                                                                                <li>use_bigip</li>
                                                                                                                                                                                                <li>keep_version</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Sets the conflict resolution policy for Access module <code>apm</code> objects, only used when <code>apm</code> module is specified.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>access_group_first_device</b>
                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies if the imported device is the first device in the access group to import shared configuration for that access group.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>access_group_name</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Access group name to import Access configuration for devices, once set it cannot be changed.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>conflict_policy</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>use_bigiq</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>use_bigip</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Sets the conflict resolution policy for shared objects across BIG-IP devices, except LTM profiles and monitors.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>device_address</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The IP address of the BIG-IP device to be imported/managed.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>device_conflict_policy</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>use_bigiq</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>use_bigip</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Sets the conflict resolution policy for objects that are specific to a particular to a BIG-IP device and not shared among BIG-IP devices.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>device_password</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The administrator password for the BIG-IP device.</div>
                                                    <div>This parameter is only required when adding a new BIG-IP device to be managed.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>device_port</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">443</div>
                                    </td>
                                                                <td>
                                                                        <div>The port on which a device trust setup between BIG-IQ and BIG-IP should happen.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>device_username</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The administrator username for the BIG-IP device.</div>
                                                    <div>This parameter is only required when adding a new BIG-IP device to be managed.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>force</b>
                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Forces rediscovery and import of existing modules on the managed BIG-IP</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ha_name</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>DSC cluster name of the BIG-IP device to be managed.</div>
                                                    <div>This is optional if the managed device is not a part of a cluster group.</div>
                                                    <div>When <code>use_bigiq_sync</code> is set to <code>yes</code> then this parameter becomes mandatory.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>modules</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>ltm</li>
                                                                                                                                                                                                <li>asm</li>
                                                                                                                                                                                                <li>apm</li>
                                                                                                                                                                                                <li>afm</li>
                                                                                                                                                                                                <li>dns</li>
                                                                                                                                                                                                <li>websafe</li>
                                                                                                                                                                                                <li>security_shared</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>List of modules to be discovered and imported into the device.</div>
                                                    <div>These modules must be provisioned on the target device otherwise operation will fail.</div>
                                                    <div>The <code>ltm</code> module must always be specified when performing discovery or re-discovery of the the device.</div>
                                                    <div>When <code>asm</code> or <code>afm</code> are specified <code>shared_security</code> module needs to also be declared.</div>
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
                                                                        <div>The password for the user account used to connect to the BIG-IP.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_PASSWORD</code>.</div>
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
                                                                        <div>The BIG-IP host.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_SERVER</code>.</div>
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
                                                                        <div>The BIG-IP server port.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_SERVER_PORT</code>.</div>
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
                                                                        <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_USER</code>.</div>
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
                                                                        <div>If <code>no</code>, SSL certificates are not validated. Use this only on personally controlled sites using self-signed certificates.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_VALIDATE_CERTS</code>.</div>
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
                                                                        <div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports.</div>
                                                    <div>You may omit this option by setting the environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>transport</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>cli</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>rest</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Configures the transport connection to use when connecting to the remote device.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>state</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>absent</li>
                                                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The state of the managed device on the system.</div>
                                                    <div>When <code>present</code>, enables new device addition as well as device rediscovery/import.</div>
                                                    <div>When <code>absent</code>, completely removes the device from the system.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>statistics</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specify the statistics collection for discovered device.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>enable</b>
                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Enables statistics collection on a device</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>interval</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>30</li>
                                                                                                                                                                                                <li>60</li>
                                                                                                                                                                                                <li>120</li>
                                                                                                                                                                                                <li>500</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specify the interval in seconds the data is collected from the discovered device.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>zone</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">default</div>
                                    </td>
                                                                <td>
                                                                        <div>Specify in which DCD zone is collecting the data from device.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>stat_modules</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>device</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li><div style="color: blue"><b>ltm</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>dns</li>
                                                                                    </ul>
                                                                                    <b>Default:</b><br/><div style="color: blue">[&#39;device&#39;, &#39;ltm&#39;]</div>
                                    </td>
                                                                <td>
                                                                        <div>Specifies for which modules the data is being collected.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>use_bigiq_sync</b>
                                                        </td>
                                <td>
                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When set to true, BIG-IQ will manually synchronize configuration changes between members in a DSC cluster.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>versioned_conflict_policy</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>use_bigiq</li>
                                                                                                                                                                                                <li>use_bigip</li>
                                                                                                                                                                                                <li>keep_version</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Sets the conflict resolution policy for LTM profile and monitor objects that are specific to a BIG-IP software version.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - BIG-IQ >= 6.1.0.
    - This module does not support atomic removal of discovered modules on the device.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires BIG-IP software version >= 12.
    - The F5 modules only manipulate the running configuration of the F5 product. To ensure that BIG-IP specific configuration persists to disk, be sure to include at least one task that uses the :ref:`bigip_config <bigip_config_module>` module to save the running configuration. Refer to the module's documentation for the correct usage of the module to save your running configuration.


Examples
--------

.. code-block:: yaml

    
    - name: Discover a new device and import config, use default conflict policy.
      bigiq_device_discovery:
        device_address: 192.168.1.1
        device_username: bigipadmin
        device_password: bigipsecret
        modules:
          - ltm
          - afm
          - shared_security
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Discover a new device and import config, use non- default conflict policy.
      bigiq_device_discovery:
        device_address: 192.168.1.1
        modules:
          - ltm
          - dns
        conflict_policy: use_bigip
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Force full device rediscovery
      bigiq_device_discovery:
        device_address: 192.168.1.1
        modules:
          - ltm
          - afm
          - dns
          - shared_security
        force: yes
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Remove discovered device and its config
      bigiq_device_discovery:
        device_address: 192.168.1.1
        state: absent
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost




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
                    <b>access_conflict_policy</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Sets the conflict resolution policy for Access module <code>apm</code> objects.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">keep_version</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>access_group_first_device</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>First device in the access group to import shared configuration for that access group.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>access_group_name</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Access group name to import Access configuration for devices.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">foo_group</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>conflict_policy</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Sets the conflict resolution policy for shared objects across BIG-IP devices.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">use_bigip</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>device_address</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The IP address of the BIG-IP device to be imported/managed.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">192.168.1.1</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>device_conflict_policy</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Sets the conflict resolution policy for objects that are specific to a particular to a BIG-IP device.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">use_bigip</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>device_port</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The port on which a device trust setup between BIG-IQ and BIG-IP should happen.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">10443</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>ha_name</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>DSC cluster name of the BIG-IP device to be managed.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">GROUP_1</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>modules</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>List of modules to be discovered and imported into the device.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ltm&#x27;, &#x27;dns&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>use_bigiq_sync</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Indicate if BIG-IQ should manually synchronise DSC configuration.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>versioned_conflict_policy</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Sets the conflict resolution policy for LTM profile and monitor objects.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">keep_version</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>


Status
------



This module is **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Wojciech Wypior (@wojtek0806)

