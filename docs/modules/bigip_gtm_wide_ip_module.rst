.. _bigip_gtm_wide_ip:


bigip_gtm_wide_ip - Manages F5 BIG-IP GTM wide ip.
++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.0


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages F5 BIG-IP GTM wide ip.


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
    <td>lb_method<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul><li>round-robin</li><li>ratio</li><li>topology</li><li>global-availability</li></ul></td>
        <td><div>Specifies the load balancing method used to select a pool in this wide IP. This setting is relevant only when multiple pools are configured for a wide IP.</div></td></tr>
            <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Wide IP name. This name must be formatted as a fully qualified domain name (FQDN). You can also use the alias <code>wide_ip</code> but this is deprecated and will be removed in a future Ansible version.</div></br>
        <div style="font-size: small;">aliases: wide_ip<div></td></tr>
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
    <td>state<br/><div style="font-size: small;"> (added in 2.4)</div></td>
    <td>no</td>
    <td>present</td>
        <td><ul><li>present</li><li>absent</li><li>disabled</li></ul></td>
        <td><div>When <code>present</code>, ensures that the Wide IP exists and is enabled. When <code>absent</code>, ensures that the Wide IP has been removed. When <code>disabled</code>, ensures that the Wide IP exists and is disabled.</div></td></tr>
            <tr>
    <td>type<br/><div style="font-size: small;"> (added in 2.4)</div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>a</li><li>aaaa</li><li>cname</li><li>mx</li><li>naptr</li><li>srv</li></ul></td>
        <td><div>Specifies the type of wide IP. GTM wide IPs need to be keyed by query type in addition to name, since pool members need different attributes depending on the response RDATA they are meant to supply. This value is required if you are using BIG-IP versions &gt;= 12.0.0.</div></td></tr>
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

    - name: Set lb method
      bigip_gtm_wide_ip:
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          lb_method: "round-robin"
          name: "my-wide-ip.example.com"
      delegate_to: localhost


Notes
-----

.. note:: Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

