Releases and Versioning
-----------------------

This documentation set applies to the F5 Modules for Ansible. 

F5 Modules for Ansible Compatibility
------------------------------------

The tables below show the versions used in development testing. The F5 Modules for Ansible may work with versions not shown here; F5 has not verified functionality in those versions.

.. table:: BIG-IP and BIG-IQ Controller/Platform compatibility

  +--------------------------+-----------------------+--------------------------+
  | Ansible Version          | BIG-IP version(s)     | BIG-IQ version(s)        |
  +==========================+=======================+==========================+
  | v2.5                     | v12.x, v13.x          | v5.4.x                   |
  +--------------------------+-----------------------+--------------------------+
   
.. important::

   F5 Networks does not back-port changes to earlier versions of Ansible.

F5 does not currently support the F5 Modules for Ansible. However, the community provides informal support through a number of channels. For details, see :doc:`support`.

Experimental Module Support
---------------------------

.. important::

   F5 Networks will only accept support cases for F5 modules shipped with supported versions of Ansible as noted above.

The F5 modules for Ansible are included when you install Ansible. The F5 modules for Ansible located in this project's |github_repo| are considered to be experimental and not production-ready. 

If an experimental module's DOCUMENTATION block has a completed ``Tested platforms`` section, then the module is likely complete and ready for testing. Issues against these modules can be created via `GitHub <https://github.com/F5Networks/f5-ansible/issues>`_.
