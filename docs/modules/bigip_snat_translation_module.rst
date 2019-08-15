:source: bigip_snat_translation.py

:orphan:

.. _bigip_snat_translation_module:


bigip_snat_translation - Manage SNAT Translations on a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.9

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage SNAT Translations on a BIG-IP.




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
                    <b>address</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the IP address of the SNAT translation. When a <code>state</code> of present, enabled, or disabled is provided, this parameter is required.</div>
                                                    <div>This parameter cannot be updated after it is set.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: ip</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>arp</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>If <code>yes</code>, specifies that the NAT sends ARP requests.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>connection_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies a limit on the number of connections a translation address must reach before it no longer initiates a connection. The default value of 0 indicates that the setting is disabled.</div>
                                                    <div>The accepted value range is <code>0 - 65535</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>description</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Description of snat-translation. <code>none or &#x27;&#x27;</code> will set to default description of null.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ip_idle_timeout</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the amount of time that connections to an IP address initiated using a SNAT address are allowed to remain idle before being automatically disconnected. <code>indefinite</code> prevents the connection from timing out.</div>
                                                    <div>The accepted value range is <code>0 - 4294967295</code> seconds, specifying <code>indefinite</code> will set it to the maximum value.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The name of SNAT translation.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>partition</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Device partition to manage resources on.</div>
                                                    <div>Required with state <code>absent</code> when partition other than Common used.</div>
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
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>auth_provider</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Configures the auth provider for to obtain authentication tokens from the remote device.</div>
                                                    <div>This option is really used when working with BIG-IQ devices.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>state</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>absent</li>
                                                                                                                                                                                                <li>enabled</li>
                                                                                                                                                                                                <li>disabled</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The SNAT translation state. If <code>absent</code>, delete the SNAT translation if it exists. <code>present</code> creates the SNAT translation and enable it. If <code>enabled</code>, enable the SNAT translation if it exists. If <code>disabled</code>, create the SNAT translation if needed, and set state to <code>disabled</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>tcp_idle_timeout</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the amount of time that TCP connections initiated using a SNAT address are allowed to remain idle before being automatically disconnected. <code>indefinite</code> Prevents the connection from timing out.</div>
                                                    <div>The accepted value range is <code>0 - 4294967295</code> seconds, specifying <code>indefinite</code> will set it to the maximum value.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>traffic_group</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The traffic group for the snat-translation address. When creating a new address, if this value is not specified, the default of <code>/Common/traffic-group-1</code> will be used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>udp_idle_timeout</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the amount of time that UDP connections initiated using a SNAT address are allowed to remain idle before being automatically disconnected. <code>indefinite</code> Prevents the connection from timing out.</div>
                                                    <div>The accepted value range is <code>0 - 4294967295</code> seconds, specifying <code>indefinite</code> will set it to the maximum value.</div>
                                                                                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires BIG-IP software version >= 12.
    - The F5 modules only manipulate the running configuration of the F5 product. To ensure that BIG-IP specific configuration persists to disk, be sure to include at least one task that uses the :ref:`bigip_config <bigip_config_module>` module to save the running configuration. Refer to the module's documentation for the correct usage of the module to save your running configuration.


Examples
--------

.. code-block:: yaml

    
    - name: Create a SNAT translation 'my-snat-translation'
      bigip_snat_translation:
        name: my-snat-pool
        state: present
        address: 10.10.10.10
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Modify a SNAT translation 'my-snat-translation'
      bigip_snat_translation:
        name: my-snat-pool
        state: present
        address: 10.10.10.10
        arp: no
        connection_limit: 300
        ip_idle_timeout: 1800
        tcp_idle_timeout: 1800
        udp_idle_timeout: 1800
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Disable a SNAT translation 'my-snat-translation'
      bigip_snat_translation:
        name: my-snat-pool
        state: disabled
        address: 10.10.10.10
        arp: no
        connection_limit: 300
        ip_idle_timeout: 1800
        tcp_idle_timeout: 1800
        udp_idle_timeout: 1800
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Enable a SNAT translation 'my-snat-translation'
      bigip_snat_translation:
        name: my-snat-pool
        state: enabled
        address: 10.10.10.10
        arp: no
        connection_limit: 300
        ip_idle_timeout: 1800
        tcp_idle_timeout: 1800
        udp_idle_timeout: 1800
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Create using partition other then /Common on a SNAT translation 'my-new-snat-translation'
      bigip_snat_translation:
        name: my-new-snat-pool
        state: enabled
        address: 10.10.10.10
        arp: no
        connection_limit: 300
        ip_idle_timeout: 1800
        partition: ansible
        tcp_idle_timeout: 1800
        udp_idle_timeout: 1800
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
      delegate_to: localhost

    - name: Modify using traffic group other then /Common/traffic-group-1 on a SNAT translation 'my-new-snat-translation'
      bigip_snat_translation:
        name: my-new-snat-pool
        state: enabled
        address: 10.10.10.10
        arp: no
        connection_limit: 300
        ip_idle_timeout: 1800
        partition: ansible
        tcp_idle_timeout: 1800
        traffic_group: /Common/ansible
        udp_idle_timeout: 1800
        provider:
          server: lb.mydomain.com
          user: admin
          password: secret
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
                    <b>address</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed and success</td>
                <td>
                                                                        <div>ip address used for SNAT translation.</div>
                                                                <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">10.10.10.10</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>arp</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Whether snat-translation send arp requests.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>connection_limit</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new connection limit of the virtual address.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">1000</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>description</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Description of the snat-translaiton.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">My snat-translation</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>ip_idle_timeout</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>IP idle timeout value for snat-translation.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">300</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>state</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new state of the snat-translation.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">disabled</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>tcp_idle_timeout</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>TCP idle timeout value for snat-translation.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">1800</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>traffic_group</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Assigned traffic group.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/traffic-group-1</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>udp_idle_timeout</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>UDP idle timeout value for snat-translation.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">indifinite</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>


Status
------



This module is **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Greg Crosby (@crosbygw)
- Wojciech Wypior (@wojtek0806)

