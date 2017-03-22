Writing a Module
================

Let's explore what it takes to write a module using the provided guidelines
and standards.

Getting Started
---------------

The first step is to decide what you will call your module. For this tutorial
we will recreate the functionality of the ``bigip_device_sshd`` module as it
provides good examples of the common idioms you will encounter when developing
or maintaining modules.

Because this module already exists, let's just slightly change the name of
our module to the following

  ``bigip_device_ssh``

This name will additionally prevent you from tab'ing to the existing sshd
module.

Create the directory layout
---------------------------

There are a number of files and directories that need to be created to hold
the various tests and validation code in addition to just your module.

To create the necessary directories and files, an executable file is
available for you to use to set these directories up automatically.

.. code-block:: shell

    $> ./scripts/stub-new-module.py stub --module=bigip_device_ssh

When it finishes running, you will have the necessary files available to
begin working on your module.

The module file
---------------

The module file that gets created is located here

  ``library/bigip_device_ssh.py

Let's open that file to get started

License header
~~~~~~~~~~~~~~

The first things you you will put in the file is the license header.

Here is the common license header.

.. code-block:: python

   #!/usr/bin/python
   # -*- coding: utf-8 -*-
   #
   # Copyright 2016 F5 Networks Inc.
   #
   # This file is part of Ansible
   #
   # Ansible is free software: you can redistribute it and/or modify
   # it under the terms of the GNU General Public License as published by
   # the Free Software Foundation, either version 3 of the License, or
   # (at your option) any later version.
   #
   # Ansible is distributed in the hope that it will be useful,
   # but WITHOUT ANY WARRANTY; without even the implied warranty of
   # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   # GNU General Public License for more details.
   #
   # You should have received a copy of the GNU General Public License
   # along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

If the module under development is your original work, then you can
include your name in the copyright above.

If you are only contributing an existing module, then it is not necessary
to include a copyright line at the top. Instead, accepting our CLA is
sufficient to get code merged into our branch.

The ANSIBLE_METADATA variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This variable should be included first in your module. It specifies
metadata for the module itself. It can always look the same. Here is
it as would be defined in code.

.. code-block:: python


   ANSIBLE_METADATA = {'status': ['preview'],
                       'supported_by': 'community',
                       'version': '1.0'}

After the metadata variable comes the `DOCUMENTATION` variable.

The DOCUMENTATION variable
~~~~~~~~~~~~~~~~~~~~~~~~~~

The next chunk of code that you will insert describes the module, what
parameters is accepts, who the authors/maintainers are, its dependencies,
etc.

Let's look at the code that we will add to our module.

.. code-block:: python

   DOCUMENTATION = '''
   ---
   module: bigip_device_sshd
   short_description: Manage the SSHD settings of a BIG-IP
   description:
     - Manage the SSHD settings of a BIG-IP
   version_added: "2.4"
   options:
     banner:
       description:
         - Whether to enable the banner or not
       required: false
       choices:
         - enabled
         - disabled
     banner_text:
       description:
         - Specifies the text to include on the pre-login banner that displays
           when a user attempts to login to the system using SSH
       required: false
     inactivity_timeout:
       description:
         - Specifies the number of seconds before inactivity causes an SSH
           session to log out
       required: false
     log_level:
       description:
         - Specifies the minimum SSHD message level to include in the system log
       choices:
         - debug
         - debug1
         - debug2
         - debug3
         - error
         - fatal
         - info
         - quiet
         - verbose
     login:
       description:
         - Specifies, when checked C(enabled), that the system accepts SSH
           communications
       required: false
     port:
       description:
         - Port that you want the SSH daemon to run on
       required: false
   notes:
     - Requires the f5-sdk Python package on the host This is as easy as pip
       install f5-sdk
   extends_documentation_fragment: f5
   requirements:
     - f5-sdk
   author:
     - Tim Rupp (@caphrim007)
   '''

Most documentation variables have a common set of keys and only differ in the
values of those keys.

The keys that one commonly finds are

  * ``module``
  * ``short_description``
  * ``description``
  * ``version_added``
  * ``options``
  * ``notes``
  * ``requirements``
  * ``author``
  * ``extends_documentation_fragment``

.. note::

    The `extends_documentation_fragment` key is special as it is what will
    automatically inject the variables `user`, `password`, `server`,
    `server_port` and `validate_certs` into your documentation. It should
    be used for all modules.

The EXAMPLES variable
~~~~~~~~~~~~~~~~~~~~~

The examples variable contains the most common use cases for this module.

I personally think that setting of the banner will be the most common case,
but future authors are free to add to my examples.

These examples will also serve as a basis for the functional tests that we
will write shortly.

For this module, our ``EXAMPLES`` variable looks like this.

.. code-block:: python

   EXAMPLES = '''
   - name: Set the banner for the SSHD service from a string
     bigip_device_sshd:
         banner: "enabled"
         banner_text: "banner text goes here"
         password: "secret"
         server: "lb.mydomain.com"
         user: "admin"
     delegate_to: localhost

   - name: Set the banner for the SSHD service from a file
     bigip_device_sshd:
         banner: "enabled"
         banner_text: "{{ lookup('file', '/path/to/file') }}"
         password: "secret"
         server: "lb.mydomain.com"
         user: "admin"
     delegate_to: localhost

   - name: Set the SSHD service to run on port 2222
     bigip_device_sshd:
         password: "secret"
         port: 2222
         server: "lb.mydomain.com"
         user: "admin"
     delegate_to: localhost
   '''

This variable should be placed __after__ the ``DOCUMENTATION`` variable.

The examples that you provide should always have the following

**delegate_to: localhost**

The BIG-IP modules are intended to run on the Ansible controller only. The
best practice is to use this `delegate_to:` here so that users get in the
habit of using it

**common args**

The common args as as follow

  * `password` should always be set to `secret`
  * `server` should always be set to `lb.mydomain.com`
  * `user` should always be set to `admin`

The RETURN variable
~~~~~~~~~~~~~~~~~~~

The pattern which we follow is that we always return what changed in the
module's parameters when the module has finished running.

The parameters that I am referring to here are the ones that are not considered
to be the "standard" parameters to the F5 modules. Some exceptions to this rule
apply. For example, where the `state` variable contains more states than just
`absent` and `present`, such as in the `bigip_virtual_server` module.

For our module these include,

  * ``banner``
  * ``banner_text``
  * ``inactivity_timeout``
  * ``log_level``
  * ``login``

The ``RETURN`` variable describes these values, specifies when they are
returned and provides examples of what the values returned might look like.

When the Ansible module documentation is generated, these values are presented
in the form of a table. Here is the RETURN variable that we would place in
our module file.

The import block
~~~~~~~~~~~~~~~~

The next section in our code is the block of code where our `import`s happen.

This code usually just involves importing the `module_util` helper library, but
may also include imports of other libraries if you are working with legacy code.

For this module our import block is the following

.. code-block:: python

   from ansible.module_utils.f5_utils import *

Module class
~~~~~~~~~~~~

The next block of code is the skeleton for our module's class. We encapsulate
all of our module's code inside a class for easy testing as well as for code
re-use outside of this module.

For example, there are cases where third-parties want to re-use this code
outside of Ansible.

The module class is where the specifics of your code will be. There are,
however, a number of commonalities across all modules. The code outlined
below includes those commonalities and leaves the implementation details
specific to the module to your interpretation.

.. code-block:: python

   class BigIpDeviceSshd(object):
       def __init__(self, *args, **kwargs):
           if not HAS_F5SDK:
               raise F5ModuleError("The python f5-sdk module is required")

           self.params = kwargs
           self.api = ManagementRoot(kwargs['server'],
                                     kwargs['user'],
                                     kwargs['password'],
                                     port=kwargs['server_port'])

       def present(self):
           pass

       def absent(self):
           pass

       def update(self):
           pass

       def read(self):
           pass

       def flush(self):
           pass

For modules where settings are actively added or removed from the system,
the modules **must** provide ``present`` and ``absent`` methods respectively.

Additionally, modules usually include an ``update`` method for those cases
where ``present`` is being performed, but the value already exists and only
an attribute of the setting is being changed.

The ``flush`` method exists to encapsulate the running of the ``absent``,
``present``, and ``update`` modules and should include the appropriate
checks of the ``state`` parameter to decide which method to call.

For the implementation specifics, you can refer to the existing module.

Connecting to Ansible
---------------------

With the implementation details of the module complete, we move on to
the code that hooks the module up to Ansible itself.

The main function
~~~~~~~~~~~~~~~~~

This code begins with the definition of the ``main`` function.

This code should be placed __after__ the definition of your class which
you wrote earlier. Here is how we begin.

.. code-block:: python

   def main():

Argument spec and instantiation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next, we generate the common argument spec using a utility method of Ansible.

.. code-block:: python

   argument_spec = f5_argument_spec()

With the ``argument_spec`` generated, we update the values in it to match
the ``options`` we declared in our ``DOCUMENTATION`` variable earlier.

The values that you must specify here are, again, the ones that are **not**
common to all F5 modules. Below is the code we need to update our
``argument_spec``

.. code-block:: python

   meta_args = dict(
       allow=dict(required=False, default=None),
       banner=dict(required=False, default=None, choices=CHOICES),
       banner_text=dict(required=False, default=None),
       inactivity_timeout=dict(required=False, default=None, type='int'),
       log_level=dict(required=False, default=None, choices=LEVELS),
       login=dict(required=False, default=None, choices=CHOICES),
       port=dict(required=False, default=None, type='int')
   )
   argument_spec.update(meta_args)

After the ``argument_spec`` has been updated, we instantiate an instance
of our class, providing the ``argument_spec`` and the value that indicates
we support Check mode.

.. code-block:: python

   module = AnsibleModule(
       argument_spec=argument_spec,
       supports_check_mode=True
   )

All F5 modules **must** support Check Mode as it allows an administrator to
determine whether a change will be made or not when the module is run
against their devices.

Try and module execution
~~~~~~~~~~~~~~~~~~~~~~~~

The next block of code that is added is a general execution of your class.

We wrap this execution inside of a try...except statement to ensure that
we handle know errors and bubble up known errors.

Never include a general Exception handler here because it will hide the
details of an unknown exception that we require when debugging an unhandled
exception.

.. code-block:: python

   try:
       obj = BigIpDeviceSshd(check_mode=module.check_mode, **module.params)
       result = obj.flush()

       module.exit_json(**result)
   except F5ModuleError as e:
       module.fail_json(msg=str(e))

Common imports
~~~~~~~~~~~~~~

The following imports are common to all of the F5 modules. The ``f5`` import
provides you with the helper functions that create the ``argument_spec``.

The ``basic`` import is replaced by Ansible itself and provides helper
functions and classes used to create the ``Module`` object (among other
things).

.. code-block:: python

   from ansible.module_utils.basic import *
   from ansible.module_utils.f5_utils import *

Common running
~~~~~~~~~~~~~~

The final two lines in your module inform Python to execute the module's
code if the script being run is itself executable.

.. code-block:: python

   if __name__ == '__main__':
       main()

Due to the way that Ansible works, this means that the ``main`` function
will be called when the module is sent to the remote device (or run locally)
but will not be called if the module is imported.

You would import the module if you were using it outside of Ansible, or
in some sort of test environment where you do not want the module to
actually run.

Testing
-------

Providing tests with your module is a crucial step for having it merged and
subsequently pushed upstream. We rely heavily on testing.

In this section I will go in to detail on how our tests are organized and
how you can write your own to ensure that your modules works as designed.

flake8
~~~~~~

We make use of the ``flake8`` command to ensure that our modules meet certain
coding standards and compatibility across Python releases.

You can run the flake8 tests via the ``make`` command

.. code-block:: bash

   make flake8

Before submitting your own module, it is recommended that your module pass
the `flake8` tests we ship with the repository. We will ask you to update
your code to meet these requirements if it does not.

Functional tests
~~~~~~~~~~~~~~~~

This is probably the most important part of testing, so let's go in to
detail on this part.

Functional tests are required during module submission so that we (F5)
and you, the developer, can agree that a module works on a particular
platform.

We will test your module on a variety of platforms automatically when
a new PR is submitted, and from there provide feedback if something does
not fly.

Structure of tests
^^^^^^^^^^^^^^^^^^

Test file stubs are created for you automatically when you stub a new
module.

To best show you how testing works, we will reference an existing module
that provides complete tests; `bigip_device_sshd`.

First, let's look at the layout of a set of tests. A test is composed of
a role whose name matches the name of the module that is being tested.

This role is placed in the `roles/` directory.

So, for our example, our test role looks like this.

   * `roles/bigip_device_sshd/`

Inside of this role is everything that you would associate with a normal
role in ansible.

Consider the following examples.

  * if your test requires static files be used, then a `files/` directory
    should be in your role.
  * if your test requires template data (for example iRules) for its
    input, then a `templates/` directory should be in your role.
  * all roles will perform some work to test the module, so a `tasks/`
    directory should be in your role.

Now let's dig in to what a test should look like.

Test content
------------

The test itself will follow the pattern below.

  - perform some operation with the module
  - assert a value

All of the tests work like this, and it is a decent smoke test for all modules
until such time as we take the testing further.

Here is an example of a test from the `bigip_device_sshd` module.

.. code-block:: yaml

   ---

   - name: Set the SSHD allow string to a specific IP
     bigip_device_sshd:
         allow:
             - "{{ allow[0] }}"
         user: "{{ bigip_username }}"
         password: "{{ bigip_password }}"
         server: "{{ inventory_hostname }}"
         server_port: "{{ bigip_port }}"
         validate_certs: "no"
     register: result

   - name: Assert Set the SSHD allow string to a specific IP
     assert:
         that:
             - result|changed

As you can see, pretty straightforward.

We use the module and then we check that the result we `register` was
changed.

Test variables
--------------

All of the tests have access to the following variables by default.

  * `{{ bigip_password }}`
  * `{{ bigip_port }}`
  * `{{ bigip_username }}`
  * `{{ inventory_hostname }}`

All other information specific to the tests that you need to run should be
put in the `defaults/main.yaml` file of your test role.

By putting them there, you allow individuals to override values in your test
by providing arguments to the CLI at runtime.

The idempotent test
-------------------

All tests that change data should also include a test right after it that
tries to perform the same test, but whose result is expected to *not* change.

These are called idempotent tests because they ensure that the module only
changes settings if the setting needs to be changed.

Here is an example of the previous test as an idempotent test

.. code-block:: yaml

   - name: Set the SSHD allow string to a specific IP - Idempotent check
     bigip_device_sshd:
         allow:
             - "{{ allow[0] }}"
         user: "{{ bigip_username }}"
         password: "{{ bigip_password }}"
         server: "{{ inventory_hostname }}"
         server_port: "{{ bigip_port }}"
         validate_certs: "no"
     register: result

   - name: Assert Set the SSHD allow string to a specific IP - Idempotent check
     assert:
         that:
             - not result|changed

There are two things to note here.

First, the test code itself is identical to the previous test.

Second, note that we changed the name of the test to include the string
``"- Idempotent check"`. This gives reviewers the ability to visually note
that this is an idempotent test.

Third, note that in our assertion, we are check that the result has *not*
changed. This is the important part because it is what ensures that the
test itself was idempotent.

Now lets look at how you call the test.

Calling the test
----------------

To call the test and run it, this repo includes a `make` command that is
available for all modules. The name of the make target is the name of your
module.

So, for our example, that `make` command would be.

  * make bigip_device_ssh

This command will run the module functional tests for you in debug mode.

Including supplementary information
-----------------------------------

If you include files inside of the `files/`, `templates`, or other directories
in which the content of that file was auto-generated or pulled from a third
party source, you should include a `README.md` file in your role's directory.

Inside of this file, you can include steps to reproduce any of the input
items that you include in the role subdirectories.

In addition, this place is also a good location to include references to third
party file locations if you have included them in the tests. For example, if
you were to include iRules or other things that you downloaded and included
from DevCentral or similar.

The `README.md` is there for future developers to reference the information
needed to re-create any of the inputs to your tests in case they need to.

Other testing notes
-------------------

When writing your tests, there is no need to be concerned about "undoing"
what you previously have done to the test environment.

Between the running of the tests, we destroy the VMs that ran the test
so for each running of the test you can assume a pristine environment.
