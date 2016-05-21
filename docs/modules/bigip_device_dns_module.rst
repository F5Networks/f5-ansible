.. _bigip_device_dns:


bigip_device_dns - Manage BIG-IP device DNS settings
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage BIG-IP device DNS settings


Requirements (on host that executes module)
-------------------------------------------

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
    <td>append<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>True</li><li>False</li></ul></td>
        <td><div>If <code>yes</code>, will only add specific servers to the device configuration, not set them to just the list in <code>nameserver</code>, <code>nameservers</code>, <code>forwarder</code>, <code>forwarders</code>, <code>search_domain</code> or <code>search_domains</code>.</div></td></tr>
            <tr>
    <td>cache<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>disable</td>
        <td><ul><li>enable</li><li>disable</li></ul></td>
        <td><div>Specifies whether the system caches DNS lookups or performs the operation each time a lookup is needed. Please note that this applies only to Access Policy Manager features, such as ACLs, web application rewrites, and authentication.</div></td></tr>
            <tr>
    <td>forwarder<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>A single BIND servers that the system can use to perform DNS lookups. BIND allows you to cache and store DNS requests and responses on a local server and minimize DNS server requests, and bandwidth. At least one of <code>forwarders</code> or <code>forwarder</code> are required.</div></td></tr>
            <tr>
    <td>forwarders<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>A list of BIND servers that the system can use to perform DNS lookups. BIND allows you to cache and store DNS requests and responses on a local server and minimize DNS server requests, and bandwidth. At least one of <code>forwarders</code> or <code>forwarder</code> are required.</div></td></tr>
            <tr>
    <td>ip_version<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>4</td>
        <td><ul><li>4</li><li>6</li></ul></td>
        <td><div>Specifies whether the DNS specifies IP addresses using IPv4 or IPv6.</div></td></tr>
            <tr>
    <td>nameserver<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>A single name server that the system uses to validate DNS lookups, and resolve host names. At least one of <code>nameservers</code> or <code>nameserver</code> are required.</div></td></tr>
            <tr>
    <td>nameservers<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>A list of name servers that the system uses to validate DNS lookups, and resolve host names. At least one of <code>nameservers</code> or <code>nameserver</code> are required.</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP password</div></td></tr>
            <tr>
    <td>search_domain<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>A single domain that the system searches for local domain lookups, to resolve local host names. At least one of <code>search_domains</code> or <code>search_domain</code> are required.</div></td></tr>
            <tr>
    <td>search_domains<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>A list of domains that the system searches for local domain lookups, to resolve local host names. At least one of <code>search_domains</code> or <code>search_domain</code> are required.</div></td></tr>
            <tr>
    <td>server<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP host</div></td></tr>
            <tr>
    <td>state<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>absent</li><li>present</li></ul></td>
        <td><div>The state of the variable on the system. When <code>present</code>, guarantees that an existing variable is set to <code>value</code>.</div></td></tr>
            <tr>
    <td>user<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>BIG-IP username</div></br>
        <div style="font-size: small;">aliases: username<div></td></tr>
            <tr>
    <td>validate_certs<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>True</td>
        <td><ul></ul></td>
        <td><div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div></td></tr>
        </table>
    </br>



Examples
--------

 ::

    - name: Set the DNS settings on the BIG-IP
      bigip_device_dns:
          server: "big-ip"
          nameservers: [208.67.222.222, 208.67.220.220]
          forwarders: []
          search_domains:
              - localdomain
              - lab.local
          state: present
      delegate_to: localhost


Notes
-----

.. note:: Requires the requests Python package on the host. This is as easy as pip install requests


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

