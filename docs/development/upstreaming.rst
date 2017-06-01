Upstreaming
===========

Upstreaming refers to opening a PR with the Ansible core product.

Our goal with this repository is to serve as an incubator for modules to
mature. Eventually, we hope that the modules here will find their way to
the upstream Ansible product (core or extras).

Incubating modules
------------------

Modules that are currently in incubation are named as normal modules are
that you would find in the Ansible product. They are easily distinguished
by their filename **not** including a leading underscore.

These modules can only be obtained through the installation steps outlined
in the `Installation`_ docs.

An incubating module may or may not be working at any point in time. While
we prefer to not break any of them during development, we recognize
that sometimes that is part of the process.

.. note::

    Just because a module is incubation does not mean that it is unstable.
    Many modules remain in the incubator because there has not been sufficient
    interest from the community either internal or external to release them.

A module in incubation should have an associated Issue in Github so that
its progress can be tracked and so that others do not repeat work.

Qualifications for upstreaming
------------------------------

A module is considered to be in a mature state once it has met all of the
standards that have been established for it.

* http://docs.ansible.com/ansible/dev_guide/testing.html
* `upstreaming requirements`_
* `coding conventions`_

At that point in its development, we will make the request to upstream
Ansible for the module's inclusion.

Releases
--------

After a module is upstreamed, there will continue to be a period of time
that must pass before it is released as part of the core Ansible product.

That release schedule is shown in the `ROADMAP files` near the top of
each file.

Depending on what version is currently stable, upstreamed modules will be
part of the next major stable release.

For example.

If 2.3 is the current stable version and a module was upstreamed to core,
it would not appear as part of `pip install ansible` until version 2.4
was released.

You can get the modules before that point in time, but you must do so
manually. The link to the `stable modules is here`_.

Upstreaming Process
===================

The upstreaming process is summarized below. Only one person should be concerned
with upstreaming things.

Upstream Github template
------------------------

Ansible provides an Issue template that will be shown to you automatically
when you create a new PR in Github. You should fill out the various fields in
it, making sure to include the following in one of the "Summary", "Description",
or related fields.

Below is an example of what has been provided in the past and you should use it
as an example of what you too should provide.

.. raw::

   PR Title:
   Adds the bigip_user module to Ansible

   Summary:
   This patch adds the bigip_user module to Ansible to support managing
   users on an F5 BIG-IP.

   Additional Info:
   Unit tests are provided. Integration tests can be found here

   * https://github.com/F5Networks/f5-ansible/blob/devel/test/integration/bigip_user.yaml
   * https://github.com/F5Networks/f5-ansible/tree/devel/test/integration/targets/bigip_user/tasks

Including the extra information that shows your due diligence in writing and
testing the module is important because it helps ensure the Ansible maintainers,
and our customers, that the code has been written well.

Upstream Window
---------------

Generally speaking the upstreaming window is open each one week around the times
of the Networking meeting. Here is the Networking team's schedule.

* https://github.com/ansible/community/blob/master/MEETINGS.md#wednesdays

During that time, you will need to comment on the Ansible Networking Groups
issue tracker for new PRs. This can be found here.

* https://github.com/ansible/community/issues/110

Upstream Meeting
----------------

The Networking team will address your PRs at their weekly meeting, which you are
expected to attend.

The meeting can be found on IRC at the below location

* Server: irc.freenode.net
* Channel: #ansible-devel

.. ROADMAP files: https://github.com/ansible/ansible/tree/devel/docs/docsite/rst/roadmap
.. upstreaming requirements: https://github.com/F5Networks/f5-ansible/blob/devel/.github/UPSTREAM_TEMPLATE.md
.. coding conventions: coding-conventions.rst
.. Installation: install
.. stable modules is here: https://github.com/ansible/ansible/tree/devel/lib/ansible/modules/network/f5
