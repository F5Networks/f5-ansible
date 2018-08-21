:source: bigip_virtual_server.py

:orphan:

.. _bigip_virtual_server_module:


bigip_virtual_server - Manage LTM virtual servers on a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.1

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage LTM virtual servers on a BIG-IP.



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
                    <b>address_translation</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies, when <code>enabled</code>, that the system translates the address of the virtual server.</div>
                                                    <div>When <code>disabled</code>, specifies that the system uses the address without translation.</div>
                                                    <div>This option is useful when the system is load balancing devices that have the same IP address.</div>
                                                    <div>When creating a new virtual server, the default is <code>enabled</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>default_persistence_profile</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Default Profile which manages the session persistence.</div>
                                                    <div>If you want to remove the existing default persistence profile, specify an empty value; <code>&quot;&quot;</code>. See the documentation for an example.</div>
                                                    <div>When <code>type</code> is <code>dhcp</code>, this parameter will be ignored.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>description</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Virtual server description.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>destination</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Destination IP of the virtual server.</div>
                                                    <div>Required when <code>state</code> is <code>present</code> and virtual server does not exist.</div>
                                                    <div>When <code>type</code> is <code>internal</code>, this parameter is ignored. For all other types, it is required.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: address, ip</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>disabled_vlans</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>List of VLANs to be disabled. If the partition is not specified in the VLAN, then the <code>partition</code> option of this module will be used.</div>
                                                    <div>This parameter is mutually exclusive with the <code>enabled_vlans</code> parameters.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>enabled_vlans</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>List of VLANs to be enabled. When a VLAN named <code>all</code> is used, all VLANs will be allowed. VLANs can be specified with or without the leading partition. If the partition is not specified in the VLAN, then the <code>partition</code> option of this module will be used.</div>
                                                    <div>This parameter is mutually exclusive with the <code>disabled_vlans</code> parameter.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>fallback_persistence_profile</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.3)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the persistence profile you want the system to use if it cannot use the specified default persistence profile.</div>
                                                    <div>If you want to remove the existing fallback persistence profile, specify an empty value; <code>&quot;&quot;</code>. See the documentation for an example.</div>
                                                    <div>When <code>type</code> is <code>dhcp</code>, this parameter will be ignored.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>firewall_enforced_policy</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Applies the specify AFM policy to the virtual in an enforcing way.</div>
                                                    <div>When creating a new virtual, if this parameter is not specified, the enforced policy is disabled.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>firewall_staged_policy</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Applies the specify AFM policy to the virtual in an enforcing way.</div>
                                                    <div>A staged policy shows the results of the policy rules in the log, while not actually applying the rules to traffic.</div>
                                                    <div>When creating a new virtual, if this parameter is not specified, the staged policy is disabled.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ip_protocol</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>ah</li>
                                                                                                                                                                                                <li>bna</li>
                                                                                                                                                                                                <li>esp</li>
                                                                                                                                                                                                <li>etherip</li>
                                                                                                                                                                                                <li>gre</li>
                                                                                                                                                                                                <li>icmp</li>
                                                                                                                                                                                                <li>ipencap</li>
                                                                                                                                                                                                <li>ipv6</li>
                                                                                                                                                                                                <li>ipv6-auth</li>
                                                                                                                                                                                                <li>ipv6-crypt</li>
                                                                                                                                                                                                <li>ipv6-icmp</li>
                                                                                                                                                                                                <li>isp-ip</li>
                                                                                                                                                                                                <li>mux</li>
                                                                                                                                                                                                <li>ospf</li>
                                                                                                                                                                                                <li>sctp</li>
                                                                                                                                                                                                <li>tcp</li>
                                                                                                                                                                                                <li>udp</li>
                                                                                                                                                                                                <li>udplite</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies a network protocol name you want the system to use to direct traffic on this virtual server.</div>
                                                    <div>When creating a new virtual server, if this parameter is not specified, the default is <code>tcp</code>.</div>
                                                    <div>The Protocol setting is not available when you select Performance (HTTP) as the Type.</div>
                                                    <div>The value of this argument can be specified in either it&#x27;s numeric value, or, for convenience, in a select number of named values. Refer to <code>choices</code> for examples.</div>
                                                    <div>For a list of valid IP protocol numbers, refer to this page https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers</div>
                                                    <div>When <code>type</code> is <code>dhcp</code>, this module will force the <code>ip_protocol</code> parameter to be <code>17</code> (UDP).</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>irules</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>List of rules to be applied in priority order.</div>
                                                    <div>If you want to remove existing iRules, specify a single empty value; <code>&quot;&quot;</code>. See the documentation for an example.</div>
                                                    <div>When <code>type</code> is <code>dhcp</code>, this parameter will be ignored.</div>
                                                    <div>When <code>type</code> is <code>stateless</code>, this parameter will be ignored.</div>
                                                    <div>When <code>type</code> is <code>reject</code>, this parameter will be ignored.</div>
                                                    <div>When <code>type</code> is <code>internal</code>, this parameter will be ignored.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: all_rules</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>metadata</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Arbitrary key/value pairs that you can attach to a pool. This is useful in situations where you might want to annotate a virtual to me managed by Ansible.</div>
                                                    <div>Key names will be stored as strings; this includes names that are numbers.</div>
                                                    <div>Values for all of the keys will be stored as strings; this includes values that are numbers.</div>
                                                    <div>Data will be persisted, not ephemeral.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Virtual server name.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: vs</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>partition</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
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
                    <b>policies</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the policies for the virtual server.</div>
                                                    <div>When <code>type</code> is <code>dhcp</code>, this parameter will be ignored.</div>
                                                    <div>When <code>type</code> is <code>reject</code>, this parameter will be ignored.</div>
                                                    <div>When <code>type</code> is <code>internal</code>, this parameter will be ignored.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: all_policies</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>pool</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Default pool for the virtual server.</div>
                                                    <div>If you want to remove the existing pool, specify an empty value; <code>&quot;&quot;</code>. See the documentation for an example.</div>
                                                    <div>When creating a new virtual server, and <code>type</code> is <code>stateless</code>, this parameter is required.</div>
                                                    <div>If <code>type</code> is <code>stateless</code>, the <code>pool</code> that is used must not have any members which define a <code>rate_limit</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>port</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Port of the virtual server. Required when <code>state</code> is <code>present</code> and virtual server does not exist.</div>
                                                    <div>If you do not want to specify a particular port, use the value <code>0</code>. The result is that the virtual server will listen on any port.</div>
                                                    <div>When <code>type</code> is <code>dhcp</code>, this module will force the <code>port</code> parameter to be <code>67</code>.</div>
                                                    <div>When <code>type</code> is <code>internal</code>, this module will force the <code>port</code> parameter to be <code>0</code>.</div>
                                                    <div>In addition to specifying a port number, a select number of service names may also be provided.</div>
                                                    <div>The string <code>ftp</code> may be substituted for for port <code>21</code>.</div>
                                                    <div>The string <code>http</code> may be substituted for for port <code>80</code>.</div>
                                                    <div>The string <code>https</code> may be substituted for for port <code>443</code>.</div>
                                                    <div>The string <code>telnet</code> may be substituted for for port <code>23</code>.</div>
                                                    <div>The string <code>smtp</code> may be substituted for for port <code>25</code>.</div>
                                                    <div>The string <code>snmp</code> may be substituted for for port <code>161</code>.</div>
                                                    <div>The string <code>snmp-trap</code> may be substituted for for port <code>162</code>.</div>
                                                    <div>The string <code>ssh</code> may be substituted for for port <code>22</code>.</div>
                                                    <div>The string <code>tftp</code> may be substituted for for port <code>69</code>.</div>
                                                    <div>The string <code>isakmp</code> may be substituted for for port <code>500</code>.</div>
                                                    <div>The string <code>mqtt</code> may be substituted for for port <code>1883</code>.</div>
                                                    <div>The string <code>mqtt-tls</code> may be substituted for for port <code>8883</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>port_translation</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies, when <code>enabled</code>, that the system translates the port of the virtual server.</div>
                                                    <div>When <code>disabled</code>, specifies that the system uses the port without translation. Turning off port translation for a virtual server is useful if you want to use the virtual server to load balance connections to any service.</div>
                                                    <div>When creating a new virtual server, the default is <code>enabled</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>profiles</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>List of profiles (HTTP, ClientSSL, ServerSSL, etc) to apply to both sides of the connection (client-side and server-side).</div>
                                                    <div>If you only want to apply a particular profile to the client-side of the connection, specify <code>client-side</code> for the profile&#x27;s <code>context</code>.</div>
                                                    <div>If you only want to apply a particular profile to the server-side of the connection, specify <code>server-side</code> for the profile&#x27;s <code>context</code>.</div>
                                                    <div>If <code>context</code> is not provided, it will default to <code>all</code>.</div>
                                                    <div>If you want to remove a profile from the list of profiles currently active on the virtual, then simply remove it from the <code>profiles</code> list. See examples for an illustration of this.</div>
                                                    <div>If you want to add a profile to the list of profiles currently active on the virtual, then simply add it to the <code>profiles</code> list. See examples for an illustration of this.</div>
                                                    <div><b>Profiles matter</b>. This module will fail to configure a BIG-IP if you mix up your profiles, or, if you attempt to set an IP protocol which your current, or new, profiles do not support. Both this module, and BIG-IP, will tell you when you are wrong, with an error resembling <code>lists profiles incompatible with its protocol</code>.</div>
                                                    <div>If you are unsure what correct profile combinations are, then have a BIG-IP available to you in which you can make changes and copy what the correct combinations are.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: all_profiles</div>
                                    </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>name</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Name of the profile.</div>
                                                    <div>If this is not specified, then it is assumed that the profile item is only a name of a profile.</div>
                                                    <div>This must be specified if a context is specified.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>context</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>all</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>server-side</li>
                                                                                                                                                                                                <li>client-side</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The side of the connection on which the profile should be applied.</div>
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
                    <b>security_log_profiles</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the log profile applied to the virtual server.</div>
                                                    <div>To make use of this feature, the AFM module must be licensed and provisioned.</div>
                                                    <div>The <code>Log all requests</code> and <code>Log illegal requests</code> are mutually exclusive and therefore, this module will raise an error if the two are specified together.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>security_nat_policy</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.7)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specify the Firewall NAT policies for the virtual server.</div>
                                                    <div>You can specify one or more NAT policies to use.</div>
                                                    <div>The most specific policy is used. For example, if you specify that the virtual server use the device policy and the route domain policy, the route domain policy overrides the device policy.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>policy</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Policy to apply a NAT policy directly to the virtual server.</div>
                                                    <div>The virtual server NAT policy is the most specific, and overrides a route domain and device policy, if specified.</div>
                                                    <div>To remove the policy, specify an empty string value.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>use_device_policy</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specify that the virtual server uses the device NAT policy, as specified in the Firewall Options.</div>
                                                    <div>The device policy is used if no route domain or virtual server NAT setting is specified.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>use_route_domain_policy</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specify that the virtual server uses the route domain policy, as specified in the Route Domain Security settings.</div>
                                                    <div>When specified, the route domain policy overrides the device policy, and is overridden by a virtual server policy.</div>
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
                    <b>snat</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Source network address policy.</div>
                                                    <div>When <code>type</code> is <code>dhcp</code>, this parameter is ignored.</div>
                                                    <div>When <code>type</code> is <code>reject</code>, this parameter will be ignored.</div>
                                                    <div>When <code>type</code> is <code>internal</code>, this parameter will be ignored.</div>
                                                    <div>The name of a SNAT pool (eg &quot;/Common/snat_pool_name&quot;) can be specified to enable SNAT with the specific pool.</div>
                                                    <div>To remove SNAT, specify the word <code>none</code>.</div>
                                                    <div>To specify automap, use the word <code>automap</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>source</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies an IP address or network from which the virtual server accepts traffic.</div>
                                                    <div>The virtual server accepts clients only from one of these IP addresses.</div>
                                                    <div>For this setting to function effectively, specify a value other than 0.0.0.0/0 or ::/0 (that is, any/0, any6/0).</div>
                                                    <div>In order to maximize utility of this setting, specify the most specific address prefixes covering all customer addresses and no others.</div>
                                                    <div>Specify the IP address in Classless Inter-Domain Routing (CIDR) format; address/prefix, where the prefix length is in bits. For example, for IPv4, 10.0.0.1/32 or 10.0.0.0/24, and for IPv6, ffe1::0020/64 or 2001:ed8:77b5:2:10:10:100:42/64.</div>
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
                                                                        <div>The virtual server state. If <code>absent</code>, delete the virtual server if it exists. <code>present</code> creates the virtual server and enable it. If <code>enabled</code>, enable the virtual server if it exists. If <code>disabled</code>, create the virtual server if needed, and set state to <code>disabled</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>type</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>standard</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>forwarding-l2</li>
                                                                                                                                                                                                <li>forwarding-ip</li>
                                                                                                                                                                                                <li>performance-http</li>
                                                                                                                                                                                                <li>performance-l4</li>
                                                                                                                                                                                                <li>stateless</li>
                                                                                                                                                                                                <li>reject</li>
                                                                                                                                                                                                <li>dhcp</li>
                                                                                                                                                                                                <li>internal</li>
                                                                                                                                                                                                <li>message-routing</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the network service provided by this virtual server.</div>
                                                    <div>When creating a new virtual server, if this parameter is not provided, the default will be <code>standard</code>.</div>
                                                    <div>This value cannot be changed after it is set.</div>
                                                    <div>When <code>standard</code>, specifies a virtual server that directs client traffic to a load balancing pool and is the most basic type of virtual server. When you first create the virtual server, you assign an existing default pool to it. From then on, the virtual server automatically directs traffic to that default pool.</div>
                                                    <div>When <code>forwarding-l2</code>, specifies a virtual server that shares the same IP address as a node in an associated VLAN.</div>
                                                    <div>When <code>forwarding-ip</code>, specifies a virtual server like other virtual servers, except that the virtual server has no pool members to load balance. The virtual server simply forwards the packet directly to the destination IP address specified in the client request.</div>
                                                    <div>When <code>performance-http</code>, specifies a virtual server with which you associate a Fast HTTP profile. Together, the virtual server and profile increase the speed at which the virtual server processes HTTP requests.</div>
                                                    <div>When <code>performance-l4</code>, specifies a virtual server with which you associate a Fast L4 profile. Together, the virtual server and profile increase the speed at which the virtual server processes layer 4 requests.</div>
                                                    <div>When <code>stateless</code>, specifies a virtual server that accepts traffic matching the virtual server address and load balances the packet to the pool members without attempting to match the packet to a pre-existing connection in the connection table. New connections are immediately removed from the connection table. This addresses the requirement for one-way UDP traffic that needs to be processed at very high throughput levels, for example, load balancing syslog traffic to a pool of syslog servers. Stateless virtual servers are not suitable for processing traffic that requires stateful tracking, such as TCP traffic. Stateless virtual servers do not support iRules, persistence, connection mirroring, rateshaping, or SNAT automap.</div>
                                                    <div>When <code>reject</code>, specifies that the BIG-IP system rejects any traffic destined for the virtual server IP address.</div>
                                                    <div>When <code>dhcp</code>, specifies a virtual server that relays Dynamic Host Control Protocol (DHCP) client requests for an IP address to one or more DHCP servers, and provides DHCP server responses with an available IP address for the client.</div>
                                                    <div>When <code>internal</code>, specifies a virtual server that supports modification of HTTP requests and responses. Internal virtual servers enable usage of ICAP (Internet Content Adaptation Protocol) servers to modify HTTP requests and responses by creating and applying an ICAP profile and adding Request Adapt or Response Adapt profiles to the virtual server.</div>
                                                    <div>When <code>message-routing</code>, specifies a virtual server that uses a SIP application protocol and functions in accordance with a SIP session profile and SIP router profile.</div>
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
                        </table>
    <br/>


Notes
-----

.. note::
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as ``pip install f5-sdk``.


Examples
--------

.. code-block:: yaml

    
    - name: Modify Port of the Virtual Server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        state: present
        partition: Common
        name: my-virtual-server
        port: 8080
      delegate_to: localhost

    - name: Delete virtual server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        state: absent
        partition: Common
        name: my-virtual-server
      delegate_to: localhost

    - name: Add virtual server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        state: present
        partition: Common
        name: my-virtual-server
        destination: 10.10.10.10
        port: 443
        pool: my-pool
        snat: Automap
        description: Test Virtual Server
        profiles:
          - http
          - fix
          - name: clientssl
            context: server-side
          - name: ilx
            context: client-side
        policies:
          - my-ltm-policy-for-asm
          - ltm-uri-policy
          - ltm-policy-2
          - ltm-policy-3
        enabled_vlans:
          - /Common/vlan2
      delegate_to: localhost

    - name: Add FastL4 virtual server
      bigip_virtual_server:
        destination: 1.1.1.1
        name: fastl4_vs
        port: 80
        profiles:
          - fastL4
        state: present

    - name: Add iRules to the Virtual Server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        name: my-virtual-server
        irules:
          - irule1
          - irule2
      delegate_to: localhost

    - name: Remove one iRule from the Virtual Server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        name: my-virtual-server
        irules:
          - irule2
      delegate_to: localhost

    - name: Remove all iRules from the Virtual Server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        name: my-virtual-server
        irules: ""
      delegate_to: localhost

    - name: Remove pool from the Virtual Server
      bigip_virtual_server:
        server: lb.mydomain.net
        user: admin
        password: secret
        name: my-virtual-server
        pool: ""
      delegate_to: localhost

    - name: Add metadata to virtual
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: absent
        name: my-pool
        partition: Common
        metadata:
          ansible: 2.4
          updated_at: 2017-12-20T17:50:46Z
      delegate_to: localhost

    - name: Add virtual with two profiles
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: absent
        name: my-pool
        partition: Common
        profiles:
          - http
          - tcp
      delegate_to: localhost

    - name: Remove HTTP profile from previous virtual
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: absent
        name: my-pool
        partition: Common
        profiles:
          - tcp
      delegate_to: localhost

    - name: Add the HTTP profile back to the previous virtual
      bigip_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: absent
        name: my-pool
        partition: Common
        profiles:
          - http
          - tcp
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
                    <b>address_translation</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new value specifying whether address translation is on or off.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>default_persistence_profile</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Default persistence profile set on the virtual server.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/dest_addr</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>description</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>New description of the virtual server.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">This is my description</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>destination</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Destination of the virtual server.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">1.1.1.1</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>disabled</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Whether the virtual server is disabled, or not.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>disabled_vlans</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>List of VLANs that the virtual is disabled for.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;/Common/vlan1&#x27;, &#x27;/Common/vlan2&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>enabled</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Whether the virtual server is enabled, or not.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>enabled_vlans</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>List of VLANs that the virtual is enabled for.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;/Common/vlan5&#x27;, &#x27;/Common/vlan6&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>fallback_persistence_profile</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Fallback persistence profile set on the virtual server.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/source_addr</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>firewall_enforced_policy</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new enforcing firewall policy.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/my-enforced-fw</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>firewall_staged_policy</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new staging firewall policy.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/my-staged-fw</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>ip_protocol</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new value of the IP protocol.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">6</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>irules</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>iRules set on the virtual server.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;/Common/irule1&#x27;, &#x27;/Common/irule2&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>metadata</b>
                    <br/><div style="font-size: small; color: red">dict</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new value of the virtual.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;key1&#x27;: &#x27;foo&#x27;, &#x27;key2&#x27;: &#x27;bar&#x27;}</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>policies</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>List of policies attached to the virtual.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;/Common/policy1&#x27;, &#x27;/Common/policy2&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>pool</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Pool that the virtual server is attached to.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/my-pool</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>port</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Port that the virtual server is configured to listen on.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">80</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>port_translation</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new value specifying whether port translation is on or off.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>profiles</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>List of profiles set on the virtual server.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;name&#x27;: &#x27;tcp&#x27;, &#x27;context&#x27;: &#x27;server-side&#x27;}, {&#x27;name&#x27;: &#x27;tcp-legacy&#x27;, &#x27;context&#x27;: &#x27;client-side&#x27;}]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>security_log_profiles</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new list of security log profiles.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;/Common/profile1&#x27;, &#x27;/Common/profile2&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>snat</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>SNAT setting of the virtual server.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Automap</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>source</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Source address, in CIDR form, set on the virtual server.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">1.2.3.4/32</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>


Status
------



This module is **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Tim Rupp (@caphrim007)

