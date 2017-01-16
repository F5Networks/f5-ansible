.. _bigip_gtm_pool:


bigip_gtm_pool - Manages F5 BIG-IP GTM pools.
+++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manages F5 BIG-IP GTM pools.


Requirements (on host that executes module)
-------------------------------------------

  * f5-sdk
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
            <tr>
    <td>alternate_lb_method<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul><li>round-robin</li><li>return-to-dns</li><li>none</li><li>ratio</li><li>topology</li><li>static-persistence</li><li>global-availability</li><li>virtual-server-capacity</li><li>packet-rate</li><li>drop-packet</li><li>fallback-ip</li><li>virtual-server-score</li></ul></td>
        <td><div>The load balancing mode that the system tries if the <code>preferred_lb_method</code> is unsuccessful in picking a pool.</div></td></tr>
            <tr>
    <td>fallback_ip<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul></ul></td>
        <td><div>Specifies the IPv4, or IPv6 address of the server to which the system directs requests when it cannot use one of its pools to do so. Note that the system uses the fallback IP only if you select the <code>fallback_ip</code> load balancing method.</div></td></tr>
            <tr>
    <td>fallback_lb_method<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul><li>round-robin</li><li>return-to-dns</li><li>ratio</li><li>topology</li><li>static-persistence</li><li>global-availability</li><li>virtual-server-capacity</li><li>least-connections</li><li>lowest-round-trip-time</li><li>fewest-hops</li><li>packet-rate</li><li>cpu</li><li>completion-rate</li><li>quality-of-service</li><li>kilobytes-per-second</li><li>drop-packet</li><li>fallback-ip</li><li>virtual-server-score</li></ul></td>
        <td><div>The load balancing mode that the system tries if both the <code>preferred_lb_method</code> and <code>alternate_lb_method</code>s are unsuccessful in picking a pool.</div></td></tr>
            <tr>
    <td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Name of the GTM pool.</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The password for the user account used to connect to the BIG-IP.</div></td></tr>
            <tr>
    <td>preferred_lb_method<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>None</td>
        <td><ul><li>round-robin</li><li>return-to-dns</li><li>ratio</li><li>topology</li><li>static-persistence</li><li>global-availability</li><li>virtual-server-capacity</li><li>least-connections</li><li>lowest-round-trip-time</li><li>fewest-hops</li><li>packet-rate</li><li>cpu</li><li>completion-rate</li><li>quality-of-service</li><li>kilobytes-per-second</li><li>drop-packet</li><li>fallback-ip</li><li>virtual-server-score</li></ul></td>
        <td><div>The load balancing mode that the system tries first.</div></td></tr>
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
    <td>yes</td>
    <td></td>
        <td><ul><li>present</li><li>absent</li><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Pool member state. When <code>present</code>, ensures that the pool is created and enabled. When <code>absent</code>, ensures that the pool is removed from the system. When <code>enabled</code> or <code>disabled</code>, ensures that the pool is enabled or disabled (respectively) on the remote device.</div></td></tr>
            <tr>
    <td>type<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>a</li><li>aaaa</li><li>cname</li><li>mx</li><li>naptr</li><li>srv</li></ul></td>
        <td><div>The type of GTM pool that you want to create. On BIG-IP releases prior to version 12, this parameter is not supported.</div></td></tr>
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
        </table>
    </br>



Examples
--------

 ::

      - name: Disable pool
        bigip_gtm_pool:
            server: "lb.mydomain.com"
            user: "admin"
            password: "secret"
            state: "disabled"
            pool: "my_pool"
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
        <td> changed </td>
        <td> Denotes if the F5 configuration was updated </td>
        <td align=center> always </td>
        <td align=center> bool </td>
        <td align=center>  </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note:: Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk
.. note:: Requires the netaddr Python package on the host. This is as easy as pip install netaddr


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

