.. _bigip_gtm_facts:


bigip_gtm_facts - Collect facts from F5 BIG-IP GTM devices
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Collect facts from F5 BIG-IP GTM devices.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 3.0.9


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
                <tr><td>filter<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Perform regex filter of response. Filtering is done on the name of the resource. Valid filters are anything that can be provided to Python&#x27;s <code>re</code> module.</div>        </td></tr>
                <tr><td>include<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul><li>pool</li><li>wide_ip</li><li>server</li></ul></td>
        <td><div>Fact category to collect.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div></br>
    <div style="font-size: small;">aliases: pass, pwd<div>        </td></tr>
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
                    <tr><td>ssh_keyfile<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Specifies the SSH keyfile to use to authenticate the connection to the remote device.  This argument is only used for <em>cli</em> transports. If the value is not specified in the task, the value of environment variable <code>ANSIBLE_NET_SSH_KEYFILE</code> will be used instead.</div>        </td></tr>
                    <tr><td>timeout<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>10</td>
                <td></td>
                <td><div>Specifies the timeout in seconds for communicating with the network device for either connecting or sending commands.  If the timeout is exceeded before the operation is completed, the module will error.</div>        </td></tr>
                    <tr><td>server<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The BIG-IP host. You can omit this option if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                    <tr><td>user<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                    <tr><td>server_port<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>443</td>
                <td></td>
                <td><div>The BIG-IP server port. You can omit this option if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                    <tr><td>password<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td></td>
                <td><div>The password for the user account used to connect to the BIG-IP. You can omit this option if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                    <tr><td>validate_certs<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td>True</td>
                <td><ul><li>yes</li><li>no</li></ul></td>
                <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
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
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. You can omit this option if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>yes</li><li>no</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. Use this only on personally controlled sites using self-signed certificates. You can omit this option if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
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
        <td> wide_ip </td>
        <td> Contains the lb method for the wide ip and the pools that are within the wide ip. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> {'wide_ip': [{'pool_lb_mode': 'round-robin', 'last_resort_pool': '', 'persist_cidr_ipv4': 32, 'persist_cidr_ipv6': 128, 'name': 'foo.ok.com', 'failure_rcode_response': 'disabled', 'failure_rcode': 'noerror', 'partition': 'Common', 'enabled': True, 'failure_rcode_ttl': 0, 'ttl_persistence': 3600, 'full_path': '/Common/foo.ok.com', 'pools': [{'partition': 'Common', 'ratio': 1, 'name': 'd3qw', 'order': 0}], 'minimal_response': 'enabled', 'type': 'naptr', 'persistence': 'disabled'}]} </td>
    </tr>
            <tr>
        <td> pool </td>
        <td> Contains the pool object status and enabled status. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> {'pool': [{'verify_member_availability': 'disabled', 'partition': 'Common', 'qos_packet_rate': 1, 'qos_hit_ratio': 5, 'alternate_mode': 'round-robin', 'members': [{'ratio': 1, 'name': 'ok3.com', 'service': 80, 'member_order': 0, 'disabled': True, 'flags': 'a', 'preference': 10, 'order': 10, 'full_path': 'ok3.com'}], 'ttl': 30, 'enabled_state': 'disabled', 'qos_vs_score': 0, 'qos_topology': 0, 'load_balancing_mode': 'round-robin', 'max_answers_returned': 1, 'fallback_mode': 'return-to-dns', 'qos_rtt': 50, 'name': 'd3qw', 'qos_hops': 0, 'qos_kilobytes_second': 3, 'qos_lcs': 30, 'enabled': True, 'qos_vs_capacity': 0, 'availability_state': 'offline', 'manual_resume': 'disabled', 'full_path': '/Common/d3qw', 'type': 'naptr', 'dynamic_ratio': 'disabled'}]} </td>
    </tr>
            <tr>
        <td> server </td>
        <td> Contains the virtual server enabled and availability status, and address. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> {'server': [{'product': 'single-bigip', 'virtual_servers': [{'limit_max_pps_status': 'disabled', 'name': 'jsdfhsd', 'destination': '10.10.10.10:0', 'enabled': True, 'translation_address': 'none', 'limit_max_pps': 0, 'limit_max_bps': 0, 'limit_max_bps_status': 'disabled', 'limit_max_connections': 0, 'limit_max_connections_status': 'disabled', 'full_path': 'jsdfhsd', 'translation_port': 0}], 'addresses': [{'translation': 'none', 'name': '10.10.10.10', 'device_name': '/Common/qweqwe'}], 'datacenter': '/Common/xfxgh', 'limit_cpu_usage': 0, 'expose_route_domains': False, 'virtual_server_discovery': 'disabled', 'iq_allow_snmp': True, 'iq_allow_service_check': True, 'limit_max_bps_status': 'disabled', 'limit_max_connections': 0, 'limit_cpu_usage_status': 'disabled', 'limit_max_pps_status': 'disabled', 'link_discovery': 'disabled', 'iq_allow_path': True, 'monitor': '/Common/bigip', 'limit_mem_avail_status': 'disabled', 'limit_mem_avail': 0, 'partition': 'Common', 'enabled': True, 'name': 'qweqwe', 'limit_max_pps': 0, 'limit_max_bps': 0, 'limit_max_connections_status': 'disabled', 'full_path': '/Common/qweqwe'}]} </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
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