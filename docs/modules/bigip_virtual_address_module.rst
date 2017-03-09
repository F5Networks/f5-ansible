.. _bigip_virtual_address:


bigip_virtual_address - Manage LTM virtual addresses on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage LTM virtual addresses on a BIG-IP




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
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Virtual address</div></br>
        <div style="font-size: small;">aliases: name<div></td></tr>
            <tr>
    <td>advertise_route<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul><li>always</li><li>when_all_available</li><li>when_any_available</li></ul></td>
        <td><div>Specifies what routes of the virtual address the system advertises. When <code>when_any_available</code>, advertises the route when any virtual server is available. When <code>when_all_available</code>, advertises the route when all virtual servers are available. When (always), always advertises the route regardless of the virtual servers available.</div></td></tr>
            <tr>
    <td>arp_state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Specifies whether the system accepts ARP requests. When (disabled), specifies that the system does not accept ARP requests. Note that both ARP and ICMP Echo must be disabled in order for forwarding virtual servers using that virtual address to forward ICMP packets. If (enabled), then the packets are dropped.</div></td></tr>
            <tr>
    <td>auto_delete<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Specifies whether the system automatically deletes the virtual address with the deletion of the last associated virtual server. When <code>disabled</code>, specifies that the system leaves the virtual address even when all associated virtual servers have been deleted. When creating the virtual address, the default value is <code>enabled</code>.</div></td></tr>
            <tr>
    <td>connection_limit<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>Specifies the number of concurrent connections that the system allows on this virtual address.</div></td></tr>
            <tr>
    <td>icmp_echo<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li><li>selective</li></ul></td>
        <td><div>Specifies how the systems sends responses to (ICMP) echo requests on a per-virtual address basis for enabling route advertisement. When <code>enabled</code>, the BIG-IP system intercepts ICMP echo request packets and responds to them directly. When <code>disabled</code>, the BIG-IP system passes ICMP echo requests through to the backend servers. When (selective), causes the BIG-IP system to internally enable or disable responses based on virtual server state; <code>when_any_available</code>, <code>when_all_available, or C(always</code>, regardless of the state of any virtual servers.</div></td></tr>
            <tr>
    <td>netmask<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>255.255.255.255</td>
        <td><ul></ul></td>
        <td><div>Netmask of the provided virtual address. This value cannot be modified after it is set.</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The BIG-IP host. This option can be omitted if the environment variable <code>F5_SERVER</code> is set.</div></td></tr>
            <tr>
    <td>server_port<br/><div style="font-size: small;"> (added in 2.2)</div></td>
    <td>no</td>
    <td>443</td>
        <td><ul></ul></td>
        <td><div>The BIG-IP server port. This option can be omitted if the environment variable <code>F5_SERVER_PORT</code> is set.</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li><li>enabled</li><li>disabled</li></ul></td>
        <td><div>The virtual address state. If <code>absent</code>, an attempt to delete the virtual address will be made. This will only succeed if this virtual address is not in use by a virtual server. <code>present</code> creates the virtual address and enables it. If <code>enabled</code>, enable the virtual address if it exists. If <code>disabled</code>, create the virtual address if needed, and set state to <code>disabled</code>.</div></td></tr>
            <tr>
    <td>use_route_advertisement<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>Specifies whether the system uses route advertisement for this virtual address. When disabled, the system does not advertise routes for this virtual address.</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The username to connect to the BIG-IP with. This user must have administrative privileges on the device. This option can be omitted if the environment variable <code>F5_USER</code> is set.</div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"> (added in 2.0)</div></td>
    <td>no</td>
    <td>True</td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. This option can be omitted if the environment variable <code>F5_VALIDATE_CERTS</code> is set.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: Add virtual address
      bigip_virtual_address:
          server: lb.mydomain.net
          user: admin
          password: secret
          state: present
          partition: Common
          address: 10.10.10.10
      delegate_to: localhost


Notes
-----

.. note:: Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

