.. _bigip_gtm_pool:


bigip_gtm_pool - Manages F5 BIG-IP GTM pools
++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages F5 BIG-IP GTM pools.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.9
  * netaddr


Options
-------

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                <tr><td>alternate_lb_method<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>round-robin</li><li>return-to-dns</li><li>none</li><li>ratio</li><li>topology</li><li>static-persistence</li><li>global-availability</li><li>virtual-server-capacity</li><li>packet-rate</li><li>drop-packet</li><li>fallback-ip</li><li>virtual-server-score</li></ul></td>
        <td><div>The load balancing mode that the system tries if the <code>preferred_lb_method</code> is unsuccessful in picking a pool.</div>        </td></tr>
                <tr><td rowspan="2">availability_requirements<br/><div style="font-size: small;"> (added in 2.6)</div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>Specifies, if you activate more than one health monitor, the number of health monitors that must receive successful responses in order for the link to be considered available.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object availability_requirements</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>type<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td><ul><li>all</li><li>at_least</li><li>require</li></ul></td>
                <td><div>Monitor rule type when <code>monitors</code> is specified.</div><div>When creating a new pool, if this value is not specified, the default of &#x27;all&#x27; will be used.</div>        </td></tr>
                    <tr><td>at_least<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the minimum number of active health monitors that must be successful before the link is considered up.</div><div>This parameter is only relevant when a <code>type</code> of <code>at_least</code> is used.</div><div>This parameter will be ignored if a type of either <code>all</code> or <code>require</code> is used.</div>        </td></tr>
                    <tr><td>number_of_probes<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the minimum number of probes that must succeed for this server to be declared up.</div><div>When creating a new virtual server, if this parameter is specified, then the <code>number_of_probers</code> parameter must also be specified.</div><div>The value of this parameter should always be <b>lower</b> than, or <b>equal to</b>, the value of <code>number_of_probers</code>.</div><div>This parameter is only relevant when a <code>type</code> of <code>require</code> is used.</div><div>This parameter will be ignored if a type of either <code>all</code> or <code>at_least</code> is used.</div>        </td></tr>
                    <tr><td>number_of_probers<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the number of probers that should be used when running probes.</div><div>When creating a new virtual server, if this parameter is specified, then the <code>number_of_probes</code> parameter must also be specified.</div><div>The value of this parameter should always be <b>higher</b> than, or <b>equal to</b>, the value of <code>number_of_probers</code>.</div><div>This parameter is only relevant when a <code>type</code> of <code>require</code> is used.</div><div>This parameter will be ignored if a type of either <code>all</code> or <code>at_least</code> is used.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td>fallback_ip<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the IPv4, or IPv6 address of the server to which the system directs requests when it cannot use one of its pools to do so. Note that the system uses the fallback IP only if you select the <code>fallback_ip</code> load balancing method.</div>        </td></tr>
                <tr><td>fallback_lb_method<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>round-robin</li><li>return-to-dns</li><li>ratio</li><li>topology</li><li>static-persistence</li><li>global-availability</li><li>virtual-server-capacity</li><li>least-connections</li><li>lowest-round-trip-time</li><li>fewest-hops</li><li>packet-rate</li><li>cpu</li><li>completion-rate</li><li>quality-of-service</li><li>kilobytes-per-second</li><li>drop-packet</li><li>fallback-ip</li><li>virtual-server-score</li></ul></td>
        <td><div>The load balancing mode that the system tries if both the <code>preferred_lb_method</code> and <code>alternate_lb_method</code>s are unsuccessful in picking a pool.</div>        </td></tr>
                <tr><td rowspan="2">members<br/><div style="font-size: small;"> (added in 2.6)</div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>Members to assign to the pool.</div><div>The order of the members in this list is the order that they will be listed in the pool.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object members</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>server<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>Name of the server which the pool member is a part of.</div>        </td></tr>
                    <tr><td>virtual_server<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>Name of the virtual server, associated with the server, that the pool member is a part of.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td>monitors<br/><div style="font-size: small;"> (added in 2.6)</div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the health monitors that the system currently uses to monitor this resource.</div><div>When <code>availability_requirements.type</code> is <code>require</code>, you may only have a single monitor in the <code>monitors</code> list.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Name of the GTM pool.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Device partition to manage resources on.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div></br>
    <div style="font-size: small;">aliases: pass, pwd<div>        </td></tr>
                <tr><td>preferred_lb_method<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>round-robin</li><li>return-to-dns</li><li>ratio</li><li>topology</li><li>static-persistence</li><li>global-availability</li><li>virtual-server-capacity</li><li>least-connections</li><li>lowest-round-trip-time</li><li>fewest-hops</li><li>packet-rate</li><li>cpu</li><li>completion-rate</li><li>quality-of-service</li><li>kilobytes-per-second</li><li>drop-packet</li><li>fallback-ip</li><li>virtual-server-score</li></ul></td>
        <td><div>The load balancing mode that the system tries first.</div>        </td></tr>
                <tr><td rowspan="2">provider<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>A dict object containing connection details.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object provider</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>password<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                    <tr><td>server<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                    <tr><td>server_port<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>443</td>
                <td></td>
                <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                    <tr><td>user<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                    <tr><td>validate_certs<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>yes</td>
                <td><ul><li>yes</li><li>no</li></ul></td>
                <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
                    <tr><td>timeout<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>10</td>
                <td></td>
                <td><div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>        </td></tr>
                    <tr><td>ssh_keyfile<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>        </td></tr>
                    <tr><td>transport<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td>cli</td>
                <td><ul><li>rest</li><li>cli</li></ul></td>
                <td><div>Configures the transport connection to use when connecting to the remote device.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                <tr><td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>present</li><li>absent</li><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Pool state. When <code>present</code>, ensures that the pool is created and enabled. When <code>absent</code>, ensures that the pool is removed from the system. When <code>enabled</code> or <code>disabled</code>, ensures that the pool is enabled or disabled (respectively) on the remote device.</div>        </td></tr>
                <tr><td>type<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>a</li><li>aaaa</li><li>cname</li><li>mx</li><li>naptr</li><li>srv</li></ul></td>
        <td><div>The type of GTM pool that you want to create. On BIG-IP releases prior to version 12, this parameter is not required. On later versions of BIG-IP, this is a required parameter.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>yes</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
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

Common return values are `documented here <http://docs.ansible.com/ansible/latest/common_return_values.html>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=1 cellpadding=4>
    <tr>
    <th class="head">name</th>
    <th class="head">description</th>
    <th class="head">returned</th>
    <th class="head">type</th>
    <th class="head">sample</th>
    </tr>

        <tr>
        <td> preferred_lb_method </td>
        <td> New preferred load balancing method for the pool. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> topology </td>
    </tr>
            <tr>
        <td> alternate_lb_method </td>
        <td> New alternate load balancing method for the pool. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> drop-packet </td>
    </tr>
            <tr>
        <td> fallback_lb_method </td>
        <td> New fallback load balancing method for the pool. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> fewest-hops </td>
    </tr>
            <tr>
        <td> fallback_ip </td>
        <td> New fallback IP used when load balacing using the C(fallback_ip) method. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 10.10.10.10 </td>
    </tr>
            <tr>
        <td> monitors </td>
        <td> The new list of monitors for the resource. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['/Common/monitor1', '/Common/monitor2'] </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the netaddr Python package on the host. This is as easy as pip install netaddr.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/integrations/networks/f5.
    - Requires the f5-sdk Python package on the host. This is as easy as ``pip install f5-sdk``.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.