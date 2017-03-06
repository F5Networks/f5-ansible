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
standards that have been `established for it`_.

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

.. ROADMAP files: https://github.com/ansible/ansible/tree/devel/docs/docsite/rst/roadmap
.. established for it: standards
.. Installation: install
.. stable modules is here: https://github.com/ansible/ansible/tree/devel/lib/ansible/modules/network/f5
