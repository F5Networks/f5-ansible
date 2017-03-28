Installing Modules
==================

Some of the modules in this repository come with Ansible out of the box. Those
modules are considered "stable".

There are other modules in this repository that do not yet come with Ansible out
of the box. Thos modules are considered "unstable".

In the tutorials on this site, we generally use only modules that are stable.

There is a chance, however, that you might need to use unstable modules though.
In particular, you'll encounter this if you need to test something or if you
just can't wait for a module to become stable.

There are a couple ways to install these modules on your system.

In your Ansible install directory
---------------------------------

Different systems can put Ansible in different locations. The recommended way
to install Ansible however (via `pip`) puts the modules here

  * /usr/local/lib/PYTHON_VERSION/site-packages/ansible/modules/extras/network/f5/

To install the F5 modules in this repository, you can copy the contents of
the `library/` directory we provide, into the location mentioned above.

on MacOSX, the following location can be used for the modules:
  * /Library/Frameworks/Python.framework/Versions/[PYTHON_VERSION]/lib/python[PYTHON_VERSION]/site-packages/ansible/modules/extras/network/f5

In a relative location
----------------------

Ansible also allows you to put modules in a location that is relative to where
the project you are working on is.

This is accomplished by ensuring that an `ansible.cfg` file exists in the
directory that you run Ansible from.

Inside the `ansible.cfg` file, you can put the following

.. code-block:: yaml

   [defaults]
   library=./library

This will instruct Ansible to look for modules in a directory called `library`
that can be found relative to where the `ansible.cfg` file exists.

So, again, you can take the modules in the `f5-ansible` repository and put
them in a directory that you specify and that will also work.

.. note::

    Specifying a `library` directory does not override the system location
    where Ansible searches for modules. It only tells ansible to "look here
    first" when importing a module. Therefore, if a module in the specified
    `library` directory does not exist, Ansible will fallback to the system
    location and look for the module there.
