Upstreaming
===========

Upstreaming refers to opening a PR with the Ansible core product.

F5's goal with this repository is to serve as an incubator for modules to mature. Eventually, the modules in this repository should find their way to the upstream Ansible product (core or extras).

Experimental modules
--------------------

Experimental modules follow the same naming convention as those in the Ansible product. Experimental modules are easy to distinguish, because their filenames do **not** include a leading underscore.

You can obtain experimental modules by using the installation steps outlined here: :ref:`installunstable`.

An experimental module may or may not work at any point in time.

.. note::

   Just because a module is experimental does not mean that it is unstable. Many modules remain in the incubator because the community has not expressed enough interest in them.

An experimental module should have an associated Issue in Github so everyone can track the module's progress and so that others do not repeat work.

Qualifications for upstreaming
------------------------------

A module is in a mature state after it has met all of the established standards.

- http://docs.ansible.com/ansible/dev_guide/testing.html
- :doc:`code-conventions`

When the module meets these requirements, F5 will request Ansible to include the module.

Ansible releases
----------------

After F5 upstreams a module, a period of time will pass before it becomes part of the core Ansible product.

That release schedule is in the `ROADMAP files` near the top of each file.

Depending on which version is currently stable, upstreamed modules will be part of the next major stable release.

For example, if 2.3 is the current stable version and F5 upstreamed a module to core, the module would not appear as part of `pip install ansible` until version 2.4 releases.

You can get the modules before that point in time, but you must do so manually. The link to the |stable_modules|.

How to upstream a module
------------------------

A summary of the upstreaming process is below. Only one person needs to know how to upstream modules.

Complete GitHub template
------------------------

Ansible provides an Issue template that you receive when you create a new PR in GitHub. You should fill out the various fields, making sure to include the following information in the "Summary", "Description", or related fields.

Here is an example:

.. code-block:: python

   PR Title:
   Adds the bigip_user module to Ansible

   Summary:
   This patch adds the bigip_user module to Ansible to support managing
   users on an F5 BIG-IP.

   Additional Info:
   Unit tests provided. Integration tests are here:

   * https://github.com/F5Networks/f5-ansible/blob/devel/test/integration/bigip_user.yaml
   * https://github.com/F5Networks/f5-ansible/tree/devel/test/integration/targets/bigip_user/tasks

When you include this extra information, it shows your due diligence in writing and testing the module. It helps assure the Ansible maintainers, and F5 customers, that you wrote the code well.

Attend the upstream meeting
---------------------------

Generally speaking, the upstreaming window is open each week, around the times of the Networking meeting. Here is the Networking team's schedule.

- https://github.com/ansible/community/blob/master/MEETINGS.md#wednesdays

During that time, you must comment on the Ansible Networking Group's issue tracker for new PRs, which is here:

- https://github.com/ansible/community/issues/110

The Networking team will address your PRs at their weekly meeting, which Ansible expects you to attend.

The meeting is on IRC at the below location:

* Server: irc.freenode.net
* Channel: #ansible-devel

.. ROADMAP files: https://github.com/ansible/ansible/tree/devel/docs/docsite/rst/roadmap
.. upstreaming requirements: https://github.com/F5Networks/f5-ansible/blob/devel/.github/UPSTREAM_TEMPLATE.md
.. coding conventions: coding-conventions.rst
.. Installation: install


.. |stable_modules| raw:: html

   <a href="https://github.com/ansible/ansible/tree/devel/lib/ansible/modules/network/f5" target="_blank">stable modules is here</a>

