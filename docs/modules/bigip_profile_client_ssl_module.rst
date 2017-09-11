.. _bigip_profile_client_ssl:


bigip_profile_client_ssl - Manages client SSL profiles on a BIG-IP
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5


.. contents::
   :local:
   :depth: 2


Synopsis
--------

* M
* a
* n
* a
* g
* e
* s
*  
* c
* l
* i
* e
* n
* t
*  
* S
* S
* L
*  
* p
* r
* o
* f
* i
* l
* e
* s
*  
* o
* n
*  
* a
*  
* B
* I
* G
* -
* I
* P
* .


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
                <tr><td>cert_key_chain<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>One or more certificates and keys to associate with the SSL profile. This option is always a list. The keys in the list dictate the details of the client/key/chain combination. Note that BIG-IPs can only have one of each type of each certificate/key type. This means that you can only have one RSA, one DSA, and one ECDSA per profile. If you attempt to assign two RSA, DSA, or ECDSA certificate/key combo, the device will reject this.</div><div>This list is a complex list that specifies a number of keys. There are several supported keys.</div><div>The <code>cert</code> key specifies a cert name for use. This key is required.</div><div>The <code>key</code> key contains a key name. This key is required.</div><div>The <code>chain</code> key contains a certificate chain that is relevant to the certificate and key mentioned earlier. This key is optional.</div>        </td></tr>
                <tr><td>ciphers<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td></td>
        <td><div>Specifies the list of ciphers that the system supports. When creating a new profile, the default cipher list is <code>DEFAULT</code>.</div>        </td></tr>
                <tr><td>name<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>-Specifies the name of the profile.</div>        </td></tr>
                <tr><td>parent<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td>/Common/clientssl</td>
        <td></td>
        <td><div>The parent template of this monitor template. Once this value has been set, it cannot be changed. By default, this value is the <code>clientssl</code> parent on the <code>Common</code> partition.</div>        </td></tr>
                <tr><td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td></td>
        <td><div>The password for the user account used to connect to the BIG-IP. This option can be omitted if the environment variable <code>F5_PASSWORD</code> is set.</div>        </td></tr>
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

    
    - name: Create client SSL profile
      bigip_profile_client_ssl:
          state: "present"
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          name: "my_profile"
      delegate_to: localhost
    
    - name: Create client SSL profile with specific ciphers
      bigip_profile_client_ssl:
          state: "present"
          server: "lb.mydomain.com"
          user: "admin"
          password: "secret"
          name: "my_profile"
          ciphers: "!SSLv3:!SSLv2:ECDHE+AES-GCM+SHA256:ECDHE-RSA-AES128-CBC-SHA"
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
        <td> ciphers </td>
        <td> The ciphers applied to the profile. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> !SSLv3:!SSLv2:ECDHE+AES-GCM+SHA256:ECDHE-RSA-AES128-CBC-SHA </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note::
    - Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.
    - Requires BIG-IP software version >= 12



Status
~~~~~~

This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.


Support
~~~~~~~

This module is community maintained without core committer oversight.

For more information on what this means please read :doc:`modules_support`


For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`dev_guide/developing_test_pr` and :doc:`dev_guide/developing_modules`.