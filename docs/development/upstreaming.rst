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
we prefer that you do not break any of them during development, we recognize
that sometimes that is part of the process.

.. note::

    Just because a module is incubation does not mean that it is unstable.
    Many modules remain in the incubator because there has not been sufficient
    interest from the community either internal or external to release them.

A module in incubation should have an associated Issue in Github so that
its progress can be tracked and so that others do not repeat work.

Deprecated modules
------------------

When a module has been successfully upstreamed, we do not remove it from this
repository. We do this because we want to maintain a place for the upstreamed
modules to be modified and hacked upon without concern for breaking the
stable product.

To denote that a module is deprecated though, we use the standard ansible
method of prefixing the module name with an underscore (_).

This allows you to visually know which modules are no longer, officially, a
part of this repository.

Deprecated modules remain candidates for exploration and trying new things.
If you would like to try something drastic out (that would probably not
fly with the Ansible core developers) it is recommended that you try it
here and if it seems like a good change to make, we will attempt to upstream
it as well.

Tracking upstream
^^^^^^^^^^^^^^^^^

For modules that are deprecated, there is still the possibility that patches
will be merged in upstream that we will want to reflect in the deprecated
modules.

To do this, we periodically rebase the deprecated module on to the tracked
upstream module; incorporating the changes. With this comes the addition
of continual testing and ongoing usage internally and externally to make
sure that the module works, and allows contributors to bolt on major changes
without affecting the stable module.

Qualifications for upstreaming
------------------------------

A module is considered to be in a mature state once it has met all of the
standards that have been `established for it`_.

At that point in its development, we will make the request to upstream
Ansible for the module's inclusion.

.. established for it: standards
.. Installation: install