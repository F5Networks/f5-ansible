.. _bigip_security_address_list:


bigip_security_address_list - Manage address lists on BIG-IP AFM
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Manages the AFM address lists on a BIG-IP. This module can be used to add and remove address list entries.


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
                <tr><td>address_lists<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Simple list of existing address lists to add to this list. Address lists can be specified in either their fully qualified name (/Common/foo) or their short name (foo). If a short name is used, the <code>partition</code> argument will automatically be prepended to the short name.</div>        </td></tr>
                <tr><td>address_ranges<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>A list of address ranges where the range starts with a port number, is followed by a dash (-) and then a second number.</div><div>If the first address is greater than the second number, the numbers will be reversed so-as to be properly formatted. ie, <code>2.2.2.2-1.1.1</code>. would become <code>1.1.1.1-2.2.2.2</code>.</div>        </td></tr>
                <tr><td>addresses<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Individual addresses that you want to add to the list. These addresses differ from ranges, and lists of lists such as what can be used in <code>address_ranges</code> and <code>address_lists</code> respectively.</div>        </td></tr>
                <tr><td>description<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Description of the address list</div>        </td></tr>
                <tr><td>fqdns<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>A list of fully qualified domain names (FQDNs).</div><div>An FQDN has at least one decimal point in it, separating the host from the domain.</div><div>To add FQDNs to a list requires that a global FQDN resolver be configured. At the moment, this must either be done via <code>bigip_command</code>, or, in the GUI of BIG-IP. If using <code>bigip_command</code>, this can be done with <code>tmsh modify security firewall global-fqdn-policy FOO</code> where <code>FOO</code> is a DNS resolver configured at <code>tmsh create net dns-resolver FOO</code>.</div>        </td></tr>
                <tr><td rowspan="2">geo_locations<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td><td></td>
    <td> <div>List of geolocations specified by their <code>country</code> and <code>region</code>.</div>    </tr>
    <tr>
    <td colspan="5">
    <table border=1 cellpadding=4>
    <caption><b>Dictionary object geo_locations</b></caption>
    <tr>
    <th class="head">parameter</th>
    <th class="head">required</th>
    <th class="head">default</th>
    <th class="head">choices</th>
    <th class="head">comments</th>
    </tr>
                    <tr><td>country<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td><ul><li>Any valid 2 character ISO country code.</li><li>Any valid country name.</li></ul></td>
                <td><div>The country name, or code, of the geolocation to use.</div><div>In addition to the country full names, you may also specify their abbreviated form, such as <code>US</code> instead of <code>United States</code>.</div><div>Valid country codes can be found here https://countrycode.org/.</div>        </td></tr>
                    <tr><td>region<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Region name of the country to use.</div>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Specifies the name of the address list.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"></div></td>
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
                <tr><td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li></ul></td>
        <td><div>When <code>present</code>, ensures that the address list and entries exists.</div><div>When <code>absent</code>, ensures the address list is removed.</div>        </td></tr>
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

    
    - name: Create an address list
      bigip_security_address_list:
        name: foo
        addresses:
          - 3.3.3.3
          - 4.4.4.4
          - 5.5.5.5
        password: secret
        server: lb.mydomain.com
        state: present
        user: admin
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
        <td> geo_locations </td>
        <td> The new list of geo locations applied to the address list. </td>
        <td align=center> changed </td>
        <td align=center> complex </td>
        <td align=center>  </td>
    </tr>
            <tr>
        <td> description </td>
        <td> The new description of the address list. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> My address list </td>
    </tr>
            <tr>
        <td> address_lists </td>
        <td> The new list of address list names applied to the address list. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['/Common/list1', '/Common/list2'] </td>
    </tr>
            <tr>
        <td> address_ranges </td>
        <td> The new list of address ranges applied to the address list. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['1.1.1.1-2.2.2.2', '3.3.3.3-4.4.4.4'] </td>
    </tr>
            <tr>
        <td> fqdns </td>
        <td> The new list of FQDN names applied to the address list. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['google.com', 'mit.edu'] </td>
    </tr>
            <tr>
        <td> addresses </td>
        <td> The new list of addresses applied to the address list. </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['1.1.1.1', '2.2.2.2'] </td>
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