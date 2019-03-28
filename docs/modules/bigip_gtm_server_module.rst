:source: bigip_gtm_server.py

:orphan:

.. _bigip_gtm_server_module:


bigip_gtm_server - Manages F5 BIG-IP GTM servers
++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage BIG-IP server configuration. This module is able to manipulate the server definitions in a BIG-IP.




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
                    <b>availability_requirements</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies, if you activate more than one health monitor, the number of health monitors that must receive successful responses in order for the link to be considered available.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>type</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>all</li>
                                                                                                                                                                                                <li>at_least</li>
                                                                                                                                                                                                <li>require</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Monitor rule type when <code>monitors</code> is specified.</div>
                                                    <div>When creating a new pool, if this value is not specified, the default of &#x27;all&#x27; will be used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>at_least</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the minimum number of active health monitors that must be successful before the link is considered up.</div>
                                                    <div>This parameter is only relevant when a <code>type</code> of <code>at_least</code> is used.</div>
                                                    <div>This parameter will be ignored if a type of either <code>all</code> or <code>require</code> is used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>number_of_probes</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the minimum number of probes that must succeed for this server to be declared up.</div>
                                                    <div>When creating a new virtual server, if this parameter is specified, then the <code>number_of_probers</code> parameter must also be specified.</div>
                                                    <div>The value of this parameter should always be <b>lower</b> than, or <b>equal to</b>, the value of <code>number_of_probers</code>.</div>
                                                    <div>This parameter is only relevant when a <code>type</code> of <code>require</code> is used.</div>
                                                    <div>This parameter will be ignored if a type of either <code>all</code> or <code>at_least</code> is used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>number_of_probers</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the number of probers that should be used when running probes.</div>
                                                    <div>When creating a new virtual server, if this parameter is specified, then the <code>number_of_probes</code> parameter must also be specified.</div>
                                                    <div>The value of this parameter should always be <b>higher</b> than, or <b>equal to</b>, the value of <code>number_of_probers</code>.</div>
                                                    <div>This parameter is only relevant when a <code>type</code> of <code>require</code> is used.</div>
                                                    <div>This parameter will be ignored if a type of either <code>all</code> or <code>at_least</code> is used.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>datacenter</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Data center the server belongs to. When creating a new GTM server, this value is required.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>devices</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Lists the self IP addresses and translations for each device. When creating a new GTM server, this value is required. This list is a complex list that specifies a number of keys.</div>
                                                    <div>The <code>name</code> key specifies a name for the device. The device name must be unique per server. This key is required.</div>
                                                    <div>The <code>address</code> key contains an IP address, or list of IP addresses, for the destination server. This key is required.</div>
                                                    <div>The <code>translation</code> key contains an IP address to translate the <code>address</code> value above to. This key is optional.</div>
                                                    <div>Specifying duplicate <code>name</code> fields is a supported means of providing device addresses. In this scenario, the addresses will be assigned to the <code>name</code>&#x27;s list of addresses.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>iquery_options</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.7)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the Global Traffic Manager uses this BIG-IP system to conduct a variety of probes before delegating traffic to it.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>allow_path</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies that the system verifies the logical network route between a data center server and a local DNS server.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>allow_service_check</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies that the system verifies that an application on a server is running, by remotely running the application using an external service checker program.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>allow_snmp</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies that the system checks the performance of a server running an SNMP agent.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>limits</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies resource thresholds or limit requirements at the pool member level.</div>
                                                    <div>When you enable one or more limit settings, the system then uses that data to take members in and out of service.</div>
                                                    <div>You can define limits for any or all of the limit settings. However, when a member does not meet the resource threshold limit requirement, the system marks the member as unavailable and directs load-balancing traffic to another resource.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>bits_enabled</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Whether the bits limit it enabled or not.</div>
                                                    <div>This parameter allows you to switch on or off the effect of the limit.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>packets_enabled</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Whether the packets limit it enabled or not.</div>
                                                    <div>This parameter allows you to switch on or off the effect of the limit.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>connections_enabled</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Whether the current connections limit it enabled or not.</div>
                                                    <div>This parameter allows you to switch on or off the effect of the limit.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>cpu_enabled</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Whether the CPU limit it enabled or not.</div>
                                                    <div>This parameter allows you to switch on or off the effect of the limit.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>memory_enabled</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Whether the memory limit it enabled or not.</div>
                                                    <div>This parameter allows you to switch on or off the effect of the limit.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>bits_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the maximum allowable data throughput rate, in bits per second, for the member.</div>
                                                    <div>If the network traffic volume exceeds this limit, the system marks the member as unavailable.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>packets_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the maximum allowable data transfer rate, in packets per second, for the member.</div>
                                                    <div>If the network traffic volume exceeds this limit, the system marks the member as unavailable.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>connections_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the maximum number of concurrent connections, combined, for all of the member.</div>
                                                    <div>If the connections exceed this limit, the system marks the server as unavailable.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>cpu_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the percent of CPU usage.</div>
                                                    <div>If percent of CPU usage goes above the limit, the system marks the server as unavailable.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>memory_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the available memory required by the virtual servers on the server.</div>
                                                    <div>If available memory falls below this limit, the system marks the server as unavailable.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>link_discovery</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>enabled</li>
                                                                                                                                                                                                <li>disabled</li>
                                                                                                                                                                                                <li>enabled-no-delete</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the system auto-discovers the links for this server. When creating a new GTM server, if this parameter is not specified, the default value <code>disabled</code> is used.</div>
                                                    <div>If you set this parameter to <code>enabled</code> or <code>enabled-no-delete</code>, you must also ensure that the <code>virtual_server_discovery</code> parameter is also set to <code>enabled</code> or <code>enabled-no-delete</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>monitors</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the health monitors that the system currently uses to monitor this resource.</div>
                                                    <div>When <code>availability_requirements.type</code> is <code>require</code>, you may only have a single monitor in the <code>monitors</code> list.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The name of the server.</div>
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
                                                                        <div>The password for the user account used to connect to the BIG-IP.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_PASSWORD</code>.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: pass, pwd</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>prober_fallback</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>any</li>
                                                                                                                                                                                                <li>inside-datacenter</li>
                                                                                                                                                                                                <li>outside-datacenter</li>
                                                                                                                                                                                                <li>inherit</li>
                                                                                                                                                                                                <li>pool</li>
                                                                                                                                                                                                <li>none</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the type of prober to use to monitor this server&#x27;s resources when the preferred prober is not available.</div>
                                                    <div>This option is ignored in <code>TMOS</code> version <code>12.x</code>.</div>
                                                    <div>From <code>TMOS</code> version <code>13.x</code> and up, when prober_preference is set to <code>pool</code> a <code>prober_pool</code> parameter must be specified.</div>
                                                    <div>The choices are mutually exclusive with prober_preference parameter, with the exception of <code>any-available</code> or <code>none</code> option.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>prober_pool</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the prober pool to use to monitor this server&#x27;s resources.</div>
                                                    <div>From <code>TMOS</code> version <code>13.x</code> and up, this parameter is mandatory when <code>prober_preference</code> is set to <code>pool</code>.</div>
                                                    <div>Format of the name can be either be prepended by partition (<code>/Common/foo</code>), or specified just as an object name (<code>foo</code>).</div>
                                                    <div>In <code>TMOS</code> version <code>12.x</code> prober_pool can be set to empty string to revert to default setting of inherit.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>prober_preference</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>inside-datacenter</li>
                                                                                                                                                                                                <li>outside-datacenter</li>
                                                                                                                                                                                                <li>inherit</li>
                                                                                                                                                                                                <li>pool</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the type of prober to use to monitor this server&#x27;s resources.</div>
                                                    <div>This option is ignored in <code>TMOS</code> version <code>12.x</code>.</div>
                                                    <div>From <code>TMOS</code> version <code>13.x</code> and up, when prober_preference is set to <code>pool</code> a <code>prober_pool</code> parameter must be specified.</div>
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
                                                                <td colspan="2">
                    <b>server_port</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.2)</div>                </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">443</div>
                                    </td>
                                                                <td>
                                                                        <div>The BIG-IP server port.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_SERVER_PORT</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>server_type</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>alteon-ace-director</li>
                                                                                                                                                                                                <li>cisco-css</li>
                                                                                                                                                                                                <li>cisco-server-load-balancer</li>
                                                                                                                                                                                                <li>generic-host</li>
                                                                                                                                                                                                <li>radware-wsd</li>
                                                                                                                                                                                                <li>windows-nt-4.0</li>
                                                                                                                                                                                                <li>bigip</li>
                                                                                                                                                                                                <li>cisco-local-director-v2</li>
                                                                                                                                                                                                <li>extreme</li>
                                                                                                                                                                                                <li>generic-load-balancer</li>
                                                                                                                                                                                                <li>sun-solaris</li>
                                                                                                                                                                                                <li>cacheflow</li>
                                                                                                                                                                                                <li>cisco-local-director-v3</li>
                                                                                                                                                                                                <li>foundry-server-iron</li>
                                                                                                                                                                                                <li>netapp</li>
                                                                                                                                                                                                <li>windows-2000-server</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the server type. The server type determines the metrics that the system can collect from the server. When creating a new GTM server, the default value <code>bigip</code> is used.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: product</div>
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
                                                                        <div>The server state. If <code>absent</code>, an attempt to delete the server will be made. This will only succeed if this server is not in use by a virtual server. <code>present</code> creates the server and enables it. If <code>enabled</code>, enable the server if it exists. If <code>disabled</code>, create the server if needed, and set state to <code>disabled</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
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
                                                                        <div>If <code>no</code>, SSL certificates are not validated. Use this only on personally controlled sites using self-signed certificates.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_VALIDATE_CERTS</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>virtual_server_discovery</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>enabled</li>
                                                                                                                                                                                                <li>disabled</li>
                                                                                                                                                                                                <li>enabled-no-delete</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the system auto-discovers the virtual servers for this server. When creating a new GTM server, if this parameter is not specified, the default value <code>disabled</code> is used.</div>
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

    
    - name: Create server "GTM_Server"
      bigip_gtm_server:
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
        provider:
          user: admin
          password: secret
          server: lb.mydomain.com
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
        provider:
          user: admin
          password: secret
          server: lb.mydomain.com
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
                    <b>bits_enabled</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Whether the bits limit is enabled.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>bits_limit</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new bits_enabled limit.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">100</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>connections_enabled</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Whether the connections limit is enabled.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>connections_limit</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new connections_limit limit.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">100</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>datacenter</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new <code>datacenter</code> which the server is part of.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">datacenter01</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>link_discovery</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new <code>link_discovery</code> configured on the remote device.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">enabled</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>monitors</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new list of monitors for the resource.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;/Common/monitor1&#x27;, &#x27;/Common/monitor2&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>packets_enabled</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Whether the packets limit is enabled.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>packets_limit</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new packets_limit limit.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">100</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>server_type</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new type of the server.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">bigip</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>virtual_server_discovery</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new <code>virtual_server_discovery</code> name for the trap destination.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">disabled</div>
                                    </td>
            </tr>
                        </table>
    <br/><br/>


Status
------



This module is **stableinterface** which means that the maintainers for this module guarantee that no backward incompatible interface changes will be made.




Author
~~~~~~

- Robert Teller (@r-teller)
- Tim Rupp (@caphrim007)
- Wojciech Wypior (@wojtek0806)

