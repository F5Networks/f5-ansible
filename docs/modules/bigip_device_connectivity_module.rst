.. _bigip_device_connectivity:


bigip_device_connectivity - Manages device IP configuration settings for HA on a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages device IP configuration settings for HA on a BIG-IP. Each BIG-IP device has synchronization and failover connectivity information (IP addresses) that you define as part of HA pairing or clustering. This module allows you to configure that information.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 2.2.3


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
                <tr><td>config_sync_ip<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Local IP address that the system uses for ConfigSync operations.</div>        </td></tr>
                <tr><td>failover_multicast<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>When <code>yes</code>, ensures that the Failover Multicast configuration is enabled and if no further multicast configuration is provided, ensures that <code>multicast_interface</code>, <code>multicast_address</code> and <code>multicast_port</code> are the defaults specified in each option's description. When <code>no</code>, ensures that Failover Multicast configuration is disabled.</div>        </td></tr>
                <tr><td>mirror_primary_address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the primary IP address for the system to use to mirror connections.</div>        </td></tr>
                <tr><td>mirror_secondary_address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the secondary IP address for the system to use to mirror connections.</div>        </td></tr>
                <tr><td>multicast_address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>IP address for the system to send multicast messages associated with failover. When <code>failover_multicast</code> is <code>yes</code> and this option is not provided, a default of <code>224.0.0.245</code> will be used.</div>        </td></tr>
                <tr><td>multicast_interface<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Interface over which the system sends multicast messages associated with failover. When <code>failover_multicast</code> is <code>yes</code> and this option is not provided, a default of <code>eth0</code> will be used.</div>        </td></tr>
                <tr><td>multicast_port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Port for the system to send multicast messages associated with failover. When <code>failover_multicast</code> is <code>yes</code> and this option is not provided, a default of <code>62960</code> will be used. This value must be between 0 and 65535.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The BIG-IP host. This option can be omitted if the environment variable <code>F5_SERVER</code> is set.</div>        </td></tr>
                <tr><td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td></td>
        <td><div>The BIG-IP server port. This option can be omitted if the environment variable <code>F5_SERVER_PORT</code> is set.</div>        </td></tr>
                <tr><td>unicast_failover<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Desired addresses to use for failover operations. Options <code>address</code> and <code>port</code> are supported with dictionary structure where <code>address</code> is the local IP address that the system uses for failover operations. Port specifies the port that the system uses for failover operations. If <code>port</code> is not specified, the default value <code>1026</code> will be used.</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. This option can be omitted if the environment variable <code>F5_USER</code> is set.</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. This option can be omitted if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Configure device connectivity for standard HA pair
      bigip_device_connectivity:
        config_sync_ip: 10.1.30.1
        mirror_primary_address: 10.1.30.1
        unicast_failover:
          - address: 10.1.30.1
        server: lb.mydomain.com
        user: admin
        password: secret
      delegate_to: localhost

Return Values
-------------

Common return values are documented here :doc:`common_return_values`, the following are the fields unique to this module:

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
        <td> multicast_interface </td>
        <td> The new value of the C(multicast_interface) setting. </td>
        <td align=center>  </td>
        <td align=center> string </td>
        <td align=center> eth0 </td>
    </tr>
            <tr>
        <td> changed </td>
        <td> Denotes if the F5 configuration was updated. </td>
        <td align=center> always </td>
        <td align=center> bool </td>
        <td align=center>  </td>
    </tr>
            <tr>
        <td> mirror_primary_address </td>
        <td> The new value of the C(mirror_primary_address) setting. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 10.1.1.2 </td>
    </tr>
            <tr>
        <td> mirror_secondary_address </td>
        <td> The new value of the C(mirror_secondary_address) setting. </td>
        <td align=center>  </td>
        <td align=center> string </td>
        <td align=center> 10.1.1.3 </td>
    </tr>
            <tr>
        <td> config_sync_ip </td>
        <td> The new value of the C(config_sync_ip) setting. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> 10.1.1.1 </td>
    </tr>
            <tr>
        <td> multicast_address </td>
        <td> The new value of the C(multicast_address) setting. </td>
        <td align=center>  </td>
        <td align=center> string </td>
        <td align=center> 224.0.0.245 </td>
    </tr>
            <tr>
        <td> failover_multicast </td>
        <td> Whether a failover multicast attribute has been changed or not. </td>
        <td align=center>  </td>
        <td align=center> bool </td>
        <td align=center>  </td>
    </tr>
            <tr>
        <td> unicast_failover </td>
        <td> The new value of the C(unicast_failover) setting. </td>
        <td align=center>  </td>
        <td align=center> list </td>
        <td align=center> [{'port': 1026, 'address': '10.1.1.2'}] </td>
    </tr>
            <tr>
        <td> multicast_port </td>
        <td> The new value of the C(multicast_port) setting. </td>
        <td align=center>  </td>
        <td align=center> string </td>
        <td align=center> 1026 </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - This module is primarily used as a component of configuring HA pairs of BIG-IP devices.
    - Requires BIG-IP >= 12.1.x.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.