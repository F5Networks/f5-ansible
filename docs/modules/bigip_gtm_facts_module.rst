:source: bigip_gtm_facts.py

:orphan:

.. _bigip_gtm_facts_module:


bigip_gtm_facts - Collect facts from F5 BIG-IP GTM devices
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Collect facts from F5 BIG-IP GTM devices.



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
                    <b>filter</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Perform regex filter of response. Filtering is done on the name of the resource. Valid filters are anything that can be provided to Python&#x27;s <code>re</code> module.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>include</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>pool</li>
                                                                                                                                                                                                <li>wide_ip</li>
                                                                                                                                                                                                <li>server</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Fact category to collect.</div>
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

    
    - name: Get pool facts
      bigip_gtm_facts:
        server: lb.mydomain.com
        user: admin
        password: secret
        include: pool
        filter: my_pool
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
                    <b>pool</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Contains the pool object status and enabled status.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;pool&#x27;: [{&#x27;alternate_mode&#x27;: &#x27;round-robin&#x27;, &#x27;dynamic_ratio&#x27;: &#x27;disabled&#x27;, &#x27;enabled&#x27;: True, &#x27;fallback_mode&#x27;: &#x27;return-to-dns&#x27;, &#x27;full_path&#x27;: &#x27;/Common/d3qw&#x27;, &#x27;load_balancing_mode&#x27;: &#x27;round-robin&#x27;, &#x27;manual_resume&#x27;: &#x27;disabled&#x27;, &#x27;max_answers_returned&#x27;: 1, &#x27;members&#x27;: [{&#x27;disabled&#x27;: True, &#x27;flags&#x27;: &#x27;a&#x27;, &#x27;full_path&#x27;: &#x27;ok3.com&#x27;, &#x27;member_order&#x27;: 0, &#x27;name&#x27;: &#x27;ok3.com&#x27;, &#x27;order&#x27;: 10, &#x27;preference&#x27;: 10, &#x27;ratio&#x27;: 1, &#x27;service&#x27;: 80}], &#x27;name&#x27;: &#x27;d3qw&#x27;, &#x27;partition&#x27;: &#x27;Common&#x27;, &#x27;qos_hit_ratio&#x27;: 5, &#x27;qos_hops&#x27;: 0, &#x27;qos_kilobytes_second&#x27;: 3, &#x27;qos_lcs&#x27;: 30, &#x27;qos_packet_rate&#x27;: 1, &#x27;qos_rtt&#x27;: 50, &#x27;qos_topology&#x27;: 0, &#x27;qos_vs_capacity&#x27;: 0, &#x27;qos_vs_score&#x27;: 0, &#x27;availability_state&#x27;: &#x27;offline&#x27;, &#x27;enabled_state&#x27;: &#x27;disabled&#x27;, &#x27;ttl&#x27;: 30, &#x27;type&#x27;: &#x27;naptr&#x27;, &#x27;verify_member_availability&#x27;: &#x27;disabled&#x27;}]}</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Contains the virtual server enabled and availability status, and address.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;server&#x27;: [{&#x27;addresses&#x27;: [{&#x27;device_name&#x27;: &#x27;/Common/qweqwe&#x27;, &#x27;name&#x27;: &#x27;10.10.10.10&#x27;, &#x27;translation&#x27;: &#x27;none&#x27;}], &#x27;datacenter&#x27;: &#x27;/Common/xfxgh&#x27;, &#x27;enabled&#x27;: True, &#x27;expose_route_domains&#x27;: False, &#x27;full_path&#x27;: &#x27;/Common/qweqwe&#x27;, &#x27;iq_allow_path&#x27;: True, &#x27;iq_allow_service_check&#x27;: True, &#x27;iq_allow_snmp&#x27;: True, &#x27;limit_cpu_usage&#x27;: 0, &#x27;limit_cpu_usage_status&#x27;: &#x27;disabled&#x27;, &#x27;limit_max_bps&#x27;: 0, &#x27;limit_max_bps_status&#x27;: &#x27;disabled&#x27;, &#x27;limit_max_connections&#x27;: 0, &#x27;limit_max_connections_status&#x27;: &#x27;disabled&#x27;, &#x27;limit_max_pps&#x27;: 0, &#x27;limit_max_pps_status&#x27;: &#x27;disabled&#x27;, &#x27;limit_mem_avail&#x27;: 0, &#x27;limit_mem_avail_status&#x27;: &#x27;disabled&#x27;, &#x27;link_discovery&#x27;: &#x27;disabled&#x27;, &#x27;monitor&#x27;: &#x27;/Common/bigip&#x27;, &#x27;name&#x27;: &#x27;qweqwe&#x27;, &#x27;partition&#x27;: &#x27;Common&#x27;, &#x27;product&#x27;: &#x27;single-bigip&#x27;, &#x27;virtual_server_discovery&#x27;: &#x27;disabled&#x27;, &#x27;virtual_servers&#x27;: [{&#x27;destination&#x27;: &#x27;10.10.10.10:0&#x27;, &#x27;enabled&#x27;: True, &#x27;full_path&#x27;: &#x27;jsdfhsd&#x27;, &#x27;limit_max_bps&#x27;: 0, &#x27;limit_max_bps_status&#x27;: &#x27;disabled&#x27;, &#x27;limit_max_connections&#x27;: 0, &#x27;limit_max_connections_status&#x27;: &#x27;disabled&#x27;, &#x27;limit_max_pps&#x27;: 0, &#x27;limit_max_pps_status&#x27;: &#x27;disabled&#x27;, &#x27;name&#x27;: &#x27;jsdfhsd&#x27;, &#x27;translation_address&#x27;: &#x27;none&#x27;, &#x27;translation_port&#x27;: 0}]}]}</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <b>wide_ip</b>
                    <br/><div style="font-size: small; color: red">list</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>Contains the lb method for the wide ip and the pools that are within the wide ip.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;wide_ip&#x27;: [{&#x27;enabled&#x27;: True, &#x27;failure_rcode&#x27;: &#x27;noerror&#x27;, &#x27;failure_rcode_response&#x27;: &#x27;disabled&#x27;, &#x27;failure_rcode_ttl&#x27;: 0, &#x27;full_path&#x27;: &#x27;/Common/foo.ok.com&#x27;, &#x27;last_resort_pool&#x27;: &#x27;&#x27;, &#x27;minimal_response&#x27;: &#x27;enabled&#x27;, &#x27;name&#x27;: &#x27;foo.ok.com&#x27;, &#x27;partition&#x27;: &#x27;Common&#x27;, &#x27;persist_cidr_ipv4&#x27;: 32, &#x27;persist_cidr_ipv6&#x27;: 128, &#x27;persistence&#x27;: &#x27;disabled&#x27;, &#x27;pool_lb_mode&#x27;: &#x27;round-robin&#x27;, &#x27;pools&#x27;: [{&#x27;name&#x27;: &#x27;d3qw&#x27;, &#x27;order&#x27;: 0, &#x27;partition&#x27;: &#x27;Common&#x27;, &#x27;ratio&#x27;: 1}], &#x27;ttl_persistence&#x27;: 3600, &#x27;type&#x27;: &#x27;naptr&#x27;}]}</div>
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

