BIG-IP Versions
---------------

There are a number of versions of software that F5 officially supports. For the full list, see |bigip_support|.

This should not be considered the list that the Ansible modules support though.

We're doing our best to move more towards using the REST API, so with that in mind, we're also moving many of the Ansible modules along in terms of supported BIG-IP versions.

Generally speaking, the versions of BIG-IP that are tested and supported by the Ansible modules include:

* 11.6.0
* 12.0.0
* 12.1.0

So that the oldest that we're willing to aim for is when the REST interface went GA.

If you're seriously interested in the Ansible modules, then consider it a reason to upgrade if you have not yet done so.


.. |bigip_support| raw:: html

   <a href="https://support.f5.com/csp/article/K5903" target="_blank">this webpage</a>
