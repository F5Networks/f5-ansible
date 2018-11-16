:source: bigip_log_destination.py

:orphan:

.. _bigip_log_destination_module:


bigip_log_destination - Manages log destinations on a BIG-IP.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.6

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manages log destinations on a BIG-IP.




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
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the IP address that will receive messages from the specified local Log Destination.</div>
                                                    <div>This parameter is only available when <code>type</code> is <code>management-port</code>.</div>
                                                    <div>When creating a new log destination and <code>type</code> is <code>management-port</code>, this parameter is required.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>description</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The description of the log destination.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>distribution</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>adaptive</li>
                                                                                                                                                                                                <li>balanced</li>
                                                                                                                                                                                                <li>replicated</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the distribution method used by the Remote High Speed Log destination to send messages to pool members.</div>
                                                    <div>When <code>adaptive</code>, connections to pool members will be added as required to provide enough logging bandwidth. This can have the undesirable effect of logs accumulating on only one pool member when it provides sufficient logging bandwidth on its own.</div>
                                                    <div>When <code>balanced</code>, sends each successive log to a new pool member, balancing the logs among them according to the pool&#x27;s load balancing method.</div>
                                                    <div>When <code>replicated</code>, replicates each log to all pool members, for redundancy.</div>
                                                    <div>When creating a new log destination and <code>type</code> is <code>remote-high-speed-log</code>, if this parameter is not specified, the default is <code>adaptive</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>forward_to</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>When <code>type</code> is <code>remote-syslog</code>, specifies the management port log destination, which will be used to forward the logs to a single log server, or a remote high-speed log destination, which will be used to forward the logs to a pool of remote log servers.</div>
                                                    <div>When <code>type</code> is <code>splunk</code> or <code>arcsight</code>, specifies the log destination to which logs are forwarded. This log destination may be a management port destination, a remote high-speed log destination, or a remote Syslog destination which is configured to send logs to an ArcSight or Splunk server.</div>
                                                    <div>When creating a new log destination and <code>type</code> is <code>remote-syslog</code>, <code>splunk</code>, or <code>arcsight</code>, this parameter is required.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the log destination.</div>
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
                                                                        <div>The password for the user account used to connect to the BIG-IP.</div>
                                                    <div>You may omit this option by setting the environment variable <code>F5_PASSWORD</code>.</div>
                                                                                        <div style="font-size: small; color: darkgreen"><br/>aliases: pass, pwd</div>
                                    </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>pool</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>When <code>type</code> is <code>remote-high-speed-log</code>, specifies the existing pool of remote high-speed log servers where logs will be sent.</div>
                                                    <div>When <code>type</code> is <code>ipfix</code>, specifies the existing LTM pool of remote IPFIX collectors. Any BIG-IP application that uses this log destination sends its IP-traffic logs to this pool of collectors.</div>
                                                    <div>When creating a new destination and <code>type</code> is <code>remote-high-speed-log</code> or <code>ipfix</code>, this parameter is required.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>pool_settings</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>This parameter is only available when <code>type</code> is <code>remote-high-speed-log</code>.</div>
                                                    <div>Deprecated. Use the equivalent top-level parameters instead.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>distribution</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>adaptive</li>
                                                                                                                                                                                                <li>balanced</li>
                                                                                                                                                                                                <li>replicated</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the distribution method used by the Remote High Speed Log destination to send messages to pool members.</div>
                                                    <div>When <code>adaptive</code>, connections to pool members will be added as required to provide enough logging bandwidth. This can have the undesirable effect of logs accumulating on only one pool member when it provides sufficient logging bandwidth on its own.</div>
                                                    <div>When <code>balanced</code>, sends each successive log to a new pool member, balancing the logs among them according to the pool&#x27;s load balancing method.</div>
                                                    <div>When <code>replicated</code>, replicates each log to all pool members, for redundancy.</div>
                                                    <div>When creating a new log destination (and <code>type</code> is <code>remote-high-speed-log</code>), if this parameter is not specified, the default is <code>adaptive</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>protocol</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>tcp</li>
                                                                                                                                                                                                <li>udp</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the protocol for the system to use to send logs to the pool of remote high-speed log servers, where the logs are stored.</div>
                                                    <div>When creating a new log destination (and <code>type</code> is <code>remote-high-speed-log</code>), if this parameter is not specified, the default is <code>tcp</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>pool</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the existing pool of remote high-speed log servers where logs will be sent.</div>
                                                    <div>When creating a new destination (and <code>type</code> is <code>remote-high-speed-log</code>), this parameter is required.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>port</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the port of the IP address that will receive messages from the specified local Log Destination.</div>
                                                    <div>This parameter is only available when <code>type</code> is <code>management-port</code>.</div>
                                                    <div>When creating a new log destination and <code>type</code> is <code>management-port</code>, this parameter is required.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>protocol</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>tcp</li>
                                                                                                                                                                                                <li>udp</li>
                                                                                                                                                                                                <li>ipfix</li>
                                                                                                                                                                                                <li>netflow-9</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>type</code> is <code>remote-high-speed-log</code>, specifies the protocol for the system to use to send logs to the pool of remote high-speed log servers, where the logs are stored.</div>
                                                    <div>When <code>type</code> is <code>ipfix</code>, can be IPFIX or Netflow v9, depending on the type of collectors you have in the pool that you specify.</div>
                                                    <div>When <code>type</code> is <code>management-port</code>, specifies the protocol used to send messages to the specified location.</div>
                                                    <div>When <code>type</code> is <code>management-port</code>, only <code>tcp</code> and <code>udp</code> are valid values.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>provider</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.5)</div>                </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                    </td>
                                                                <td>
                                                                        <div>A dict object containing connection details.</div>
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
                    <b>transport</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>rest</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>cli</li>
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
                    <b>server_ssl_profile</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>If the <code>transport_profile</code> is a TCP profile, you can use this field to choose a Secure Socket Layer (SSL) profile for sending logs to the IPFIX collectors.</div>
                                                    <div>An SSL server profile defines how to communicate securely over SSL or Transport Layer Security (TLS).</div>
                                                    <div>This parameter is only available when <code>type</code> is <code>ipfix</code>.</div>
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
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>present</code>, ensures that the resource exists.</div>
                                                    <div>When <code>absent</code>, ensures the resource is removed.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>syslog_format</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>bsd-syslog</li>
                                                                                                                                                                                                <li>syslog</li>
                                                                                                                                                                                                <li>legacy-bigip</li>
                                                                                                                                                                                                <li>rfc5424</li>
                                                                                                                                                                                                <li>rfc3164</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the method to use to format the logs associated with the remote Syslog log destination.</div>
                                                    <div>When creating a new log destination (and <code>type</code> is <code>remote-syslog</code>), if this parameter is not specified, the default is <code>bsd-syslog</code>.</div>
                                                    <div>The <code>syslog</code> and <code>rfc5424</code> choices are two ways of saying the same thing.</div>
                                                    <div>The <code>bsd-syslog</code> and <code>rfc3164</code> choices are two ways of saying the same thing.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>syslog_settings</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>This parameter is only available when <code>type</code> is <code>remote-syslog</code>.</div>
                                                    <div>Deprecated. Use the equivalent top-level parameters instead.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>syslog_format</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>bsd-syslog</li>
                                                                                                                                                                                                <li>syslog</li>
                                                                                                                                                                                                <li>legacy-bigip</li>
                                                                                                                                                                                                <li>rfc5424</li>
                                                                                                                                                                                                <li>rfc3164</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the method to use to format the logs associated with the remote Syslog log destination.</div>
                                                    <div>When creating a new log destination (and <code>type</code> is <code>remote-syslog</code>), if this parameter is not specified, the default is <code>bsd-syslog</code>.</div>
                                                    <div>The <code>syslog</code> and <code>rfc5424</code> choices are two ways of saying the same thing.</div>
                                                    <div>The <code>bsd-syslog</code> and <code>rfc3164</code> choices are two ways of saying the same thing.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>forward_to</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the management port log destination, which will be used to forward the logs to a single log server, or a remote high-speed log destination, which will be used to forward the logs to a pool of remote log servers.</div>
                                                    <div>When creating a new log destination (and <code>type</code> is <code>remote-syslog</code>), this parameter is required.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>template_delete_delay</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Enter the time (in seconds) that the BIG-IP device should pause between deleting an obsolete IPFIX template and reusing its template ID.</div>
                                                    <div>This feature is useful for systems where you use iRules to create customized IPFIX templates.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>template_retransmit_interval</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Enter the time (in seconds) between each transmission of IPFIX templates to the pool of IPFIX collectors.</div>
                                                    <div>The logging destination periodically retransmits all of its IPFIX templates at the interval you set in this field. These retransmissions are helpful for UDP, a lossy transport mechanism.</div>
                                                    <div>This parameter is only available when <code>type</code> is <code>ipfix</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>transport_profile</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.8)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Is a transport profile based on either TCP or UDP.</div>
                                                    <div>This profile defines the TCP or UDP options used to send IP-traffic logs to the pool of collectors.</div>
                                                    <div>This parameter is only available when <code>type</code> is <code>ipfix</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>type</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>remote-high-speed-log</li>
                                                                                                                                                                                                <li>remote-syslog</li>
                                                                                                                                                                                                <li>arcsight</li>
                                                                                                                                                                                                <li>splunk</li>
                                                                                                                                                                                                <li>management-port</li>
                                                                                                                                                                                                <li>ipfix</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the type of log destination.</div>
                                                    <div>Once created, this parameter cannot be changed.</div>
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

    
    - name: Create a high-speed logging destination
      bigip_log_destination:
        name: foo
        type: remote-high-speed-log
        pool: my-ltm-pool
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Create a remote-syslog logging destination
      bigip_log_destination:
        name: foo
        type: remote-syslog
        syslog_format: rfc5424
        forward_to: my-destination
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
                    <b>address</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Address value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">1.2.3.2</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>distribution</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Distribution Method value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">balanced</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>forward_to</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Forward To value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/dest1</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>pool</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Pool value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/pool1</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>port</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Port value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2020</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>protocol</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Protocol value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">tcp</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>server_ssl_profile</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Server SSL Profile value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/serverssl</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>syslog_format</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Syslog format value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">syslog</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>template_delete_delay</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Template Delete Delay value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">20</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>template_retransmit_interval</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Template Retransmit Interval value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">200</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>transport_profile</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new Transport Profile value.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/tcp</div>
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

