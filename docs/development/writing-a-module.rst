Writing a module
================

The following tutorial explains how to create a module.

Give the module a name
----------------------

The first step is to decide what to call your module. This tutorial recreates the ``bigip_device_sshd`` module, because it provides good examples of the common idioms you will encounter when developing or maintaining modules.

Because this module already exists, change the name of the module to the following:

``bigip_device_ssh``

This name will prevent you from tabbing to the existing sshd module.

Create the directory layout
---------------------------

In addition to your module, there are a number of files and directories you must create to hold the various test and validation code.

To create the necessary directories and files automatically, use this executable file:

.. code-block:: shell

    $> ./devtools/bin/stubber.py --module MODULE_NAME stub

When it finishes running, you will have the necessary files available to begin working on your module.

Stub files
----------

The stubber creates a number of files that you need to do some form of development on. These files are:

* ``docs/modules/MODULE_NAME.rst``
* ``library/MODULE_NAME.py``
* ``test/integration/MODULE_NAME.yaml``
* ``test/integration/targets/MODULE_NAME/``
* ``test/unit/bigip/test_MODULE_NAME.py``

DOCUMENTATION variable
``````````````````````

The next chunk of code that you will insert describes the module, which parameter it accepts, who the authors/maintainers are, its dependencies, etc.

Here is an example of the code you will add to your module.

.. code-block:: python

   DOCUMENTATION = '''
   ---
   module: bigip_device_sshd
   short_description: Manage the SSHD settings of a BIG-IP
   description:
     - Manage the SSHD settings of a BIG-IP
   version_added: "2.5"
   options:
     banner:
       description:
         - Whether to enable the banner or not
       choices:
         - enabled
         - disabled
     banner_text:
       description:
         - Specifies the text to include on the pre-login banner that displays
           when a user attempts to login to the system using SSH
     inactivity_timeout:
       description:
         - Specifies the number of seconds before inactivity causes an SSH
           session to log out
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
     port:
       description:
         - Port that you want the SSH daemon to run on
   notes:
     - Requires the f5-sdk Python package on the host This is as easy as pip
       install f5-sdk
   extends_documentation_fragment: f5
   requirements:
     - f5-sdk
   author:
     - Tim Rupp (@caphrim007)
   '''

Most documentation variables have a common set of keys and only differ in the values of those keys.

Commonly-used keys are:

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

   The `extends_documentation_fragment` key is special as it automatically injects the variables `user`, `password`, `server`, `server_port`, and `validate_certs` into your documentation. You should use it for all modules.

Additionally, note that Ansible upstream has several rules for their documentation blocks. At the time of this writing, the rules include:

- If a parameter is *not* required, **do not** include a `required: false` field in the parameter's `DOCUMENTATION` section.

EXAMPLES variable
`````````````````

The EXAMPLES variable contains the most common use cases for this module.

Setting the banner is the most common case, but you are free to add to these examples.

These examples also serve as a basis for the functional tests.

For this module, the ``EXAMPLES`` variable looks like this:

.. code-block:: python

   EXAMPLES = '''
   - name: Set the banner for the SSHD service from a string
     bigip_device_sshd:
       banner: enabled
       banner_text: banner text goes here
       password: secret
       server: lb.mydomain.com
       user: admin
     delegate_to: localhost

   - name: Set the banner for the SSHD service from a file
     bigip_device_sshd:
       banner: enabled
       banner_text: "{{ lookup('file', '/path/to/file') }}"
       password: secret
       server: lb.mydomain.com
       user: admin
     delegate_to: localhost

   - name: Set the SSHD service to run on port 2222
     bigip_device_sshd:
       password: secret
       port: 2222
       server: lb.mydomain.com
       user: admin
     delegate_to: localhost
   '''

This variable should go **after** the ``DOCUMENTATION`` variable.

The examples that you provide should always have the following:

**delegate_to: localhost**

You should run the BIG-IP modules on the Ansible controller only. The best practice is to use `delegate_to:` here so that you get in the habit of using it.

**common args**

The common args are:

- `password` should always be `secret`
- `server` should always be `lb.mydomain.com`
- `user` should always be `admin`

RETURN variable
```````````````

When a module finishes running, F5 always uses the module's parameters to return the changes.

Some exceptions to this rule apply. For example, where the `state` variable contains more states than just `absent` and `present`, such as in the `bigip_virtual_server` module.

For the sample module, these values include:

- ``banner``
- ``banner_text``
- ``inactivity_timeout``
- ``log_level``
- ``login``

The ``RETURN`` variable describes these values, specifies when they're returned, and provides examples of what the values returned might look like.

When the Ansible module documentation generates, these values are output in a table.

The import block
````````````````

The next section is the block of code where the imports happen.

This code usually just involves importing the ``module_util`` helper libraries, but may also include imports of other libraries if you are working with legacy code.

For this module, the import block is:

.. code-block:: python

   from ansible.module_utils.f5_utils import AnsibleF5Client
   from ansible.module_utils.f5_utils import AnsibleF5Parameters
   from ansible.module_utils.f5_utils import HAS_F5SDK
   from ansible.module_utils.f5_utils import F5ModuleError
   from ansible.module_utils.f5_utils import iteritems
   from ansible.module_utils.f5_utils import defaultdict

   try:
       from ansible.module_utils.f5_utils import iControlUnexpectedHTTPError
   except ImportError:
       HAS_F5SDK = False

In 90% of cases, this code is boilerplate and you can ignore it when writing a module. `stubber.py` takes care of this for you.

ModuleManager class
```````````````````

The next block of code is the skeleton for the module's `Manager` class. Most of the module's steering code is inside this class. It acts as the traffic cop, determining which path the module should take to reach the desired outcome.

The `Manager` class is where the specifics of your code will be. The `stubber` will create a generic version of this for you. It is your responsibility to change the API calls as needed.

Below are examples of the different versions of the design standards that have existed at one point or another:

* version 3.3 (proposed)
* `version 3.2 (current)`_
* `version 3.1`_
* `version 3`_
* `version 2`_
* `version 1`_

.. note::

   The ``ModuleManager`` class will change over time as design standards change. The above examples are for historical reference and training.

For implementation specifics, refer to the existing module.

A deep dive into the major differences between the different versions of design standards are here: :ref:`designdecisions`.

Connect to Ansible
------------------

After you complete the implementation details of the module, you can work on the code that hooks the module up to Ansible itself.

The main function
`````````````````

This code begins with the definition of the ``main`` function. This code should come after the definition of your class that you wrote earlier.

.. code-block:: python

   def main():

Argument spec and instantiation
```````````````````````````````

Next, generate the common argument spec using a utility method of Ansible.

.. code-block:: python

   argument_spec = f5_argument_spec()

With the ``argument_spec`` generated, update the values in it to match the ``options`` you declared in your ``DOCUMENTATION`` variable earlier.

The values that you must specify here are, again, the ones that are **not** common to all F5 modules. Below is the code you need to update your ``argument_spec``.

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

After you update the ``argument_spec``, instantiate an instance of the class, providing the ``argument_spec`` and the value that indicates it supports Check mode.

.. code-block:: python

   module = AnsibleModule(
       argument_spec=argument_spec,
       supports_check_mode=True
   )

All F5 modules **must** support Check mode, because you can use it to determine if the module makes changes when it's run against your devices.

Try and module execution
````````````````````````

The next block of code is a general execution of your class.

Wrap this execution inside of a ``try...except`` statement to ensure that you handle known errors.

Never include a general Exception handler here because it hides the details of an unknown exception.

.. code-block:: python

   try:
       obj = BigIpDeviceSshd(check_mode=module.check_mode, **module.params)
       result = obj.flush()

       module.exit_json(**result)
   except F5ModuleError as e:
       module.fail_json(msg=str(e))

Common running
``````````````

The final two lines in your module inform Python to execute the module's code if the script itself is executable.

.. code-block:: python

   if __name__ == '__main__':
       main()

Because of how Ansible works, when the ``main`` function contacts the remote device (or runs locally), it is not called if you import the module.

You would import the module if you were using it outside of Ansible, or in some sort of test environment where you do not want the module to actually run.

Test your module
----------------

Providing tests with your module is a crucial step for having it merged and subsequently pushed upstream.

This section provides detail on the organization of tests and how you can write your own to ensure that your modules work as designed.

Connection variables
````````````````````

You do not have to specify connection-related variables for each task. The playbook provides these values automatically.

These values include:

* `server`
* `server_port`
* `user`
* `password`
* `validate_certs`

Style checks
````````````

F5 uses the ``pycodestyle`` command to ensure that all modules meet certain coding standards and compatibility across Python releases.

You can run the style tests via the ``make`` command:

.. code-block:: bash

   make style

Before submitting your own module, your module must pass the style tests that F5 ships with the repository.

Integration/Functional tests
````````````````````````````

This is probably the most important part of testing.

When you submit your module, you must submit functional tests, so that you and F5 can agree that a module works on a particular platform.

When you submit a new PR, F5 will test your module on a variety of versions automatically, and will provide feedback if issues exist.

Structure of tests
``````````````````

When you stub a new module, test file stubs are automatically created.

First, let's look at the layout of a set of tests. A test includes a role whose name matches the name of the module you are testing.

This role goes in the `tests/integration/targets/` directory.

For example, a test role might look like this:

- `test/integration/targets/MODULE_NAME/`

This role has everything you would associate with a normal role in Ansible.

Consider the following examples:

- If your test requires static files, then a `files/` directory should be in your role.
- If your test requires template data (for example, iRules) for its input, then a `templates/` directory should be in your role.
- All roles will perform some work to test the module, so a `tasks/` directory should be in your role.

Now let's dig in to what a test should look like.

Test content
````````````

The test itself will follow the pattern below.

- Perform some operation with the module
- Assert a change (and optionally other values)
- Perform the same operation again (identical)
- Assert no change

All of the tests work like this, and it is a decent smoke test for all modules.

Here is an example of a test from the `bigip_device_sshd` module:

.. code-block:: yaml

   ---

   - name: Set the SSHD allow string to a specific IP
     bigip_device_sshd:
         allow:
             - "{{ allow[0] }}"
     register: result

   - name: Assert Set the SSHD allow string to a specific IP
     assert:
         that:
             - result is changed


You use the module and then check that the result you `register` changed. Tests for idempotence (the last two bullets above) are in the following section.

Test variables
``````````````

Information specific to the tests that you need to run should be in the `defaults/main.yaml` file of your test role.

By putting them there, you allow individuals to override values in your test by providing arguments to the CLI at runtime.

The idempotent test
```````````````````

All tests that change data should include a subsequent test that tries to perform the same test, but whose result you do *not* expect to change.

These are idempotent tests because they ensure that the module only changes settings if needed.

Here is an example of the previous test as an idempotent test:

.. code-block:: yaml

   - name: Set the SSHD allow string to a specific IP - Idempotent check
     bigip_device_sshd:
         allow:
             - "{{ allow[0] }}"
     register: result

   - name: Assert Set the SSHD allow string to a specific IP - Idempotent check
     assert:
         that:
             - result is not changed

**Notes:**

- The test code itself is identical to the previous test.

- The test name includes the string ``"- Idempotent check"``. This gives reviewers the ability to visually note that this is an idempotent test.

- The assertion checks that the result has *not* changed. This is the important part, because it ensures that the test itself was idempotent.

Calling the test
````````````````

To call the test and run it, this repo includes a `make` command that is available for all modules. The name of the `make` target is the name of your module.

For this example, the `make` command would be:

- make bigip_device_ssh

This command will run the module functional tests in debug mode.

You may optionally call the tests with the literal `ansible-playbook` command if you need to do things like:

- stepping (`--step`)
- starting at a particular task (`--start-at-task`)
- running tasks by tag name (`--tags issue-00239`)

To run the tests without `make`, first, change to the following directory:

- `test/integration`

Next, find the playbook that matches the module you wish to test. Using this playbook, run `ansible-playbook` as you normally would. A hosts file is in your working directory.

An example command might be:

.. code-block:: bash

   ansible-playbook -i inventory/hosts bigip_device_sshd.yaml

This is the most flexible option during debugging.

Including supplementary information
```````````````````````````````````

If you include files inside of the `files/`, `templates`, or other directories in which the content of that file was auto-generated or pulled from a third party source, you should include a `README.md` file in your role's directory.

In this file, you can include steps to reproduce any of the input items that you include in the role subdirectories.

In addition, this is a good location to include references to third-party file locations if you have included them in the tests. For example, if you were to include iRules or other things that you downloaded and included from DevCentral or similar.

The `README.md` is there for future developers to reference the information needed to re-create any of the inputs to your tests.

Other testing notes
```````````````````

When writing your tests, you should concern yourself with "undoing" what you have done previously to the test environment.

The test environment (at the time of this writing) boots harnesses for each suite of tests. That means that all tests run on the same harness.

Therefore, someone might accidentally use changes you made in one of the integration tests as a basis for subsequent tests. This makes using the `ansible-playbook` arguments specified previously exceedingly difficult.

Therefore, please cleanup after yourself. Since you need to test the `absent` case in most cases, this is a good opportunity to do that.

.. _version 1: https://github.com/F5Networks/f5-ansible/blob/b0d2afa1ad0b5bef29526477bb1ca0cdfd74ff74/library/_bigip_node.py
.. _version 2: https://github.com/F5Networks/f5-ansible/blob/b6a502034e21d1d7039ec0cbb642e22259d646fc/library/bigip_routedomain.py
.. _version 3: https://github.com/F5Networks/f5-ansible/blob/b81304b75d0d3a4d406f20e121ac3c3285168c2d/library/bigip_device_sshd.py
.. _version 3.1: https://github.com/F5Networks/f5-ansible/blob/f6ae5eecbcffdf0008905830dbefb4044f849a14/library/bigip_monitor_tcp_echo.py
.. _version 3.2 (current): https://github.com/F5Networks/f5-ansible/blob/8505ed1a245673aa856eb88baad9896bbe87994b/library/bigip_pool.py
