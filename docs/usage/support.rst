Version support
===============

F5 develops the Ansible modules in tandem with the REST API, and newer versions of BIG-IP provide better support for the REST API.

F5 has tested these versions of BIG-IP with the Ansible modules:

* 12.1.0
* 12.0.0
* 11.6.0

You may need a later version, depending on the needs of the REST API.

**Note:** F5 Ansible modules are not currently supported by F5.

Get assistance
--------------

If you need help with anything related to these modules, F5 recommends that you open an issue |github_issue|.


.. |github_issue| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible/issues" target="_blank">on GitHub</a>

When communicating with F5 on the Issues page, use the GitHub user interface, rather than email.

You should not expose the name of your company when communicating an issue in a public forum.

If you need more in-depth technical assistance, you can ask us to ping you offline.

Credentials and secret things
`````````````````````````````

You should not expose credentials in a GitHub issue.

F5 *does not need any* of the following task arguments to debug your issue:

- user
- password
- server
- server_port

When you submit an issue:

- Do not provide this information (leave it empty with quotes "").
- Provide placeholders for this information (such as "admin," "secret," and "lb.mydomain.com").

F5 does not need this information to provide you with assistance.

Is a module supported?
----------------------

Remember that, ultimately, this repository contains *experimental* code.

However, with that said, there is a quick way to determine if a particular module works on a particular platform.

First, look for your modules in the *tests/* directory.

Each module has a doc block which includes a "Tested platforms" section. For example:

.. code-block:: python

   # Tested platforms:
   #
   #    - NA
   #

The above doc block tells you that F5 has not tested this particular module on any platforms, and the module is likely not complete yet.

Therefore, F5 does not recommend filing bugs against the module.

Here is another example:

.. code-block:: python

   # Tested platforms:
   #
   #    - 11.6.0
   #    - 12.0.0
   #

This module specifies the versions of BIG-IP that F5 has tested. Therefore, you can consider this module to be "complete" and ready for use.

You can file bugs against modules that are complete.
