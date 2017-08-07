Code Conventions
================

The F5 modules attempt to follow a set of coding conventions that apply to
all new and existing modules.

These conventions help new contributors quickly develop new modules.
Additionally, they help existing contributors maintain the current modules.

Style checking
--------------

Where possible, we try to automate the validation of these coding conventions
so that you are aware of mistakes and able to fix them yourself without
having to have the maintainers intervene.

For more information on what tools perform these checks, refer to the tests
page.

Conventions
-----------

When writing your modules and their accompanying tests and docs, please
follow the below coding conventions.

Use the complex/structure map format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In reference to Jeff Geerling's page `here`_, this format looks like this.

.. code-block:: yaml

   - name: Create a UCS
     bigip_ucs_fetch:
        dest: "/tmp/{{ ucs_name }}"
        password: "{{ bigip_password }}"
        server: "{{ inventory_hostname }}"
        src: "{{ ucs_name }}"
        user: "{{ bigip_username }}"
        validate_certs: "{{ validate_certs }}"
     register: result

There are several reasons that we use this format. Among them are Geerling's
reasons.

  * The structure is all valid YAML, using the structured list/map syntax
    mentioned in the beginning of this post.
  * Strings, booleans, integers, octals, etc. are all preserved (instead of
    being converted to strings).
  * Each parameter must be on its own line, so you can't chain together
    ``mode: 0755, owner: root, user: root`` to save space.
  * YAML syntax highlighting works slightly better for this format than
    ``key=value``, since each key will be highlighted, and values will be
    displayed as constants, strings, etc.

In addition to those reasons, there are also some situations that, if you
use the simple ``key=value`` format will raise syntax errors. Finally, it
saves on space and, in the maintainers opinion, is easier to read and know
(by looking) what the arguments to the module are.

Alphabetize your module parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The parameters to your modules in the Roles and Playbooks that are developed
here must be in alphabetic order.

**GOOD**

.. code-block:: yaml

   - name: My task
     bigip_module:
         alpha: "foo"
         beta: "bar"
         gamma: "baz"


**BAD**

.. code-block:: yaml

   - name: My task
     bigip_module:
         alpha: "foo"
         gamma: "baz"
         beta: "bar"

This provides for consistency amongst module usage as well as provides a way
to see at a glance if a module has the correct parameters.

Double-quotes for Strings, no quotes for Numbers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ansible supports a simple form of typing for your parameters. If there is
a value that is a string, it should be represented as a string using double
quotes.

**GOOD**

.. code-block:: yaml

   - name: My task
     bigip_module:
         alpha: "foo"
         beta: "bar"


**BAD**

.. code-block:: yaml

   - name: My task
     bigip_module:
         alpha: foo
         beta: bar

For numeric characters, you should not use any quotes because this can cause
some modules to raise 'type' errors if the expected value is a number and you
provide it with a number wrapped in quotes


**GOOD**

.. code-block:: yaml

   - name: My task
     bigip_module:
         alpha: 1
         beta: 100


**BAD**

.. code-block:: yaml

   - name: My task
     bigip_module:
         alpha: "1"
         beta: "100"

Begin YAML files with a triple-dash
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A YAML file usually begins with three dashes. As such, you should have that
be a part of your own YAML files.


**GOOD**

.. code-block:: yaml

   ---

   - name: My task
     bigip_module:
         alpha: 1
         beta: 100


**BAD**

.. code-block:: yaml

   - name: My task
     bigip_module:
         alpha: "1"
         beta: "100"

All tasks should have a name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When your Playbooks encounter errors, the name of the task is always called
out in the failure. If you do not provide a name, then Ansible creates a
name for you using the module call itself.

Naming your tasks allows you to quickly reference where a failure occurred.

**GOOD**

.. code-block:: yaml

   - name: My task
     bigip_module:
         alpha: 1
         beta: 100


**BAD**

.. code-block:: yaml

   - bigip_module:
         alpha: "1"
         beta: "100"

All modules must have a DOCUMENTATION variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The DOCUMENTATION variable is also required by Ansible upstream as it
serves as the source of the module documentation that is generated
on their site.

Good documentation is essential to people being able to use the module
so it must be included.

**GOOD**

.. code-block:: python

   DOCUMENTATION = '''
   ---
   module: bigip_device_ntp
   short_description: Manage NTP servers on a BIG-IP
   description:
     - Manage NTP servers on a BIG-IP
   version_added: "2.1"
   options:
   ...
   '''


**BAD**

.. code-block:: python

   Missing DOCUMENTATION variable


All modules must have an EXAMPLES variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Useful and valid examples are crucial for people new to Ansible and to
the module itself.

When providing examples, be mindful of what you provide. If you developed
the module with a specific use case in mind, be sure to include that use
case. It may be applicable to a large majority of users and, therefore, may
eliminate a significant portion of their time that they would otherwise
spend figuring out what is or is not needed.

**GOOD**

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
   '''


**BAD**

.. code-block:: python

   Missing EXAMPLES variable

All modules must have a RETURN variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The RETURN variable provides documentation essential to determining what, if
any, information is returned by the operation of the module.

End users of the module will reference this documentation when they want to
use the ``register`` keyword.

The ``RETURN`` field should include the parameters that have been changed by
your module. If nothing has been changed, then no values need be returned.

**GOOD**

.. code-block:: python

   RETURN = '''
   full_name:
       description: Full name of the user
       returned: changed
       type: string
       sample: "John Doe"
   '''


**BAD**

.. code-block:: python

   Missing RETURN variable

If your module does not return any information, then an empty YAML string
is sufficient

**GOOD**

..code-block:: python

  RETURN = '''# '''

The author field must be a list
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a good possibility that multiple people will work to maintain
the module over time, so it is a good idea to make the ``author`` keyword
in your module a list.

**GOOD**

.. code-block:: yaml

   author:
     - Tim Rupp (@caphrim007)


**BAD**

.. code-block:: yaml

   author: Tim Rupp (@caphrim007)


Author field should be Github handle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Both Ansible and this repository are maintained on Github. Therefore, for
maintenance reasons we require your Github handle. Additionally, your
email address may change over time.

**GOOD**

.. code-block:: yaml

   author:
     - Tim Rupp (@caphrim007)


**BAD**

.. code-block:: yaml

   author:
     - Tim Rupp <caphrim007@gmail.com>


Use 2 spaces in the DOCUMENTATION, EXAMPLES, and RETURN
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a simple spacing convention to ensure that everything is properly
spaced over.

**GOOD**

.. code-block:: yaml

   options:
     server:
       description:
         - BIG-IP host
       required: true
     user:
   ^^


**BAD**

.. code-block:: yaml

   options:
       server:
           description:
               - BIG-IP host
           required: true
       user:
   ^^^^

Use ansible lookup plugins where appropriate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ansible provides existing facilities that can be used to read in file contents
to a module's parameters.

If your module can accept a string or a file containing a string, then assume
that users will be using the lookup plugins.

For example, SSL files are typically strings. SSH keys are also strings even
if they are contained in a file. Therefore, you would delegate the fetching
of the string data to a lookup plugin.

There should be no need to use the python ``open`` facility to read in the
file.

**GOOD**

.. code-block:: yaml

   some_module:
       string_param: "{{ lookup('file', '/path/to/file') }}"


**BAD**

.. code-block:: yaml

    some_module:
        param: "/path/to/file"


Always expand lists in the various documentation variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When listing examples or documentation in any of the following variables,

  * DOCUMENTATION
  * RETURN
  * EXAMPLES

be sure to always expand lists of values if that key takes a list value.

**GOOD**

.. code-block:: yaml

   options:
     state:
       description:
         - The state of things
       choices:
         - present
         - absent


**BAD**

.. code-block:: yaml

   options:
     state:
       description:
         - The state of things
       choices: ['enabled', 'disabled']

Support for 12.0.0 or greater at this time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the ``DOCUMENTATION`` section notes, you should specify what version of BIG-IP
the module requires.

At this time, that version is 12.0.0, so your ``DOCUMENTATION`` string should
reflect that.

**GOOD**

.. code-block:: yaml

   notes:
     - Requires BIG-IP version 12.0.0 or greater


**BAD**

.. code-block:: yaml

   Any version less than 12.0.0.

If your module requires functionality greater than 12.0.0 it is also
acceptable to specify that in the ``DOCUMENTATION`` block.

Never raise a general Exception
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

General Exceptions are bad because they hide unknown errors from you, the
developer. If a bug report comes in and is being caused by an exception
that you do not handle, it will be exceedingly difficult to debug it.

Instead, only catch the `F5ModuleError` exception that is provided by the
`f5-sdk`. Specifically raise this module and handle those errors. If an
unknown error occurs, a full traceback will be produced that will more easily
allow you to debug the problem.

**GOOD**

.. code-block:: python

   try:
       // do some things here that can cause an Exception
   except bigsuds.OperationFailed as e:
       raise F5ModuleError('Error on setting profiles : %s' % e)

**GOOD**

.. code-block:: python

   if foo:
       // assume something successful happens here
   else:
       raise F5ModuleError('Error on baz')

**BAD**

.. code-block:: python

   try:
       // do some things here that can cause an Exception
   except bigsuds.OperationFailed as e:
       raise Exception('Error on setting profiles : %s' % e)

**BAD**

.. code-block:: python

   if foo:
       // assume something successful happens here
   else:
       raise Exception('Error on baz')

All modules must support check mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check-mode allows Ansible to run your Playbooks in a dry-mode sort of
operation. This is very handy when you want to run a set of tasks but
are not sure what will happen when you do.

Since BIG-IPs are usually considered a sensitive device to handle, there
should always be a check-mode implemented in your module.

.. _here: http://www.jeffgeerling.com/blog/yaml-best-practices-ansible-playbooks-tasks

Do not use local_action in your EXAMPLES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some folks like local_action and some folks like delegation. Delegation
is more applicable to general-purpose Ansible, so for that reason I want
to get people in the habit of using and understanding it.

Therefore, do not use `local_action` when defining examples. Instead,
use `delegate_to`.

**GOOD**

.. code-block:: python

   - name: Reset the initial setup screen
     bigip_sys_db:
         user: "admin"
         password: "secret"
         server: "lb.mydomain.com"
         key: "setup.run"
         state: "reset"
     delegate_to: localhost

**BAD**

.. code-block:: python

   - name: Reset the initial setup screen
     local_action:
         module: "bigip_sys_db"
         user: "admin"
         password: "secret"
         server: "lb.mydomain.com"
         key: "setup.run"
         state: "reset"

Default EXAMPLE parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^

For consistency, always using the following values for the given parameters

  * user: "admin"
  * password: "secret"
  * server: "lb.mydomain.com"

This allows you to not have to overthink the inclusion of your example.

**GOOD**

.. code-block:: python

   - name: Reset the initial setup screen
     bigip_sys_db:
         user: "admin"
         password: "secret"
         server: "lb.mydomain.com"
         key: "setup.run"
         state: "reset"
     delegate_to: localhost

**BAD**

.. code-block:: python

   - name: Reset the initial setup screen
     bigip_sys_db:
         user: "joe_user"
         password: "admin"
         server: "bigip.host"
         key: "setup.run"
         state: "reset"
     delegate_to: localhost

Assign before returning
^^^^^^^^^^^^^^^^^^^^^^^

To enable easier debugging when something goes wrong, ensure that you assign values
**before** you return those values.

**GOOD**

.. code-block:: python

   def exists(self):
       result = self.client.api.tm.gtm.pools.pool.exists(
           name=self.want.name,
           partition=self.want.partition
       )
       return result

**BAD**

.. code-block:: python

   def exists(self):
       return self.client.api.tm.gtm.pools.pool.exists(
           name=self.want.name,
           partition=self.want.partition
       )

The reason that the above **BAD** example is considered bad is that when it comes time
to debug the value of a variable, it requires that you change the code to do an
assignment operation anyway.

For example, using `q` to debug the value of the above requires that you implicitly
assign the value of the API call before you do this,

.. code-block:: python

   ...
   result = self.client.api....
   q.q(result)
   ...

When the code does not do a assignment, then you are required to change the code before
you are able to debug the code.

Fixed Github issues should have an associated issue-xxxxx.yaml file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a developer takes on a new issue that requires changes to code to get working,
these changes should be tested with a new functional test yaml file located in the
module's `test/integration/PRODUCT/targets` directory.

For example.

Consider the `Github Issue 59`_ which is relevant to the `bigip_virtual_server` module.

The developer needed to add new code to the module. So to verify that the new code is
tested, the developer should add a new file to the module's `targets` directory here

  * `test/functional/bigip/bigip_virtual_server/tasks`

The name of the file should be

  * `issue-59.yaml`

And inside of the file should be any and all work that is required to,

  * Setup the test
  * Perform the test
  * Teardown the test

Any issues that are reported on github should follow the same pattern, however the
filenames of those modules should be

  * `ansible-xxxxx.yaml`

So-as not to step on the numeric namespace that is used natively in the `f5-ansible`
repository.

.. _Github Issue 59: https://github.com/F5Networks/f5-ansible/issues/59

RETURN value when there is no return
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The correct way to set a RETURN variable whose module has no returnable things
is like this according to `bcoca`.

.. raw::

   RETURN = '''
   # only common fields returned
   '''

Excluding code from unit test coverage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ansible's test runner makes use of `pytest`, so the acceptable way of excluding
lines from code coverage is documented here.

  * http://coverage.readthedocs.io/en/coverage-4.2/excluding.html

The cases where you would want to use this include the various `*_on_device` and
`*_from_device` methods in modules that make direct calls to the remote BIG-IPs.

Exception message should be on a new line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This convention is done to eliminate the total number of columns in use, but also
to increase readability when long lines tend to scroll off screen. Even with a
160 column limit for this project, long lines, and many lines, can begin to grow
less compact.

**BAD**

.. code-block::python

   ...
   raise F5ModuleError('"{0}" is not a supported filter. '
                       'Supported key values are: {1}'.format(key, ', '.join(keys)))

**GOOD**

.. code-block::python

   ...
   raise F5ModuleError(
       '"{0}" is not a supported filter. '
       'Supported key values are: {1}'.format(key, ', '.join(keys)))
   )

List contents should start on a new line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the same reason given above concerning compactness, lists should follow the same
rule. The ending bracket should be on a new line as well, aligned with the beginning of
the variable name

**BAD**

.. code-block::python

   ...
   mylist = ['foo', 'bar',
             'baz', 'biz']

**GOOD**

.. code-block::python

   ...
   mylist = [
       'foo', 'bar',
       'baz', 'biz'
   ]
