.. _installunstable:

Install unstable F5 Modules
===========================

When you install Ansible, it includes some F5 modules. These modules are "stable."

Other F5 modules are not yet installed when you install Ansible. These modules are "unstable."

The tutorials on this site generally use modules that are stable.

You might need to use unstable modules. For example, you may need to test something, or you just can't wait for a module to become stable.

You can install these unstable modules on your system in one of a few ways.

In a relative location (recommended)
------------------------------------

Ansible allows you to put modules in a location that is relative to the project you are working on.

To accomplish this, ensure that an `ansible.cfg` file exists in the directory that you run Ansible from.

Inside the `ansible.cfg` file, add the following code.

.. code-block:: yaml

   [defaults]
   library=./library

This code instructs Ansible to look for modules in a directory called `library` that is relative to where the `ansible.cfg` file exists.

You can take the modules in the `f5-ansible` repository and put them in that directory.

.. note::

    Specifying a `library` directory does not override the system location where Ansible searches for modules. It only tells Ansible to "look here first" when importing a module.
    Therefore, if a module in the specified `library` directory does not exist, Ansible will fall back to the system location and look for the module there.

You can also specify multiple locations by separating them with a colon. For example, if you have two different directories that have two different sets of modules in them, you might do something like this.

.. code-block:: yaml

   [defaults]
   library=./library:./unstable

In the example above, when looking for a module named `foo.py`, Ansible will follow this order:

1. `./library/foo.py`
2. `./unstable/foo.py`
3. Recursively through `/usr/local/lib/PYTHON_VERSION/site-packages/ansible/modules/`

Whichever method you choose is up to you.

In your Ansible install directory
---------------------------------

Different systems can put Ansible in different locations. The recommended way to install Ansible (via `pip`) puts the modules here:

- `/usr/local/lib/PYTHON_VERSION/site-packages/ansible/modules/extras/network/f5/`

To install the F5 modules in this repository, you can copy the contents of the `library/` directory that F5 provides into the location mentioned above.

On Mac OS X, you can use the following location for the modules:

- `/Library/Frameworks/Python.framework/Versions/[PYTHON_VERSION]/lib/python[PYTHON_VERSION]/site-packages/ansible/modules/extras/network/f5`

For example.

.. code-block:: bash

   cp library/* /usr/local/lib/PYTHON_VERSION/site-packages/ansible/modules/extras/network/f5/

This command overwrites *all* of the modules with the ones in this repository. If you want only one or two modules, then just copy those. For example:

.. code-block:: bash

   cp library/bigip_iapp_service.py /usr/local/lib/PYTHON_VERSION/site-packages/ansible/modules/extras/network/f5/

This example copies only the `bigip_iapp_service` module.

Caveats
-------

If you use method #1 and then update your Ansible installation, the update will *remove* the changes you had made to your installation.

For this reason, F5 recommends you put modules in your own personal directory and referencing that directory through your `ansible.cfg` file.
