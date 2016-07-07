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
