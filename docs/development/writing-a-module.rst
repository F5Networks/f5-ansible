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

    $> ./scripts/stub-new-module.sh bigip_device_ssh

The script accepts a single argument; the name of your module.

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

Some contributors choose to put their names in there as if that implies that
they actually have a copyright over the code. For example, you might often
see something that resembles the following

.. code-block:: yaml

   # (c) 2015, John Smith

As a general rule of thumb, we frown upon that behavior. Instead, we ask
that you use the common license header and list yourself as an author.

Here is the common license header.

.. code-block:: python

   #!/usr/bin/python
   # -*- coding: utf-8 -*-
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

Following this format is done to provide consistency and to ensure that
there are never any conflicts over whose authority is implied with copyright.

If you are concerned over credit being given where it is due, do not
worry as we will address that in the next section.

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
   version_added: "2.2"
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
     password:
       description:
         - BIG-IP password
       required: true
     port:
       description:
         - Port that you want the SSH daemon to run on
       required: false
     server:
       description:
         - BIG-IP host
       required: true
     server_port:
       description:
         - BIG-IP server port
       required: false
       default: 443
     user:
       description:
         - BIG-IP username
       required: true
       aliases:
         - username
     validate_certs:
       description:
         - If C(no), SSL certificates will not be validated. This should only be
           used on personally controlled sites using self-signed certificates.
       required: false
       default: true
   notes:
     - Requires the f5-sdk Python package on the host This is as easy as pip
       install f5-sdk
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

The EXAMPLES variable
~~~~~~~~~~~~~~~~~~~~~

Our examples variable contains the most common use cases for this module.

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
         password: "admin"
         server: "bigip.localhost.localdomain"
         user: "admin"
     delegate_to: localhost

   - name: Set the banner for the SSHD service from a file
     bigip_device_sshd:
         banner: "enabled"
         banner_text: "{{ lookup('file', '/path/to/file') }}"
         password: "admin"
         server: "bigip.localhost.localdomain"
         user: "admin"
     delegate_to: localhost

   - name: Set the SSHD service to run on port 2222
     bigip_device_sshd:
         password: "admin"
         port: 2222
         server: "bigip.localhost.localdomain"
         user: "admin"
     delegate_to: localhost
   '''

This variable should be placed __after__ the ``DOCUMENTATION`` variable.

The RETURN variable
~~~~~~~~~~~~~~~~~~~

The pattern which we follow is that we always return the current state of
the module's parameters when the module has finished running.

The parameters that I am refering to here are the ones that are not considered
to be the "standard" parameters to the F5 modules.

For our module there include

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

The next section in our code is the block of code where our imports happen.

This code usually just involves importing the ``f5-sdk`` library, but may
also include imports of other libraries if you are working with legacy code.

For this module our import block is the following

.. code-block:: python

   try:
       from f5.bigip import ManagementRoot
       HAS_F5SDK = True
   except ImportError:
       HAS_F5SDK = False

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
   from ansible.module_utils.f5 import *

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

Before submiting your own module, it is recommended that your module pass
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

