Stubbing the module fragments
=============================

At this point, you're ready to begin working in the development environment that you
downloaded, or built, earlier.

If you have not already, please run the development container now. We will work with
the ``py3.6`` container for the remainder of the tutorial.

For the general public
----------------------

For the public, you should use the following command

.. code-block:: shell

    $ docker-compose -f devtools/docker-compose.yaml run py3.6

For F5'ers
----------

F5'ers should use the following command. This assumes that you have contacted a member
of the dev team to prepare your environment.

.. code-block:: shell

    $ docker-compose -f devtools/docker-compose.yaml -f devtools/docker-compose.site.yaml run py3.6

Stubbing
--------

This tutorial recreates the ``bigip_policy_rule`` module, because it provides good examples
of the common idioms you will encounter when developing or maintaining modules.

Because this module already exists, we'll first want to remove it. The development
container provides a tool to do this. Using the ``f5ansible`` command, provide the
following arguments to delete the existing ``bigip_policy_rule`` module and its
associated stubs.

.. code-block:: bash

   $ f5ansible unstub module bigip_policy_rule

Using the ``git status`` command, you should see that there are a number of files being
reported as deleted now. This is OK. Now, we need to recreate the stubs from scratch.

There are a number of files and directories you must create to hold the various test and
validation code, in addition to the module code itself and docs.

To create the necessary directories and files automatically, use this command,

.. code-block:: shell

    $ f5ansible stub module bigip_policy_rule

When it finishes running, you will have the necessary files available to begin working
on your module.

Stubbed files
-------------

The stubber creates a number of files that you need to do some form of development on.
These files are:

* ``docs/modules/bigip_policy_rule.rst``
* ``library/bigip_policy_rule.py``
* ``test/integration/bigip_policy_rule.yaml``
* ``test/integration/targets/bigip_policy_rule/``
* ``test/unit/bigip/test_bigip_policy_rule.py``

For now we will disregard the first file there (the docs file) because we have tools at our
disposal in this container that will help us build all of those tools automatically.

With these files in place, you're ready to begin re-creating the source for the
``bigip_policy_rule`` module.

Open the ``library/bigip_policy_rule.py`` file.

Library Stub
------------

The library file is the module itself. Inside of this file is all of the work that you
will be doing to make this add LTM Policy Rule functionality to Ansible.

The ``f5ansible`` command graciously provides you with quite a starting point though.

As you scroll through the library file, take note of the names of the classes that you
encounter. Take note of the imports near the top of the file and how there are different
sets of them.

When you reach the bottom, observe how the module's execution actually occurs. The module
is written using the standard Python pattern of writing a Python module (not an Ansible
module; same words, different meaning) that can be both included and executed. In other
words, used as a library, or run as an application.

In the tutorial, you will see how the module is used in both ways. Whether it be included
in a unit test, or executed in a Playbook run.

Up next
-------

In the next section, we will see how to change one of the required areas to update; the
``DOCUMENTATION`` variable.
