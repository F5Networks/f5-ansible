:source: bigip_gtm_pool.py

:orphan:

.. _bigip_gtm_pool_module:


bigip_gtm_pool - Manages F5 BIG-IP GTM pools
++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manages F5 BIG-IP GTM pools.



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
                    <b>alternate_lb_method</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>round-robin</li>
                                                                                                                                                                                                <li>return-to-dns</li>
                                                                                                                                                                                                <li>none</li>
                                                                                                                                                                                                <li>ratio</li>
                                                                                                                                                                                                <li>topology</li>
                                                                                                                                                                                                <li>static-persistence</li>
                                                                                                                                                                                                <li>global-availability</li>
                                                                                                                                                                                                <li>virtual-server-capacity</li>
                                                                                                                                                                                                <li>packet-rate</li>
                                                                                                                                                                                                <li>drop-packet</li>
                                                                                                                                                                                                <li>fallback-ip</li>
                                                                                                                                                                                                <li>virtual-server-score</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The load balancing mode that the system tries if the <code>preferred_lb_method</code> is unsuccessful in picking a pool.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>availability_requirements</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
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
                    <b>fallback_ip</b>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Specifies the IPv4, or IPv6 address of the server to which the system directs requests when it cannot use one of its pools to do so. Note that the system uses the fallback IP only if you select the <code>fallback_ip</code> load balancing method.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>fallback_lb_method</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>round-robin</li>
                                                                                                                                                                                                <li>return-to-dns</li>
                                                                                                                                                                                                <li>ratio</li>
                                                                                                                                                                                                <li>topology</li>
                                                                                                                                                                                                <li>static-persistence</li>
                                                                                                                                                                                                <li>global-availability</li>
                                                                                                                                                                                                <li>virtual-server-capacity</li>
                                                                                                                                                                                                <li>least-connections</li>
                                                                                                                                                                                                <li>lowest-round-trip-time</li>
                                                                                                                                                                                                <li>fewest-hops</li>
                                                                                                                                                                                                <li>packet-rate</li>
                                                                                                                                                                                                <li>cpu</li>
                                                                                                                                                                                                <li>completion-rate</li>
                                                                                                                                                                                                <li>quality-of-service</li>
                                                                                                                                                                                                <li>kilobytes-per-second</li>
                                                                                                                                                                                                <li>drop-packet</li>
                                                                                                                                                                                                <li>fallback-ip</li>
                                                                                                                                                                                                <li>virtual-server-score</li>
                                                                                                                                                                                                <li>none</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The load balancing mode that the system tries if both the <code>preferred_lb_method</code> and <code>alternate_lb_method</code>s are unsuccessful in picking a pool.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>members</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Members to assign to the pool.</div>
                                                    <div>The order of the members in this list is the order that they will be listed in the pool.</div>
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
                                                                        <div>Name of the server which the pool member is a part of.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <b>virtual_server</b>
                    <br/><div style="font-size: small; color: red">required</div>                                    </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                                                        <div>Name of the virtual server, associated with the server, that the pool member is a part of.</div>
                                                                                </td>
            </tr>
                    
                                                <tr>
                                                                <td colspan="2">
                    <b>monitors</b>
                                        <br/><div style="font-size: small; color: darkgreen">(added in 2.6)</div>                </td>
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
                                                                        <div>Name of the GTM pool.</div>
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
                    <b>preferred_lb_method</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>round-robin</li>
                                                                                                                                                                                                <li>return-to-dns</li>
                                                                                                                                                                                                <li>ratio</li>
                                                                                                                                                                                                <li>topology</li>
                                                                                                                                                                                                <li>static-persistence</li>
                                                                                                                                                                                                <li>global-availability</li>
                                                                                                                                                                                                <li>virtual-server-capacity</li>
                                                                                                                                                                                                <li>least-connections</li>
                                                                                                                                                                                                <li>lowest-round-trip-time</li>
                                                                                                                                                                                                <li>fewest-hops</li>
                                                                                                                                                                                                <li>packet-rate</li>
                                                                                                                                                                                                <li>cpu</li>
                                                                                                                                                                                                <li>completion-rate</li>
                                                                                                                                                                                                <li>quality-of-service</li>
                                                                                                                                                                                                <li>kilobytes-per-second</li>
                                                                                                                                                                                                <li>drop-packet</li>
                                                                                                                                                                                                <li>fallback-ip</li>
                                                                                                                                                                                                <li>virtual-server-score</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The load balancing mode that the system tries first.</div>
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
                                                                                                                                                                <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                <li>absent</li>
                                                                                                                                                                                                <li>enabled</li>
                                                                                                                                                                                                <li>disabled</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>Pool state. When <code>present</code>, ensures that the pool is created and enabled. When <code>absent</code>, ensures that the pool is removed from the system. When <code>enabled</code> or <code>disabled</code>, ensures that the pool is enabled or disabled (respectively) on the remote device.</div>
                                                                                </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <b>type</b>
                                                        </td>
                                <td>
                                                                                                                            <ul><b>Choices:</b>
                                                                                                                                                                <li>a</li>
                                                                                                                                                                                                <li>aaaa</li>
                                                                                                                                                                                                <li>cname</li>
                                                                                                                                                                                                <li>mx</li>
                                                                                                                                                                                                <li>naptr</li>
                                                                                                                                                                                                <li>srv</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                                                        <div>The type of GTM pool that you want to create. On BIG-IP releases prior to version 12, this parameter is not required. On later versions of BIG-IP, this is a required parameter.</div>
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

    
    - name: Create a GTM pool
      bigip_gtm_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        name: my_pool
      delegate_to: localhost

    - name: Disable pool
      bigip_gtm_pool:
        server: lb.mydomain.com
        user: admin
        password: secret
        state: disabled
        name: my_pool
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
                    <b>alternate_lb_method</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>New alternate load balancing method for the pool.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">drop-packet</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>fallback_ip</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>New fallback IP used when load balacing using the <code>fallback_ip</code> method.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">10.10.10.10</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>fallback_lb_method</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>New fallback load balancing method for the pool.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">fewest-hops</div>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <b>members</b>
                    <br/><div style="font-size: small; color: red">complex</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>List of members in the pool.</div>
                                        <br/>
                                    </td>
            </tr>
                                                            <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>server</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The name of the server portion of the member.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <b>virtual_server</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>The name of the virtual server portion of the member.</div>
                                        <br/>
                                    </td>
            </tr>
                    
                                                <tr>
                                <td colspan="2">
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
                                <td colspan="2">
                    <b>preferred_lb_method</b>
                    <br/><div style="font-size: small; color: red">string</div>
                </td>
                <td>changed</td>
                <td>
                                            <div>New preferred load balancing method for the pool.</div>
                                        <br/>
                                            <div style="font-size: smaller"><b>Sample:</b></div>
                                                <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">topology</div>
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

