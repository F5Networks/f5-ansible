:source: bigip_security_log_profile.py

:orphan:

.. _bigip_security_log_profile_module:


bigip_security_log_profile - Manage logging profiles on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.6

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manages logging profiles configured in the system along with basic information about each profile.



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- f5-sdk >= 3.0.9


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
                                                                                                                                                    
                                                                                                                                                                
                                                                                                                                                                                                                                                                                            
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                    <tr>
            <th colspan="3">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="3">
                    <b>description</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Description of the log profile.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="3">
                    <b>dos_protection</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Configures DoS related settings of the log profile.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="2">
                    <b>dns_publisher</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the log publisher used for DNS DoS events.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="3">
                    <b>ip_intelligence</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Configures IP Intelligence related settings of the log profile.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="2">
                    <b>publisher</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the log publisher used for IP Intelligence events.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
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
                                                                        <div>This option is used to enable or disable the logging of translated (i.e server side) fields in IP Intelligence log messages.</div>
                                                    <div>Translated fields include (but are not limited to) source address/port, destination address/port, IP protocol, route domain, and VLAN.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="3">
                    <b>name</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the log profile.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="3">
                    <b>network_firewall</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Configures Network Firewall related settings of the log profile.</div>
                                                                                </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="2">
                    <b>publisher</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the name of the log publisher used for Network events.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="2">
                    <b>log_matches_accept_rule</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                                                    </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
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
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="2">
                    <b>log_matches_drop_rule</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                                                    </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
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
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="2">
                    <b>log_matches_reject_rule</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                                                    </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
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
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="2">
                    <b>log_ip_errors</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                                                    </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
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
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="2">
                    <b>log_tcp_errors</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                                                    </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
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
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="2">
                    <b>log_tcp_events</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                                                    </td>
            </tr>
                                                            <tr>
                                                    <td class="elbow-placeholder"></td>
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
                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>rate_limit</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>This option is used to set rate limits for the logging of TCP events on client side.</div>
                                                    <div>This option is effective only if logging of this message type is enabled.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                    <td class="elbow-placeholder"></td>
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
                                                    <td class="elbow-placeholder"></td>
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
                                                    <div>When <code>field-list</code>, specifies that the log displays only the items you specify in the <code>fields</code> list with <code>delimiter</code> as the delimiter between the items.</div>
                                                    <div>When <code>none</code>, the messages will be logged in the default format, which is <code>&quot;management_ip_address&quot;,&quot;bigip_hostname&quot;,&quot;context_type&quot;, &quot;context_name&quot;,&quot;src_geo&quot;,&quot;src_ip&quot;, &quot;dest_geo&quot;,&quot;dest_ip&quot;,&quot;src_port&quot;, &quot;dest_port&quot;,&quot;vlan&quot;,&quot;protocol&quot;,&quot;route_domain&quot;, &quot;translated_src_ip&quot;, &quot;translated_dest_ip&quot;,&quot;translated_src_port&quot;,&quot;translated_dest_port&quot;, &quot;translated_vlan&quot;,&quot;translated_ip_protocol&quot;,&quot;translated_route_domain&quot;, &quot;acl_policy_type&quot;, &quot;acl_policy_name&quot;,&quot;acl_rule_name&quot;,&quot;action&quot;, &quot;drop_reason&quot;,&quot;sa_translation_type&quot;, &quot;sa_translation_pool&quot;,&quot;flow_id&quot;, &quot;source_user&quot;,&quot;source_fqdn&quot;,&quot;dest_fqdn&quot;</code>.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="2">
                    <b>log_format_delimiter</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the delimiter string when using a <code>type</code> of <code>field-list</code>.</div>
                                                    <div>When creating a new profile, if this parameter is not specified, the default value of <code>,</code> (the comma character) will be used.</div>
                                                    <div>This option is valid when the <code>type</code> is set to <code>field-list</code>. It will be ignored otherwise.</div>
                                                    <div>Depending on the delimiter used, it may be necessary to wrap the delimiter in quotes to prevent YAML errors from occurring.</div>
                                                    <div>The special character <code>$</code> should not be used, and will raise an error if used, as it is reserved for internal use.</div>
                                                    <div>The maximum length allowed for this parameter is <code>31</code> characters.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
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
                                                    <div>This option is valid when the <code>type</code> is set to <code>field-list</code>. It will be ignored otherwise.</div>
                                                    <div>The order of the list is important as the server displays the selected traffic items in the log sequentially according to it.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="3">
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
                                                                <td colspan="3">
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
                                                                <td colspan="3">
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
                                                    <td class="elbow-placeholder"></td>
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
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="2">
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
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="2">
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
                                                <td colspan="2">
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
                                                <td colspan="2">
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
                                                <td colspan="2">
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
                                                                <td colspan="3">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="3">
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
                                                                <td colspan="3">
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
                                                    <div>When <code>absent</code>, ensures that the resource does not exist.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="3">
                    <b>user</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="3">
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

    
    - name: Create a security profile stub
      bigip_security_log_profile:
        name: policy1
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
      delegate_to: localhost

    - name: Create/modify multiple log profiles with similar settings
      bigip_security_log_profile:
        name: "{{ item.name }}"
        description: "{{ item.description|default(omit) }}"
        network_firewall:
           publisher: "{{ item.publisher }}"
           log_matches_accept_rule:
              enabled: yes
              rate_limit: 100
           log_matches_drop_rule:
              enabled: yes
              rate_limit: 200
           log_matches_reject_rule:
              enabled: yes
           log_ip_errors:
              enabled: yes
              rate_limit: 400
           log_tcp_errors:
              enabled: yes
           log_tcp_events:
              enabled: yes
           log_translation_fields: yes
           storage_format:
              type: field-list
              delimiter: ","
              fields: "{{ field_list_1 }}"
        dos_protection:
           dns_publisher: "{{ item.publisher }}"
        ip_intelligence:
           publisher: "{{ item.publisher }}"
           log_translation_fields: yes




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
                    <b>param1</b>
                    <br/><div style="font-size: small; color: red">bool</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new param1 value of the resource.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">True</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>param2</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The new param2 value of the resource.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">Foo is bar</div>
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

