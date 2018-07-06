Releases and Versioning
-----------------------

F5 Ansible modules in 2.5.0 & 2.6.0 are supported on TMOS 12.x & 13.x.

.. important::

   F5 Networks does not back-port changes to earlier versions of Ansible.

For a detailed list of BIG-IP versions that are currently supported by F5, see |k5903|.

.. |k5903| raw:: html

   <a href="https://support.f5.com/csp/article/K5903" target="_blank">this solution article</a>

F5 follows Ansible’s model and supports the two most recent major stable releases.

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
