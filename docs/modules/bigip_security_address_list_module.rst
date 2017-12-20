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
                    <tr><td>region<br/><div style="font-size: small;"></div></td>
        <td>no</td>
        <td></td>
                <td></td>
                <td><div>Region name of the geolocation to use.</div>        </td></tr>
                    <tr><td>type<br/><div style="font-size: small;"></div></td>
        <td>yes</td>
        <td></td>
                <td><ul><li>Andorra (AD)</li><li>AE</li><li>AF</li><li>AG</li><li>AI</li><li>AL</li><li>AM</li><li>AN</li><li>AO</li><li>AP</li><li>AQ</li><li>AR</li><li>AS</li><li>AT</li><li>AU</li><li>AW</li><li>Aland Islands (AX)</li><li>AZ</li><li>BA</li><li>BB</li><li>BD</li><li>BE</li><li>BF</li><li>BG</li><li>BH</li><li>BI</li><li>BJ</li><li>BL</li><li>BM</li><li>BN</li><li>BO</li><li>BQ</li><li>BR</li><li>BS</li><li>BT</li><li>BV</li><li>BW</li><li>BY</li><li>BZ</li><li>CA</li><li>CC</li><li>CD</li><li>CF</li><li>CG</li><li>CH</li><li>CI</li><li>CK</li><li>CL</li><li>CM</li><li>CN</li><li>CO</li><li>CR</li><li>CU</li><li>CV</li><li>CX</li><li>CY</li><li>CZ</li><li>DE</li><li>DJ</li><li>DK</li><li>DM</li><li>DO</li><li>DZ</li><li>EC</li><li>EE</li><li>EG</li><li>EH</li><li>ER</li><li>ES</li><li>ET</li><li>EU</li><li>FI</li><li>FJ</li><li>FK</li><li>FM</li><li>FO</li><li>FR</li><li>FX</li><li>GA</li><li>GB</li><li>GD</li><li>GE</li><li>GF</li><li>GG</li><li>GH</li><li>GI</li><li>GL</li><li>GM</li><li>GN</li><li>GP</li><li>GQ</li><li>GR</li><li>GS</li><li>GT</li><li>GU</li><li>GW</li><li>GY</li><li>HK</li><li>HM</li><li>HN</li><li>HR</li><li>HT</li><li>HU</li><li>ID</li><li>IE</li><li>IL</li><li>IM</li><li>IN</li><li>IO</li><li>IQ</li><li>IR</li><li>IS</li><li>IT</li><li>JE</li><li>JM</li><li>JO</li><li>JP</li><li>KE</li><li>KG</li><li>KH</li><li>KI</li><li>JM</li><li>JN</li><li>KP</li><li>KR</li><li>KW</li><li>KY</li><li>KZ</li><li>LA</li><li>LB</li><li>LC</li><li>LI</li><li>LK</li><li>LR</li><li>LS</li><li>LT</li><li>LU</li><li>LV</li><li>LY</li><li>MA</li><li>MC</li><li>MD</li><li>ME</li><li>MF</li><li>MG</li><li>MH</li><li>MK</li><li>ML</li><li>MM</li><li>MN</li><li>MO</li><li>MP</li><li>MQ</li><li>MR</li><li>MS</li><li>MT</li><li>MU</li><li>MV</li><li>MW</li><li>MX</li><li>MY</li><li>MZ</li><li>NA</li><li>NC</li><li>NE</li><li>NF</li><li>NG</li><li>NI</li><li>NL</li><li>False</li><li>NP</li><li>NR</li><li>NU</li><li>NZ</li><li>OM</li><li>PA</li><li>PE</li><li>PF</li><li>PG</li><li>PH</li><li>PK</li><li>PL</li><li>PM</li><li>PN</li><li>PR</li><li>PS</li><li>PT</li><li>PW</li><li>PY</li><li>QA</li><li>RE</li><li>RO</li><li>RS</li><li>RU</li><li>RW</li><li>SA</li><li>SB</li><li>SC</li><li>SD</li><li>SE</li><li>SG</li><li>SH</li><li>SI</li><li>SJ</li><li>SK</li><li>SL</li><li>SM</li><li>SN</li><li>SO</li><li>SR</li><li>ST</li><li>SV</li><li>SY</li><li>SZ</li><li>TC</li><li>TD</li><li>TF</li><li>TG</li><li>TH</li><li>TJ</li><li>TK</li><li>TL</li><li>TM</li><li>TN</li><li>TO</li><li>TR</li><li>TT</li><li>TV</li><li>TW</li><li>TZ</li><li>UA</li><li>UG</li><li>UM</li><li>US</li><li>UY</li><li>UZ</li><li>VA</li></ul></td>
                <td>        </td></tr>
        </table>
    </td>
    </tr>
        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>Specifies the name of the address list.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"> (added in 2.5)</div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>Device partition to manage resources on.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Create a ...
      bigip_security_address_list:
        name: foo
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
        <td> param2 </td>
        <td> The new param2 value of the resource. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> Foo is bar </td>
    </tr>
            <tr>
        <td> param1 </td>
        <td> The new param1 value of the resource. </td>
        <td align=center> changed </td>
        <td align=center> bool </td>
        <td align=center> True </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - For more information on using Ansible to manage F5 Networks devices see https://www.ansible.com/ansible-f5.



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.