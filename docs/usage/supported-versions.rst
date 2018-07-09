Releases and Versioning
-----------------------

Learn more about our `Support Policy <https://f5.com/support/support-policies>`_ and
`BIG-IP product support policies <https://support.f5.com/csp/article/K5903>`_.

.. important::

   * F5 follows Ansible’s model and supports the two most recent major stable releases.
   * F5 does not back-port changes to earlier versions of Ansible.

The tables below display F5 product and Ansible versions that are eligible for support.

BIG-IP
``````

.. container:: support-matrix

   +-------------------------+----------------------+------------------------+
   |                         | Ansible 2.5          |  Ansible 2.6           |
   +=========================+======================+========================+
   | BIG-IP 13.x             | |check|              |  |check|               |
   +-------------------------+----------------------+------------------------+
   | BIG-IP 12.x             | |check|              |  |check|               |
   +-------------------------+----------------------+------------------------+
   | BIG-IP <= 11.x          | |x|                  |  |x|                   |
   +-------------------------+----------------------+------------------------+

BIG-IQ
``````

.. container:: support-matrix

   +-------------------------+----------------------+------------------------+
   |                         | Ansible 2.5          |  Ansible 2.6           |
   +=========================+======================+========================+
   | BIG-IQ 6.0              | |check|              |  |check|               |
   +-------------------------+----------------------+------------------------+
   | BIG-IQ 5.4              | |check|              |  |check|               |
   +-------------------------+----------------------+------------------------+
   | BIG-IQ <= 5.3           | |x|                  |  |x|                   |
   +-------------------------+----------------------+------------------------+

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

.. |check| image:: ../_static/check.svg
.. |x| image:: ../_static/x.svg
