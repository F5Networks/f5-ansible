BIG-IP versions
---------------

F5 does not currently support the F5 Modules for Ansible. However, the community provides informal support through a number of channels. For details, see :doc:`support`.

Use the F5 modules with BIG-IP version 12.0.0 and later, and BIG-IQ 5.4.0 and later.

F5 develops the Ansible modules in tandem with the REST API, and newer versions of BIG-IP provide better support for the REST API.

F5 does not back-port changes to earlier versions of Ansible.


Experimental vs. production modules
-----------------------------------

F5 modules are included when you install Ansible.

F5 modules are also in the |github_repo|. You should consider these modules to be experimental and not production-ready.

However, if an experimental module's DOCUMENTATION block has a completed ``Tested platforms`` section, then the module is likely complete and ready for use. You can file issues against modules that are complete.

.. code-block:: python

   # Tested platforms:
   #
   #    - 12.0.0
   #

.. |github_repo| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible/issues" target="_blank">F5 GitHub repository</a>
