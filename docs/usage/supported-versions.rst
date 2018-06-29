Releases and Versioning
-----------------------

F5 tests and supports the following versions.

The F5 Modules for Ansible may work with versions not shown here; F5 has not verified functionality in those versions.

+-------------------------+-----------------------+----------------------+
| **Ansible Version**     | **BIG-IP versions**   | **BIG-IQ versions**  |
+=========================+=======================+======================+
| * v2.5                  | * v12.x               | * v5.4.x             |
| * v2.6                  | * v13.x               |                      |
+-------------------------+-----------------------+----------------------+

.. important::

   F5 Networks does not back-port changes to earlier versions of Ansible.

For a detailed list of BIG-IP versions that are currently supported by F5, see |k5903|.

.. |k5903| raw:: html

   <a href="https://support.f5.com/csp/article/K5903" target="_blank">this solution article</a>

When a version of BIG-IP reaches end of technical support, F5 supports it until the next Ansible release.

For example, if a version of BIG-IP reaches end of technical support on January 1, and Ansible releases a new version on March 1, then F5 supports the modules on that version of BIG-IP until March 1.

Experimental Module Support
```````````````````````````

F5 Networks accepts support cases for F5 modules that have shipped with supported versions of Ansible. See the preceding table for details.

The F5 Modules for Ansible are included when you install Ansible. The F5 Modules for Ansible located in this project's |github_repo| are considered to be experimental and not production-ready.

If an experimental module's DOCUMENTATION block has a completed ``Tested platforms`` section, then the module is likely complete and ready for testing. You can create issues for these modules `here <https://github.com/F5Networks/f5-ansible/issues>`_.


.. |github_repo| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible" target="_blank">GitHub repo</a>
