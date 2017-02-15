.. _bigip_sys_global:


bigip_sys_global - Manage BIG-IP global settings.
+++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.3


.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage BIG-IP global settings.


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
    <td>banner_text<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Specifies the text to present in the advisory banner.</div></td></tr>
            <tr>
    <td>console_timeout<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Specifies the number of seconds of inactivity before the system logs off a user that is logged on.</div></td></tr>
            <tr>
    <td>gui_setup<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div><code>enable</code> or <code>disabled</code> the Setup utility in the browser-based Configuration utility</div></td></tr>
            <tr>
    <td>lcd_display<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Specifies, when <code>enabled</code>, that the system menu displays on the LCD screen on the front of the unit. This setting has no effect when used on the VE platform.</div></td></tr>
            <tr>
    <td>mgmt_dhcp<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Specifies whether or not to enable DHCP client on the management interface</div></td></tr>
            <tr>
    <td>net_reboot<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Specifies, when <code>enabled</code>, that the next time you reboot the system, the system boots to an ISO image on the network, rather than an internal media drive.</div></td></tr>
            <tr>
    <td>password<br/><div style="font-size: small;"></div></td>
    <td>yes</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>The password for the user account used to connect to the BIG-IP.</div></td></tr>
            <tr>
    <td>quiet_boot<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul></ul></td>
        <td><div>Specifies, when <code>enabled</code>, that the system suppresses informational text on the console during the boot cycle. When <code>disabled</code>, the system presents messages and informational text on the console during the boot cycle.</div></td></tr>
            <tr>
    <td>security_banner<br/><div style="font-size: small;"></div></td>
    <td>no</td>
    <td></td>
        <td><ul><li>enabled</li><li>disabled</li></ul></td>
        <td><div>Specifies whether the system displays an advisory message on the login screen.</div></td></tr>
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
        <td><ul><li>present</li></ul></td>
        <td><div>The state of the variable on the system. When <code>present</code>, guarantees that an existing variable is set to <code>value</code>.</div></td></tr>
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

    - name: Disable the setup utility
      bigip_sys_global:
          gui_setup: "disabled"
          password: "secret"
          server: "lb.mydomain.com"
          user: "admin"
          state: "present"
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
        <td> security_banner </td>
        <td> The new setting for whether the system should display an advisory message on the login screen or not
 </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> enabled </td>
    </tr>
            <tr>
        <td> net_reboot </td>
        <td> The new setting for whether the system should boot to an ISO on the network or not
 </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> enabled </td>
    </tr>
            <tr>
        <td> banner_text </td>
        <td> The new text to present in the advisory banner. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> This is a corporate device. Do not touch. </td>
    </tr>
            <tr>
        <td> console_timeout </td>
        <td> The new number of seconds of inactivity before the system logs off a user that is logged on.
 </td>
        <td align=center> changed </td>
        <td align=center> integer </td>
        <td align=center> 600 </td>
    </tr>
            <tr>
        <td> quiet_boot </td>
        <td> The new setting for whether the system should suppress information to the console during boot or not.
 </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> enabled </td>
    </tr>
            <tr>
        <td> mgmt_dhcp </td>
        <td> The new setting for whether the mgmt interface should DHCP or not
 </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> enabled </td>
    </tr>
            <tr>
        <td> gui_setup </td>
        <td> The new setting for the Setup utility. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> enabled </td>
    </tr>
            <tr>
        <td> lcd_display </td>
        <td> The new setting for displaying the system menu on the LCD. </td>
        <td align=center> changed </td>
        <td align=center> string </td>
        <td align=center> enabled </td>
    </tr>
        
    </table>
    </br></br>

Notes
-----

.. note:: Requires the f5-sdk Python package on the host. This is as easy as pip install f5-sdk.


    
This is an Extras Module
------------------------

For more information on what this means please read :doc:`modules_extra`

    
For help in developing on modules, should you be so inclined, please read :doc:`community`, :doc:`developing_test_pr` and :doc:`developing_modules`.

