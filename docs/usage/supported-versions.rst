BIG-IP versions
---------------

F5 does not currently support the F5 Modules for Ansible. However, F5 provides informal support through a number of channels. For details, see :doc:`support`.

The informal support F5 provides is for BIG-IP version 12.0.0 and later.

For a detailed list of BIG-IP versions that are currently supported, see |k5903|.

.. |k5903| raw:: html

   <a href="https://support.f5.com/csp/article/K5903" target="_blank">this solution article</a>

When a version of BIG-IP reaches end of technical support, it is supported until the next Ansible release.

For example, if a version of BIG-IP reaches end of technical support on January 1, and Ansible releases a new version on March 1, then the F5 Modules for Ansible are supported on that version of BIG-IP until March 1.

F5 does not back-port changes to earlier versions of Ansible.

F5 develops the Ansible modules in tandem with the REST API, and newer versions of BIG-IP provide better support for the REST API.

Experimental vs. production modules
-----------------------------------

F5 modules are included when you install Ansible. These modules are informally supported by F5 employees.

F5 modules are also in the |github_repo|. These modules are also informally supported by F5 employees, but you should consider these modules to be experimental and not production-ready.

However, if an experimental module's DOCUMENTATION block has a completed ``Tested platforms`` section, then the module is likely complete and ready for use. You can file issues against modules that are complete.

.. code-block:: python

   # Tested platforms:
   #
   #    - 12.0.0
   #

.. |github_repo| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible/issues" target="_blank">F5 GitHub repository</a>
