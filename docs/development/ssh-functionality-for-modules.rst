Using SSH to configure the modules
==================================

Users have requested the ability to use SSH to configure the F5 Modules for Ansible.

To get the same results as the existing ``Parameter`` classes, you can try to use local ``curl`` commands to parse the REST output.

Before you use this method, note the following limitations.

Limited role usage
------------------

Only two roles can use the "Advanced shell," also known as "bash."

- Administrator
- Resource Administrator

If you have either role, you can use ``curl`` through the ``tmsh run util bash`` command.

All other roles are limited to the ``tmsh`` shell only. In ``tmsh``, you do not natively have a ``curl`` command you can use.

Appliance mode
--------------

Appliance mode's restrictions are outlined in this support article:

- https://support.f5.com/csp/article/K12815

Some of the restrictions are:

- Access to the Advanced shell (``bash``) has been removed.
- Administrative access is limited to the Configuration utility, bigpipe shell (``bpsh``), and Traffic Management Shell (``tmsh``).
- The root user cannot log in to the device by any means, including the serial console.
- To disable Appliance mode, you must contact F5 to help remove Appliance mode from your license file and then perform a clean installation of the software.

These restrictions make it difficult to configure the device by using an API that provides structured data.

In addition, some of the actions the modules take become impossible. For example, in Appliance Mode, you cannot upload file data that would require SCP functionality.

As it stands, these requirements mean that you would need to rely on ``tmsh`` itself to accomplish your tasks.

This means working with a tool that provides free-form output, rather than structured output.

A ``--oneline`` argument exists that may be supplied to ``tmsh`` commands, but it is not clear how parseable, or reliable, this format is.

Conclusion
----------

For the above reasons, if you pursue CLI functionality for any of these modules, F5 recommends that the functionality
be allowed for users with one of the following roles only:

- Administrator
- Resource Administrator

These roles can access **all** modules.

Without making this a requirement, it may not be possible to provide you with a reliable way to configure the system,
due to restrictions put in place by other roles.
