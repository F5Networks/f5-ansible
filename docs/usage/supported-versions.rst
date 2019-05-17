Releases and Versioning
-----------------------

Learn more about our `Support Policy <https://f5.com/support/support-policies>`_ and
`BIG-IP product support policies <https://support.f5.com/csp/article/K5903>`_.

.. important::

   * F5 follows Ansible’s model and supports the two most recent major stable releases.
   * F5 does not back-port changes to earlier versions of Ansible.

BIG-IP
``````
These BIG-IP versions are supported in these Ansible versions.

+-------------------------+----------------------+------------------------+------------------------+
| BIG-IP version          | Ansible 2.6          | Ansible 2.7            | Ansible 2.8            |
+=========================+======================+========================+========================+
| BIG-IP 14.x             | X                    | X                      | X                      |
+-------------------------+----------------------+------------------------+------------------------+
| BIG-IP 13.x             | X                    | X                      | X                      |
+-------------------------+----------------------+------------------------+------------------------+
| BIG-IP 12.x             | X                    | X                      | X                      |
+-------------------------+----------------------+------------------------+------------------------+
| BIG-IP 11.x and earlier | not supported        | not supported          | not supported          |
+-------------------------+----------------------+------------------------+------------------------+



BIG-IQ
``````
These BIG-IQ versions are supported in these Ansible versions.

+-------------------------+----------------------+------------------------+------------------------+
| BIG-IP version          | Ansible 2.6          | Ansible 2.7            | Ansible 2.8            |
+=========================+======================+========================+========================+
| BIG-IQ 6.x              | X                    | X                      | X                      |
+-------------------------+----------------------+------------------------+------------------------+
| BIG-IQ 5.4              | X                    | X                      | X                      |
+-------------------------+----------------------+------------------------+------------------------+
| BIG-IQ <= 5.3           | not supported        | not supported          | not supported          |
+-------------------------+----------------------+------------------------+------------------------+

Experimental Module Support
```````````````````````````

F5 Networks accepts support cases for F5 modules that have shipped with supported versions of
Ansible. See the preceding table for details.

The F5 Modules for Ansible are included when you install Ansible. The F5 Modules for Ansible
located in this project's |github_repo| are considered to be experimental and not production-ready.

If an experimental module's DOCUMENTATION block has a completed ``Tested platforms`` section,
then the module is likely complete and ready for testing. You can create issues for these modules
`here <https://github.com/F5Networks/f5-ansible/issues>`_.


.. |github_repo| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible" target="_blank">GitHub repo</a>

.. |check| image:: ../_static/check.png
.. |x| image:: ../_static/x.png
