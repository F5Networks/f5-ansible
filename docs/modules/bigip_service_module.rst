:source: modules/bigip_service.py

.. _bigip_service:


bigip_service - Manage BIG-IP service states
++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.2

.. contents::
   :local:
   :depth: 2


Synopsis
--------
- Manage BIG-IP service states



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- bigsuds


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
                <tr>
            <th class="head"><div class="cell-border">Parameter</div></th>
            <th class="head"><div class="cell-border">Choices/<font color="blue">Defaults</font></div></th>
                        <th class="head" width="100%"><div class="cell-border">Comments</div></th>
        </tr>
                    <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>name</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                                    <li>big3d</li>
                                                                                                                                                                                                                        <li>gtmd</li>
                                                                                                                                                                                                                        <li>named</li>
                                                                                                                                                                                                                        <li>ntpd</li>
                                                                                                                                                                                                                        <li>snmpd</li>
                                                                                                                                                                                                                        <li>sshd</li>
                                                                                                                                                                                                                        <li>zrd</li>
                                                                                                                                                                                                                        <li>websso</li>
                                                                                                </ul>
                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>Name of the service</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>password</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                        <b>Default:</b><br/><div style="color: blue">admin</div>
                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>BIG-IP password</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>server</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>BIG-IP host</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>state</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                        <ul><b>Choices:</b>
                                                                                                                                                                                    <li>started</li>
                                                                                                                                                                                                                        <li>stopped</li>
                                                                                                                                                                                                                        <li>restarted</li>
                                                                                                </ul>
                                                                                                    <b>Default:</b><br/><div style="color: blue">None</div>
                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div><code>started</code>/<code>stopped</code> are idempotent actions that will not run commands unless necessary. <code>restarted</code> will always bounce the service.</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>user</b>
                            <br/><div style="font-size: small; color: red">required</div>                                                    </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>BIG-IP username</div>
                                                                                                </div>
                </td>
            </tr>
                                <tr class="return-value-column">
                                <td>
                    <div class="outer-elbow-container">
                                                <div class="elbow-key">
                            <b>validate_certs</b>
                                                                                </div>
                    </div>
                </td>
                                <td>
                    <div class="cell-border">
                                                                                                                                                                                                                                                                    <ul><b>Choices:</b>
                                                                                                                                                                                                                                                                <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                                                                                                                                                                                                                                                                                                    <li>no</li>
                                                                                                </ul>
                                                                                                    <b>Default:</b><br/><div style="color: blue">yes</div>
                                            </div>
                </td>
                                                                <td>
                    <div class="cell-border">
                                                                                    <div>If <code>no</code>, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.</div>
                                                                                                </div>
                </td>
            </tr>
                        </table>
    <br/>


Notes
-----

.. note::
    - Requires the bigsuds Python package on the host if using the iControl interface. This is as easy as pip install bigsuds


Examples
--------

.. code-block:: yaml

    
    - name: Restart the BIG-IP sshd service
      bigip_service:
        server: lb.mydomain.com
        name: sshd
        user: admin
        password: secret
        state: restarted
      delegate_to: localhost





Status
------



This module is flagged as **preview** which means that it is not guaranteed to have a backwards compatible interface.




Author
~~~~~~

- Tim Rupp (@caphrim007)

