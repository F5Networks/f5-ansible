.. _bigip_snmp_trap:


bigip_snmp_trap - Manipulate SNMP trap information on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.4


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manipulate SNMP trap information on a BIG-IP.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk >= 2.2.0


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
                <tr><td>community<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the community name for the trap destination.</div>        </td></tr>
                <tr><td>destination<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the address for the trap destination. This can be either an IP address or a hostname.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Name of the SNMP configuration endpoint.</div>        </td></tr>
                <tr><td>network<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>other</li><li>management</li><li>default</li></ul></td>
        <td><div>Specifies the name of the trap network. This option is not supported in versions of BIG-IP &lt; 12.1.0. If used on versions &lt; 12.1.0, it will simply be ignored.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
                <tr><td>port<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the port for the trap destination.</div>        </td></tr>
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
                <tr><td>snmp_version<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>1</li><li>2c</li></ul></td>
        <td><div>Specifies to which Simple Network Management Protocol (SNMP) version the trap destination applies.</div>        </td></tr>
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
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create snmp v1 trap
      bigip_snmp_trap:
          community: "general"
          destination: "1.2.3.4"
          name: "my-trap1"
          network: "management"
          port: "9000"
          snmp_version: "1"
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
      delegate_to: localhost
    
    - name: Create snmp v2 trap
      bigip_snmp_trap:
          community: "general"
          destination: "5.6.7.8"
          name: "my-trap2"
          network: "default"
          port: "7000"
          snmp_version: "2c"
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
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
        <td> snmp_version </td>
        <td> The new C(snmp_version) configured on the remote device. </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> 2c </td>
    </tr>
            <tr>
        <td> destination </td>
        <td> The new address for the trap destination in either IP or hostname form. </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> 1.2.3.4 </td>
    </tr>
            <tr>
        <td> port </td>
        <td> The new C(port) of the trap destination. </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> 900 </td>
    </tr>
            <tr>
        <td> community </td>
        <td> The new C(community) name for the trap destination. </td>
        <td align=center> changed and success </td>
        <td align=center> list </td>
        <td align=center> secret </td>
    </tr>
            <tr>
        <td> network </td>
        <td> The new name of the network the SNMP trap is on. </td>
        <td align=center> changed and success </td>
        <td align=center> string </td>
        <td align=center> management </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - This module only supports version v1 and v2c of SNMP.
    - The ``network`` option is not supported on versions of BIG-IP < 12.1.0 because the platform did not support that option until 12.1.0. If used on versions < 12.1.0, it will simply be ignored.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.