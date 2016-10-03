.. _bigip_selfip:


bigip_selfip - Manage Self-IPs on a BIG-IP system
+++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage Self-IPs on a BIG-IP system


Requirements (on host that executes module)
-------------------------------------------

  * netaddr
  * f5-sdk


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
            <tr>
    <td>address<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The IP addresses for the new self IP. This value is ignored upon update as addresses themselves cannot be changed after they are created.</div></td></tr>
            <tr>
    <td>allow_service<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Configure port lockdown for the Self IP. By default, the Self IP has a "default deny" policy. This can be changed to allow TCP and UDP ports as well as specific protocols. This list should contain <code>protocol</code>:<code>port</code> values.</div></td></tr>
            <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td>Value of C(address)</td>
        <td><ul></ul></td>
        <td><div>The self IP to create.</div></td></tr>
            <tr>
    <td>netmask<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The netmasks for the self IP.</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The password for the user account used to connect to the BIG-IP.</div></td></tr>
            <tr>
    <td>route_domain<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>none</td>
        <td><ul></ul></td>
        <td><div>The route domain id of the system. If none, id of the route domain will be "0" (default route domain)</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The BIG-IP host.</div></td></tr>
            <tr>
    <td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td><ul></ul></td>
        <td><div>The BIG-IP server port.</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>absent</li><li>present</li></ul></td>
        <td><div>The state of the variable on the system. When <code>present</code>, guarantees that the Self-IP exists with the provided attributes. When <code>absent</code>, removes the Self-IP from the system.</div></td></tr>
            <tr>
    <td>traffic_group<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The traffic group for the self IP addresses in an active-active, redundant load balancer configuration.</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device.</div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div></td></tr>
            <tr>
    <td>vlan<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The VLAN that the new self IPs will be on.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: Create Self IP
      bigip_selfip:
          address: "10.10.10.10"
          name: "self1"
          netmask: "255.255.255.0"
          password: "secret"
          server: "lb.mydomain.com"
          user: "admin"
          validate_certs: "no"
          vlan: "vlan1"
      delegate_to: localhost
    - name: Create Self IP with a Route Domain
      bigip_selfip:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          validate_certs: "no"
          name: "self1"
          address: "10.10.10.10"
          netmask: "255.255.255.0"
          vlan: "vlan1"
          route_domain: "10"
          allow_service: "default"
      delegate_to: localhost
    - name: Delete Self IP
      bigip_selfip:
          name: "self1"
          password: "secret"
          server: "lb.mydomain.com"
          state: "absent"
          user: "admin"
          validate_certs: "no"
      delegate_to: localhost
    - name: Allow management web UI to be accessed on this Self IP
      bigip_selfip:
          name: "self1"
          password: "secret"
          server: "lb.mydomain.com"
          state: "absent"
          user: "admin"
          validate_certs: "no"
          allow_service:
              - "tcp:443"
      delegate_to: localhost
    - name: Allow HTTPS and SSH access to this Self IP
      bigip_selfip:
          name: "self1"
          password: "secret"
          server: "lb.mydomain.com"
          state: "absent"
          user: "admin"
          validate_certs: "no"
          allow_service:
              - "tcp:443"
              - "tpc:22"
      delegate_to: localhost
    - name: Allow all services access to this Self IP
      bigip_selfip:
          name: "self1"
          password: "secret"
          server: "lb.mydomain.com"
          state: "absent"
          user: "admin"
          validate_certs: "no"
          allow_service:
              - all
      delegate_to: localhost
    - name: Allow only GRE and IGMP protocols access to this Self IP
      bigip_selfip:
          name: "self1"
          password: "secret"
          server: "lb.mydomain.com"
          state: "absent"
          user: "admin"
          validate_certs: "no"
          allow_service:
              - gre:0
              - igmp:0
      delegate_to: localhost
    - name: Allow all TCP, but no other protocols access to this Self IP
      bigip_selfip:
          name: "self1"
          password: "secret"
          server: "lb.mydomain.com"
          state: "absent"
          user: "admin"
          validate_certs: "no"
          allow_service:
              - tcp:0
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
        <td> netmask </td>
        <td> The netmask of the Self IP </td>
        <td align=center> ['changed', 'created'] </td>
        <td align=center> string </td>
        <td align=center> 255.255.255.0 </td>
    </tr>
            <tr>
        <td> name </td>
        <td> The name of the Self IP </td>
        <td align=center> ['created', 'changed', 'deleted'] </td>
        <td align=center> string </td>
        <td align=center> self1 </td>
    </tr>
            <tr>
        <td> address </td>
        <td> The address for the Self IP </td>
        <td align=center> created </td>
        <td align=center> string </td>
        <td align=center> 192.0.2.10 </td>
    </tr>
            <tr>
        <td> traffic_group </td>
        <td> The traffic group that the Self IP is a member of </td>
        <td align=center>  </td>
        <td align=center> string </td>
        <td align=center> traffic-group-local-only </td>
    </tr>
            <tr>
        <td> vlan </td>
        <td> The VLAN set on the Self IP </td>
        <td align=center>  </td>
        <td align=center> string </td>
        <td align=center> vlan1 </td>
    </tr>
            <tr>
        <td> allow_service </td>
        <td> Services that allowed via this Self IP </td>
        <td align=center> changed </td>
        <td align=center> list </td>
        <td align=center> ['igmp:0', 'tcp:22', 'udp:53'] </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note:: Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
.. note:: Requires the netaddr Python package on the host.


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

