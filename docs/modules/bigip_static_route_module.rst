.. _bigip_static_route:


bigip_static_route - Manipulate static routes on a BIG-IP
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manipulate static routes on a BIG-IP.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 2.2.3
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
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Descriptive text that identifies the route.</div>        </td></tr>
                <tr><td>destination<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Specifies an IP address, and netmask, for the static entry in the routing table. When <code>state</code> is <code>present</code>, this value is required.</div>        </td></tr>
                <tr><td>gateway_address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Specifies the router for the system to use when forwarding packets to the destination host or network. Also known as the next-hop router address. This can be either an IPv4 or IPv6 address. When it is an IPv6 address that starts with <code>FE80:</code>, the address will be treated as a link-local address. This requires that the <code>vlan</code> parameter also be supplied.</div>        </td></tr>
                <tr><td>mtu<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Specifies a specific maximum transmission unit (MTU).</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Name of the static route.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                <tr><td>pool<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Specifies the pool through which the system forwards packets to the destination.</div>        </td></tr>
                <tr><td>reject<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Specifies that the system drops packets sent to the destination.</div>        </td></tr>
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
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>When <code>present</code>, ensures that the cloud connector exists. When <code>absent</code>, ensures that the cloud connector does not exist.</div>        </td></tr>
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
                <tr><td>vlan<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td></td>
        <td><div>Specifies the VLAN or Tunnel through which the system forwards packets to the destination. When <code>gateway_address</code> is a link-local IPv6 address, this value is required</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create static route with gateway address
      bigip_static_route:
        destination: 10.10.10.10
        gateway_address: 10.2.2.3
        name: test-route
        password: secret
        server: lb.mydomain.come
        user: admin
        validate_certs: no
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
        <td> destination </td>
        <td> Whether the banner is enabled or not. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> gateway_address </td>
        <td> Whether the banner is enabled or not. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> description </td>
        <td> Whether the banner is enabled or not. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> reject </td>
        <td> Whether the banner is enabled or not. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> vlan </td>
        <td> Whether the banner is enabled or not. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> True </td>
    </tr>
            <tr>
        <td> pool </td>
        <td> Whether the banner is enabled or not. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> True </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - Requires the netaddr Python package on the host. This is as easy as pip install netaddr.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.