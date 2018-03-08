.. _bigip_routedomain_facts:


bigip_routedomain_facts - Retrieve route domain attributes from a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* Retrieve route domain attributes from a BIG-IP




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
                <tr><td>id<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The unique identifying integer representing the route domain.</div>        </td></tr>
                <tr><td>partition<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>Common</td>
        <td></td>
        <td><div>The partition the route domain resides on</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>BIG-IP password</div>        </td></tr>
                <tr><td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>BIG-IP host</div>        </td></tr>
                <tr><td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>BIG-IP username</div>        </td></tr>
                <tr><td>validate_certs<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div>        </td></tr>
        </table>
    </br>



Examples
--------

 ::

    
    - name: Get the facts for a route domain
      bigip_routedomain_facts:
        id: 1234
        password: secret
        server: lb.mydomain.com
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
        <td> service_policy </td>
        <td> Service policy to associate with the route domain </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> /Common/abc </td>
    </tr>
            <tr>
        <td> description </td>
        <td> Descriptive text that identifies the route domain </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> The foo route domain </td>
    </tr>
            <tr>
        <td> connection_limit </td>
        <td> Maximum number of concurrent connections allowed for the route domain </td>
        <td align=center> changed </td>
        <td align=center> integer </td>
        <td align=center> 0 </td>
    </tr>
            <tr>
        <td> strict </td>
        <td> Whether the system enforces cross-routing restrictions </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> enabled </td>
    </tr>
            <tr>
        <td> routing_protocol </td>
        <td> Dynamic routing protocols for the system to use in the route domain </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['BGP', 'OSPFv2'] </td>
    </tr>
            <tr>
        <td> bwc_policy </td>
        <td> Bandwidth controller for the route domain </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> /Common/foo </td>
    </tr>
            <tr>
        <td> evict_policy </td>
        <td> Eviction policy to use with this route domain </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> /Common/default-eviction-policy </td>
    </tr>
            <tr>
        <td> vlans </td>
        <td> VLANs for the system to use in the route domain </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['/Common/abc', '/Common/xyz'] </td>
    </tr>
            <tr>
        <td> id </td>
        <td> ID of the route domain </td>
        <td align=center> changed </td>
        <td align=center> integer </td>
        <td align=center> 1234 </td>
    </tr>
        
    </table>
    </br></br>




Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`/usage/support`


For help developing modules, should you be so inclined, please read :doc:`Getting Involved </development/getting-involved>`, :doc:`Writing a Module </development/writing-a-module>` and :doc:`Guidelines </development/guidelines>`.