:source: bigip_monitor_dns.py

:orphan:

.. _bigip_monitor_dns_module:


bigip_monitor_dns - Manage DNS monitors on a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.7

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manages DNS monitors on a BIG-IP.



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
                    <b>accept_rcode</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>no-error</li>
                                                                                                                                                                                                <li>anything</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the RCODE required in the response for an up status.</div>
                                                    <div>When creating a new monitor, if this parameter is not specified, the default value is <code>no-error</code>.</div>
                                                    <div>When <code>no-error</code>, specifies that the status of the node will be marked up if the received DNS message has no error.</div>
                                                    <div>When <code>anything</code>, specifies that the status of the node will be marked up irrespective of the RCODE in the DNS message received.</div>
                                                    <div>If this parameter is set to <code>anything</code>, it will disregard the <code>receive</code> string, and nullify it if the monitor is being updated.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>adaptive</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether adaptive response time monitoring is enabled for this monitor.</div>
                                                    <div>When <code>yes</code>, the monitor determines the state of a service based on how divergent from the mean latency a monitor probe for that service is allowed to be. Also, values for the <code>allowed_divergence</code>, <code>adaptive_limit</code>, and and <code>sampling_timespan</code> will be enforced.</div>
                                                    <div>When <code>disabled</code>, the monitor determines the state of a service based on the <code>interval</code>, <code>up_interval</code>, <code>time_until_up</code>, and <code>timeout</code> monitor settings.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>adaptive_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the absolute number of milliseconds that may not be exceeded by a monitor probe, regardless of <code>allowed_divergence</code> setting, for a probe to be considered successful.</div>
                                                    <div>This value applies regardless of the value of the <code>allowed_divergence</code> setting.</div>
                                                    <div>While this value can be configured when <code>adaptive</code> is <code>no</code>, it will not take effect on the system until <code>adaptive</code> is <code>yes</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>allowed_divergence_type</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>relative</li>
                                                                                                                                                                                                <li>absolute</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When specifying a new monitor, if <code>adaptive</code> is <code>yes</code>, the default is <code>relative</code></div>
                                                    <div>When <code>absolute</code>, the number of milliseconds the latency of a monitor probe can exceed the mean latency of a monitor probe for the service being probed. In typical cases, if the monitor detects three probes in a row that miss the latency value you set, the pool member or node is marked down.</div>
                                                    <div>When <code>relative</code>, the percentage of deviation the latency of a monitor probe can exceed the mean latency of a monitor probe for the service being probed.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>allowed_divergence_value</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>When specifying a new monitor, if <code>adaptive</code> is <code>yes</code>, and <code>type</code> is <code>relative</code>, the default is <code>25</code> percent.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>answer_section_contains</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>any-type</li>
                                                                                                                                                                                                <li>anything</li>
                                                                                                                                                                                                <li>query-type</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the type of DNS query that the monitor sends.</div>
                                                    <div>When creating a new monitor, if this value is not specified, the default value is <code>query-type</code>.</div>
                                                    <div>When <code>query-type</code>, specifies that the response should contain at least one answer of which the resource record type matches the query type.</div>
                                                    <div>When <code>any-type</code>, specifies that the DNS message should contain at least one answer.</div>
                                                    <div>When <code>anything</code>, specifies that an empty answer is enough to mark the status of the node up.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>description</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The description of the monitor.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>interval</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The interval specifying how frequently the monitor instance of this template will run.</div>
                                                    <div>This value <b>must</b> be less than the <code>timeout</code> value.</div>
                                                    <div>When creating a new monitor, if this parameter is not provided, the default <code>5</code> will be used.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>ip</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>IP address part of the IP/port definition.</div>
                                                    <div>If this parameter is not provided when creating a new monitor, then the default value will be <code>*</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>manual_resume</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the system automatically changes the status of a resource to <b>enabled</b> at the next successful monitor check.</div>
                                                    <div>If you set this option to <code>yes</code>, you must manually re-enable the resource before the system can use it for load balancing connections.</div>
                                                    <div>When creating a new monitor, if this parameter is not specified, the default value is <code>no</code>.</div>
                                                    <div>When <code>yes</code>, specifies that you must manually re-enable the resource after an unsuccessful monitor check.</div>
                                                    <div>When <code>no</code>, specifies that the system automatically changes the status of a resource to <b>enabled</b> at the next successful monitor check.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the monitor.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>parent</b>
                                                        </td>
                                <td>
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">/Common/dns</div>
                                    </td>
                                                                <td>
                                                                        <div>The parent template of this monitor template. Once this value has been set, it cannot be changed. By default, this value is the <code>dns</code> parent on the <code>Common</code> partition.</div>
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
                    <b>port</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Port address part of the IP/port definition.</div>
                                                    <div>If this parameter is not provided when creating a new monitor, then the default value will be <code>*</code>.</div>
                                                    <div>Note that if specifying an IP address, a value between 1 and 65535 must be specified.</div>
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
                    <b>query_name</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies a query name for the monitor to use in a DNS query.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>query_type</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>a</li>
                                                                                                                                                                                                <li>aaaa</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the type of DNS query that the monitor sends.</div>
                                                    <div>When creating a new monitor, if this parameter is not specified, the default value is <code>a</code>.</div>
                                                    <div>When <code>a</code>, specifies that the monitor will send a DNS query of type A.</div>
                                                    <div>When <code>aaaa</code>, specifies that the monitor will send a DNS query of type AAAA.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>receive</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the IP address that the monitor uses from the resource record sections of the DNS response.</div>
                                                    <div>The IP address should be specified in the dotted-decimal notation or IPv6 notation.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>reverse</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the monitor operates in reverse mode.</div>
                                                    <div>When the monitor is in reverse mode, a successful receive string match marks the monitored object down instead of up. You can use the this mode only if you configure the <code>receive</code> option.</div>
                                                    <div>This parameter is not compatible with the <code>time_until_up</code> parameter. If <code>time_until_up</code> is specified, it must be <code>0</code>. Or, if it already exists, it must be <code>0</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>sampling_timespan</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the length, in seconds, of the probe history window that the system uses to calculate the mean latency and standard deviation of a monitor probe.</div>
                                                    <div>While this value can be configured when <code>adaptive</code> is <code>no</code>, it will not take effect on the system until <code>adaptive</code> is <code>yes</code>.</div>
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
                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>absent</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>present</code>, ensures that the monitor exists.</div>
                                                    <div>When <code>absent</code>, ensures the monitor is removed.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>time_until_up</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the amount of time in seconds after the first successful response before a node will be marked up.</div>
                                                    <div>A value of 0 will cause a node to be marked up immediately after a valid response is received from the node.</div>
                                                    <div>If this parameter is not provided when creating a new monitor, then the default value will be <code>0</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>timeout</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The number of seconds in which the node or service must respond to the monitor request.</div>
                                                    <div>If the target responds within the set time period, it is considered up.</div>
                                                    <div>If the target does not respond within the set time period, it is considered down.</div>
                                                    <div>You can change this number to any number you want, however, it should be 3 times the interval number of seconds plus 1 second.</div>
                                                    <div>If this parameter is not provided when creating a new monitor, then the default value will be <code>16</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>transparent</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies whether the monitor operates in transparent mode.</div>
                                                    <div>Monitors in transparent mode can monitor pool members through firewalls.</div>
                                                    <div>When creating a new monitor, if this parameter is not provided, then the default value will be <code>no</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>up_interval</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the interval for the system to use to perform the health check when a resource is up.</div>
                                                    <div>When <code>0</code>, specifies that the system uses the interval specified in <code>interval</code> to check the health of the resource.</div>
                                                    <div>When any other number, enables specification of a different interval to use when checking the health of a resource that is up.</div>
                                                    <div>When creating a new monitor, if this parameter is not provided, the default <code>0</code> will be used.</div>
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

    
    - name: Create a DNS monitor
      bigip_monitor_dns:
        name: DNS-UDP-V6
        interval: 2
        query_name: localhost
        query_type: aaaa
        up_interval: 5
        adaptive: no
        password: secret
        server: lb.mydomain.com
        state: present
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
                    <b>accept_rcode</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>RCODE required in the response for an up status.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">no-error</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>adaptive</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Whether adaptive is enabled or not.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>adaptive_limit</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Absolute number of milliseconds that may not be exceeded by a monitor probe.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">200</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>allowed_divergence_type</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Type of divergence used for adaptive response time monitoring.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">absolute</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>allowed_divergence_value</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                                                        <div>Value of the type of divergence used for adaptive response time monitoring.</div>
                                                    <div>May be <code>percent</code> or <code>ms</code> depending on whether <code>relative</code> or <code>absolute</code>.</div>
                                                                <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">25</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>answer_section_contains</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Type of DNS query that the monitor sends.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">query-type</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>description</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The description of the monitor.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Important Monitor</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>interval</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new interval in which to run the monitor check.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>ip</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new IP of IP/port definition.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">10.12.13.14</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>manual_resume</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                                                        <div>Whether the system automatically changes the status of a resource to enabled at the next successful monitor check.</div>
                                                                <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">query-type</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>parent</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>New parent template of the monitor.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">http</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>port</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                                                        <div>Alias port or service for the monitor to check, on behalf of the pools or pool members with which the monitor is associated.</div>
                                                                <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">80</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>query_name</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Query name for the monitor to use in a DNS query.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">foo</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>query_type</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Type of DNS query that the monitor sends. Either <code>a</code> or <code>aaaa</code>.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">aaaa</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>receive</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>IP address that the monitor uses from the resource record sections of the DNS response.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2.3.2.4</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>reverse</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Whether the monitor operates in reverse mode.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>sampling_timespan</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Absolute number of milliseconds that may not be exceeded by a monitor probe.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">200</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>time_until_up</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new time in which to mark a system as up after first successful response.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">2</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>timeout</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new timeout in which the remote system must respond to the monitor.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">10</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>transparent</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Whether the monitor operates in transparent mode.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>up_interval</b>
                    <br/><div style="font-size: small; color: red">int</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Interval for the system to use to perform the health check when a resource is up.</div>
                                        <br/>
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
- Wojciech Wypior (@wojtek0806)

