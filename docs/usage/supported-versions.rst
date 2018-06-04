Releases and Versioning
-----------------------

F5 does not currently support the F5 Modules for Ansible. However, the community provides informal support through a number of channels. For details, see :doc:`support`.


Versions
````````

The following versions are used in development testing.

The F5 Modules for Ansible may work with versions not shown here; F5 has not verified functionality in those versions.

========================== ======================= ==========================
**Ansible Version**        **BIG-IP versions**     **BIG-IQ versions**
-------------------------- ----------------------- --------------------------
v2.5                       v12.x, v13.x            v5.4.x
========================== ======================= ==========================
   
.. important::

   F5 Networks does not back-port changes to earlier versions of Ansible.



Experimental Module Support
```````````````````````````

F5 Networks accepts support cases for F5 modules that have shipped with supported versions of Ansible. See the preceding table for details.

The F5 Modules for Ansible are included when you install Ansible. The F5 Modules for Ansible located in this project's |github_repo| are considered to be experimental and not production-ready.

If an experimental module's DOCUMENTATION block has a completed ``Tested platforms`` section, then the module is likely complete and ready for testing. You can create issues for these modules `here <https://github.com/F5Networks/f5-ansible/issues>`_.


.. |github_repo| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible" target="_blank">GitHub repo</a>
