:source: bigip_firewall_log_profile_network.py

:orphan:

.. _bigip_firewall_log_profile_network_module:


bigip_firewall_log_profile_network - Configures Network Firewall related settings of the log profile
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.9

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Configures Network Firewall related settings of the log profile.




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
                    <b>log_format_delimiter</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the delimiter string when using a <code>log_storage_format</code> of <code>field-list</code>.</div>
                                                    <div>When creating a new profile, if this parameter is not specified, the default value of <code>,</code> (the comma character) will be used.</div>
                                                    <div>This option is valid when the <code>log_storage_format</code> is set to <code>field-list</code>. It will be ignored otherwise.</div>
                                                    <div>Depending on the delimiter used, it may be necessary to wrap the delimiter in quotes to prevent YAML errors from occurring.</div>
                                                    <div>The special character <code>$</code> should not be used, and will raise an error if used, as it is reserved for internal use.</div>
                                                    <div>The maximum length allowed for this parameter is <code>31</code> characters.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>log_ip_errors</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Modify log settings for logging of IP error packets.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>enabled</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to enable or disable the logging of IP error packets.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>rate_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to set rate limits for the logging of IP error packets.</div>
                                                    <div>This option is effective only if logging of this message type is enabled.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>log_matches_accept_rule</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Modify log settings for ACL rules configured with an &quot;accept&quot; or &quot;accept decisively&quot; action.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>enabled</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to enable or disable the logging of packets that match ACL rules configured with an &quot;accept&quot; or &quot;accept decisively&quot; action.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>rate_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to set rate limits for the logging of packets that match ACL rules configured with an &quot;accept&quot; or &quot;accept decisively&quot; action.</div>
                                                    <div>This option is effective only if logging of this message type is enabled.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>log_matches_drop_rule</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Modify log settings for ACL rules configured with a drop action.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>enabled</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to enable or disable the logging of packets that match ACL rules configured with a drop action.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>rate_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to set rate limits for the logging of packets that match ACL rules configured with a drop action.</div>
                                                    <div>This option is effective only if logging of this message type is enabled.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>log_matches_reject_rule</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Modify log settings for ACL rules configured with a reject action.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>enabled</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to enable or disable the logging of packets that match ACL rules configured with a reject action.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>rate_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to set rate limits for the logging of packets that match ACL rules configured with a reject action.</div>
                                                    <div>This option is effective only if logging of this message type is enabled.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>log_message_fields</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>acl_policy_name</li>
                                                                                                                                                                                                <li>acl_policy_type</li>
                                                                                                                                                                                                <li>acl_rule_name</li>
                                                                                                                                                                                                <li>action</li>
                                                                                                                                                                                                <li>bigip_hostname</li>
                                                                                                                                                                                                <li>context_name</li>
                                                                                                                                                                                                <li>context_type</li>
                                                                                                                                                                                                <li>date_time</li>
                                                                                                                                                                                                <li>dest_fqdn</li>
                                                                                                                                                                                                <li>dest_geo</li>
                                                                                                                                                                                                <li>dest_ip</li>
                                                                                                                                                                                                <li>dest_port</li>
                                                                                                                                                                                                <li>drop_reason</li>
                                                                                                                                                                                                <li>management_ip_address</li>
                                                                                                                                                                                                <li>protocol</li>
                                                                                                                                                                                                <li>route_domain</li>
                                                                                                                                                                                                <li>sa_translation_pool</li>
                                                                                                                                                                                                <li>sa_translation_type</li>
                                                                                                                                                                                                <li>source_fqdn</li>
                                                                                                                                                                                                <li>source_user</li>
                                                                                                                                                                                                <li>src_geo</li>
                                                                                                                                                                                                <li>src_ip</li>
                                                                                                                                                                                                <li>src_port</li>
                                                                                                                                                                                                <li>translated_dest_ip</li>
                                                                                                                                                                                                <li>translated_dest_port</li>
                                                                                                                                                                                                <li>translated_ip_protocol</li>
                                                                                                                                                                                                <li>translated_route_domain</li>
                                                                                                                                                                                                <li>translated_src_ip</li>
                                                                                                                                                                                                <li>translated_src_port</li>
                                                                                                                                                                                                <li>translated_vlan</li>
                                                                                                                                                                                                <li>vlan</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies a set of fields to be logged.</div>
                                                    <div>This option is valid when the <code>log_storage_format</code> is set to <code>field-list</code>. It will be ignored otherwise.</div>
                                                    <div>The order of the list is important as the server displays the selected traffic items in the log sequentially according to it.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>log_publisher</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the log publisher used for Network events.</div>
                                                    <div>To specify the log_publisher on a different partition from the AFM log profile, specify the name in fullpath format, e.g. <code>/Foobar/log-publisher</code>, otherwise the partition for log publisher is inferred from <code>partition</code> module parameter.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>log_storage_format</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>field-list</li>
                                                                                                                                                                                                <li>none</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the type of the storage format.</div>
                                                    <div>When creating a new log profile, if this parameter is not specified, the default is <code>none</code>.</div>
                                                    <div>When <code>field-list</code>, specifies that the log displays only the items you specify in the <code>log_message_fields</code> list with <code>log_format_delimiter</code> as the delimiter between the items.</div>
                                                    <div>When <code>none</code>, the messages will be logged in the default format, which is <code>&quot;management_ip_address&quot;, &quot;bigip_hostname&quot;,&quot;context_type&quot;, &quot;context_name&quot;,&quot;src_geo&quot;,&quot;src_ip&quot;, &quot;dest_geo&quot;,&quot;dest_ip&quot;,&quot;src_port&quot;, &quot;dest_port&quot;,&quot;vlan&quot;,&quot;protocol&quot;,&quot;route_domain&quot;, &quot;translated_src_ip&quot;, &quot;translated_dest_ip&quot;, &quot;translated_src_port&quot;,&quot;translated_dest_port&quot;, &quot;translated_vlan&quot;,&quot;translated_ip_protocol&quot;, &quot;translated_route_domain&quot;, &quot;acl_policy_type&quot;, &quot;acl_policy_name&quot;,&quot;acl_rule_name&quot;,&quot;action&quot;, &quot;drop_reason&quot;,&quot;sa_translation_type&quot;, &quot;sa_translation_pool&quot;,&quot;flow_id&quot;, &quot;source_user&quot;, &quot;source_fqdn&quot;,&quot;dest_fqdn&quot;</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>log_tcp_errors</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Modify log settings for logging of TCP error packets.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>enabled</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to enable or disable the logging of TCP error packets.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>rate_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to set rate limits for the logging of TCP error packets.</div>
                                                    <div>This option is effective only if logging of this message type is enabled.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>log_tcp_events</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Modify log settings for logging of TCP events on the client side.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>enabled</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to enable or disable the logging of TCP events on the client side.</div>
                                                    <div>Only &#x27;Established&#x27; and &#x27;Closed&#x27; states of a TCP session are logged if this option is enabled.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>rate_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to set rate limits for the logging of TCP events on the client side.</div>
                                                    <div>This option is effective only if logging of this message type is enabled.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>log_translation_fields</b>
                                                        </td>
                                <td>
                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                <li>no</li>
                                                                                                                                                                                                <li>yes</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to enable or disable the logging of translated (i.e server side) fields in ACL match and TCP events.</div>
                                                    <div>Translated fields include (but are not limited to) source address/port, destination address/port, IP protocol, route domain, and VLAN.</div>
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
                                                                        <div>Device partition to create log profile on.</div>
                                                    <div>Parameter also used when specifying names for log publishers, unless log publisher names are in fullpath format.</div>
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
                    <b>profile_name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the AFM log profile to be updated.</div>
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
                    <b>rate_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Defines a rate limit for all combined network firewall log messages per second. Beyond this rate limit, log messages are not logged.</div>
                                                    <div>To specify an indefinite rate, use the value <code>indefinite</code>.</div>
                                                    <div>If specifying a numeric rate, the value must be between <code>1</code> and <code>4294967295</code>.</div>
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
                    <b>state</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>absent</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>When <code>state</code> is <code>present</code>, ensures the resource exists.</div>
                                                    <div>Only built-in profile that allows updating network log settings is global-network, attempts to do so on other built-in profiles will be ignored.</div>
                                                    <div>When <code>state</code> is <code>absent</code>, ensures that resource is removed.</div>
                                                    <div>The <code>absent</code> state is ignored for global-network log profile.</div>
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

    
    - name: Add network settings to log profile
      bigip_firewall_log_profile_network:
        profile_name: barbaz
        rate_limit: 150000
        log_publisher: local-db-pub
        log_tcp_errors:
          enabled: yes
          rate_limit: 10000
        log_tcp_events:
          enabled: yes
          rate_limit: 40000
        log_storage_format: "field-list"
        log_message_fields:
          - vlan
          - translated_vlan
          - src_ip
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Change delimiter and log fields
      bigip_firewall_log_profile_network:
        profile_name: barbaz
        log_format_delimiter: '.'
        log_message_fields:
          - translated_dest_ip
          - translated_dest_port
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Modify built-in profile
      bigip_firewall_log_profile_network:
        profile_name: "global-network"
        log_publisher: "/foobar/log1"
        log_ip_errors:
          enabled: yes
          rate_limit: 60000
        log_matches_reject_rule:
          enabled: yes
          rate_limit: 2000
        log_translation_fields: yes
        log_storage_format: "field-list"
        log_format_delimiter: '.'
        log_message_fields:
          - protocol
          - dest_ip
          - dest_port
        provider:
          password: secret
          server: lb.mydomain.com
          user: admin
      delegate_to: localhost

    - name: Remove custom log profile network log settings
      bigip_firewall_log_profile_network:
        profile_name: "{{ log_profile }}"
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
            <th colspan="2">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="2">
                    <b>log_format_delimiter</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The delimiter string when using a log_storage_format of field-list.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">.</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>log_ip_errors</b>
                    <br/><div style="font-size: small; color: red">complex</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Log settings for logging of IP error packets.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">hash/dictionary of values</div>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>enabled</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enable or disable the logging of IP error packets.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>rate_limit</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The rate limit for the logging of IP error packets.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">indefinite</div>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>log_matches_accept_rule</b>
                    <br/><div style="font-size: small; color: red">complex</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Log settings for ACL rules configured with an &quot;accept&quot; or &quot;accept decisively&quot; action.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">hash/dictionary of values</div>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>enabled</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enable or disable the logging of packets that match ACL rules.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>rate_limit</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The rate limit for the logging of packets that match ACL rules.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">indefinite</div>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>log_matches_drop_rule</b>
                    <br/><div style="font-size: small; color: red">complex</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Log settings for ACL rules configured with a drop action.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">hash/dictionary of values</div>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>enabled</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enable or disable the logging of packets that match ACL rules.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>rate_limit</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The rate limit for the logging of packets that match ACL rules.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">indefinite</div>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>log_matches_reject_rule</b>
                    <br/><div style="font-size: small; color: red">complex</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Log settings for ACL rules configured with a reject action.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">hash/dictionary of values</div>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>enabled</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enable or disable the logging of packets that match ACL rules.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>rate_limit</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The rate limit for the logging of packets that match ACL rules.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">indefinite</div>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>log_message_fields</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The delimiter string when using a log_storage_format of field-list.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;acl_policy_name&#x27;, &#x27;acl_policy_type&#x27;]</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>log_publisher</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The name of the log publisher used for Network events.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">/Common/log-publisher</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>log_tcp_errors</b>
                    <br/><div style="font-size: small; color: red">complex</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Log settings for logging of TCP error packets.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">hash/dictionary of values</div>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>enabled</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enable or disable the logging of TCP error packets.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>rate_limit</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The rate limit for the logging of TCP error packets.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">indefinite</div>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>log_tcp_events</b>
                    <br/><div style="font-size: small; color: red">complex</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Log settings for logging of TCP events on the client side.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">hash/dictionary of values</div>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>enabled</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Enable or disable the logging of TCP events on the client side.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>rate_limit</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The rate limit for the logging of TCP events on the client side.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">indefinite</div>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
                    <b>log_translation_fields</b>
                    <br/><div style="font-size: small; color: red">str</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The type of the storage format.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">field-list</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>rate_limit</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The rate limit for all combined network firewall log messages per second.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">indefinite</div>
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

