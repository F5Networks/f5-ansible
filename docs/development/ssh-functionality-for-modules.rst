SSH functionality for modules
=============================

A requested feature of the F5 modules has been the ability to use SSH to configure them.

I looked into this possibility and after discussing with Michael about it, it was
suggested that to retain the ability to parse structured output (ie, the REST output)
that we should try to use local `curl` commands to the same APIs and that we would
therefore get the same results which we could sent to our existing `Parameter` classes.

This sounded goo, but it has some deficiencies that a user needs to be aware of before
they can make use of it.

Limited role usage
------------------

By far the largest limitation is that there are only two roles who are actually able
to use the "Advanced shell" also known as "bash".

* Administrator
* Resource Administrator

All other roles are limited to the `tmsh` shell only. This results in two problems.

First, since you are in tmsh, you do not natively have a `curl` command that you can
use. Normally you would be able to use `curl` because it is installed and is a standard
feature of the system. However, you do not have a `curl` command that can be run
from, for example `tmsh run util...`

This first problem can actually be worked around if you have one of the two roles
mention above, associated with your account.

If you have either role, you can make use of curl through the `tmsh run util bash`
command.

Appliance mode
--------------

This restriction is where things get really hairy.

Appliance mode's restrictions are outlined in this support article.

* https://support.f5.com/csp/article/K12815

I will reiterate some of those restrictions below.

* Access to the Advanced shell (bash) has been removed.
* Administrative access is limited to the Configuration utility, bigpipe shell (bpsh),
  and Traffic Management Shell (tmsh)
* The root user cannot log in to the device by any means, including the serial console.
* To disable Appliance mode, you must contact F5 for assistance in removing Appliance
  mode from your license file and then perform a clean installation of the software.

The above restrictions essentially make it exceedingly difficult to configure the
device using an API that provides structured data. Additionally, it may make some
actions that we take in the modules completely impossible such as uploading file
data which would appear to require SCP functionality in the case of Appliance Mode.

As it stands, the above requirements would mean that we would need to rely on tmsh
itself to accomplish anything. This means working with a tool that does not provide
structured output; only free form output.

Indeed there is a `--oneline` argument that may be supplied to `tmsh` commands, but
it is not clear to the author how parseable, or reliable, this format is.

Conclusion
----------

For the above reasons, if CLI functionality is pursued for any of these modules, it
is my recommendation that the functionality only be allowed for users who are of
one of the following roles,

* Administrator
* Resource Administrator

Note that it is not required that the user of the modules need worry about which
partitions they are allowed to access. With these roles you can access **all** of
them.

Without making this a requirement, it may not be possible to provide a user of the
modules with a reliable way to configure the system due to restrictions that are
put in place by other roles.
