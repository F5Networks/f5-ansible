Code conventions
================

The F5 modules follow a set of coding conventions that apply to all new and existing modules. These conventions help new contributors quickly develop new modules, and they help existing contributors maintain the current modules.

Where possible, F5 tries to automate the validation of these coding conventions so you are aware of mistakes and can fix them yourself.

For more information on the tools that perform these checks, refer to the :doc:`tests` page.

When you write modules and their accompanying tests and docs, follow these coding conventions.

Use the complex/structure map format
------------------------------------

In reference to Jeff Geerling's page |geerling|, this format looks like this:

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

F5 uses this format for several reasons, including Geerling's.

- The structure is all valid YAML that uses the structured list/map syntax.
- Strings, booleans, integers, octals, etc. are all preserved (instead of converted to strings).
- Each parameter must be on its own line, so you can't chain together ``mode: 0755, owner: root, user: root`` to save space.
- YAML syntax highlighting works slightly better for this format than ``key=value``, since it highlights each key and displays values as constants, strings, etc.

In addition, some situations will raise syntax errors if you use the simple ``key=value`` format.

And finally, it saves space and is easier to read and know what the arguments to the module are.

.. |geerling| raw:: html

   <a href="http://www.jeffgeerling.com/blog/yaml-best-practices-ansible-playbooks-tasks" target="_blank">here</a>


Alphabetize the module's parameters
-----------------------------------

The parameters must be in alphabetic order.

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

This provides consistency between module usage and a way to see at a glance if a module has the correct parameters.

Use double quotes for strings
-----------------------------

Ansible supports a simple parameter format. If a value is a string, represent it as a string by using double quotes.

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

Do not use quotes for numbers
-----------------------------

For numeric characters, do not use quotes. If the expected value is a number and you provide a number wrapped in quotes, some modules will raise 'type' errors.

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
-----------------------------------

A YAML file usually begins with three dashes. As such, you should have that as part of your own YAML files.

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

Give each task a name
---------------------

When your Playbooks encounter errors, the name of the task is always called out in the failure. If you do not provide a name, Ansible creates a name by using the module call itself.

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

Always include a DOCUMENTATION variable
---------------------------------------

Ansible requires the DOCUMENTATION variable; it serves as the source of the module documentation that appears on their website.

Good documentation is essential to others being able to use the module, so you must include it.

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


Always include an EXAMPLES variable
-----------------------------------

Useful and valid examples are crucial for people new to Ansible and for the module itself.

When providing examples, be mindful of what you provide. If you developed the module with a specific use case in mind, be sure to include that use case. It may be applicable to a large majority of users and may eliminate a significant portion of time that they would otherwise spend figuring out what is or is not needed.

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

Always include a RETURN variable
--------------------------------

The RETURN variable provides documentation essential to determining what, if any, information the module returns.

Other users will reference this documentation when they want to use the ``register`` keyword.

The ``RETURN`` field should include the parameters that your module has changed. If nothing has changed, then the module does not need to return any values.

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

According to `bcoca`, the correct way to set a RETURN variable when a module does not return any information is the following.

**GOOD**

.. code-block:: python

   RETURN = '''
   # only common fields returned
   '''

Make the author field a list
----------------------------

Multiple people will probably maintain the module over time, so it is a good idea to make the ``author`` keyword in your module a list.

**GOOD**

.. code-block:: yaml

   author:
     - Tim Rupp (@caphrim007)


**BAD**

.. code-block:: yaml

   author: Tim Rupp (@caphrim007)


Use GitHub handle for the author name
-------------------------------------

Both Ansible and the F5 Ansible repository are on GitHub. Therefore, for maintenance reasons, F5 requires your GitHub handle. Additionally, your email address may change over time.

**GOOD**

.. code-block:: yaml

   author:
     - Tim Rupp (@caphrim007)


**BAD**

.. code-block:: yaml

   author:
     - Tim Rupp <caphrim007@gmail.com>


Use 2 spaces in DOCUMENTATION, EXAMPLES, and RETURN
---------------------------------------------------

Follow this simple spacing convention to ensure that everything is properly spaced.

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

Use Ansible lookup plugins where appropriate
--------------------------------------------

Ansible provides existing facilities that you can use to read in file contents to a module's parameters.

If your module can accept a string or a file containing a string, then assume that users will be using the lookup plugins.

For example, SSL files are typically strings. SSH keys are also strings, even if they are in a file. Therefore, you would delegate the fetching of the string data to a lookup plugin.

There should be no need to use the python ``open`` facility to read in the file.

**GOOD**

.. code-block:: yaml

   some_module:
       string_param: "{{ lookup('file', '/path/to/file') }}"


**BAD**

.. code-block:: yaml

    some_module:
        param: "/path/to/file"


Always expand lists in the various documentation variables
----------------------------------------------------------

When you list examples or documentation in any of the following variables:

- DOCUMENTATION
- RETURN
- EXAMPLES

Always expand lists of values if the key takes a list value.

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

Specify the BIG-IP version
--------------------------

In the ``DOCUMENTATION`` section notes, you should specify which version of BIG-IP the module requires.

**GOOD**

.. code-block:: yaml

   notes:
     - Requires BIG-IP version 12.0.0 or greater


**BAD**

.. code-block:: yaml

   Any version less than 12.0.0.

If your module requires functionality greater than 12.0.0 it is also acceptable to specify that in the ``DOCUMENTATION`` block.

Never raise a general exception
-------------------------------

General exceptions are bad because they hide unknown errors from you, the developer. If a bug report comes in and an exception that you do not handle causes the exception, the issue will be exceedingly difficult to debug.

Instead, only catch the `F5ModuleError` exception that the `f5-sdk` provides. Specifically raise this module and handle those errors. If an unknown error occurs, a full traceback will allow you to debug the problem more easily.

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

Support check mode
------------------

Check mode allows Ansible to run your Playbooks in a dry-run sort of operation. This is handy when you want to run a set of tasks but are not sure what will happen when you do.

Because BIG-IPs are usually considered a sensitive device to handle, you should always implement a check mode.

|playbook|

.. |playbook| raw:: html

   <a href="http://www.jeffgeerling.com/blog/yaml-best-practices-ansible-playbooks-tasks" target="_blank">http://www.jeffgeerling.com/blog/yaml-best-practices-ansible-playbooks-tasks</a>

Do not use local_action in your EXAMPLES
----------------------------------------

Some people prefer local_action and some people prefer delegation. Delegation is more applicable to general-purpose Ansible, so you should get in the habit of using and understanding it.

Therefore, do not use `local_action` when defining examples. Instead, use `delegate_to`.

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

Set default EXAMPLE parameters
------------------------------

For consistency, always use the following values for the given parameters, so you do not have to over-think the inclusion of your example:

- user: "admin"
- password: "secret"
- server: "lb.mydomain.com"

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

Assign values before returning them
-----------------------------------

To enable easier debugging when something goes wrong, ensure that you assign values **before** you return those values.

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

In the bad example, when it comes time to debug the value of the variable, you must change the code to do an assignment operation anyway.

For example, if you use `q` to debug the value, you must implicitly assign the value of the API call before you do this.

.. code-block:: python

   ...
   result = self.client.api....
   q.q(result)
   ...

When the code does not do an assignment, then you must change the code before you are able to debug the code.

Create a functional test for each code fix
------------------------------------------

When you fix an issue and it requires changes to code, you should create a new functional test YAML file in the module's `test/integration/PRODUCT/targets` directory.

For example, consider `Github Issue 59`_, which is relevant to the `bigip_virtual_server` module.

The developer added new code to the module. To verify that someone tested the new code, the developer should add a new file to the module's `targets` directory here:

- `test/functional/bigip/bigip_virtual_server/tasks`

The name of the file should be:

- `issue-59.yaml`

And inside the file, you should include any and all work to:

- Set up the test
- Perform the test
- Teardown the test

Any issues that you report on GitHub should follow the same pattern. However, the filenames of those modules should be:

- `ansible-xxxxx.yaml`

This way, they will not conflict with the numeric namespace in the `f5-ansible` repository.

.. _Github Issue 59: https://github.com/F5Networks/f5-ansible/issues/59


Exclude code from unit test coverage
------------------------------------

Ansible's test runner makes use of `pytest`, so the acceptable way of excluding lines from code coverage is here:

- http://coverage.readthedocs.io/en/coverage-4.2/excluding.html

You should use this to include the various `*_on_device` and `*_from_device` methods in modules that make direct calls to the remote BIG-IPs.

Put exception message on a new line
-----------------------------------

This convention helps eliminate the total number of columns in use, but also increases readability when long lines tend to scroll off screen. Even with a 160 column limit for this project, long lines, and many lines, can begin to grow less compact.

**GOOD**

.. code-block:: python

   ...
   raise F5ModuleError(
       '"{0}" is not a supported filter. '
       'Supported key values are: {1}'.format(key, ', '.join(keys)))
   )

**BAD**

.. code-block:: python

   ...
   raise F5ModuleError('"{0}" is not a supported filter. '
                       'Supported key values are: {1}'.format(key, ', '.join(keys)))

Put list contents on a new line
-------------------------------

Lists should also be on a new line. The ending bracket should be on a new line as well, aligned with the beginning of the variable name.

**GOOD**

.. code-block:: python

   ...
   mylist = [
       'foo', 'bar',
       'baz', 'biz'
   ]

**BAD**

.. code-block:: python

   ...
   mylist = ['foo', 'bar',
             'baz', 'biz']

Include the license header
--------------------------

Each module requires a license header that includes the GPL3 license.

Here is the common license header.

.. code-block:: python

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

If the module under development is your original work, then you can include your name in the copyright above.

If you are only contributing to an existing module, then it is not necessary to include a copyright line at the top. Instead, accepting the F5 CLA is sufficient to get code merged into the F5 branch.

Include the ANSIBLE_METADATA variable
-------------------------------------

The ANSIBLE_METADATA variable should be first in your module. It specifies metadata for the module itself. It can always look the same.

Here is how it's defined in code.

.. code-block:: python

   ANSIBLE_METADATA = {'status': ['preview'],
                       'supported_by': 'community',
                       'version': '1.0'}

The stubber creates this for you automatically.

Do not include required key for non-required parameters
-------------------------------------------------------

This convention comes to us courtesy of Ansible module-authoring rules. This convention limits the amount of verbosity in module code. Additionally, conflict can occur if you do not follow this convention (who is right? docs or code?).

Ansible, by default, makes parameters not required. It is redundant to provide it again in your documentation.

**GOOD**

.. code-block:: yaml

   ...
   login:
     description:
       - Specifies, when checked C(enabled), that the system accepts SSH
         communications.
     choices:
       - enabled
       - disabled
   ...

**BAD**

.. code-block:: yaml

   ...
   login:
     description:
       - Specifies, when checked C(enabled), that the system accepts SSH
         communications.
     choices:
       - enabled
       - disabled
     required: False
   ...

Do not include default key for parameters without defaults
----------------------------------------------------------

Another convention from Ansible, similar to the `required: False` convention, is applying the rule to the `default` value. Since `default: None` is already the value that Ansible uses (in code), it is redundant to provide it again in the docs.

**GOOD**

.. code-block:: yaml

   ...
   login:
     description:
       - Specifies, when checked C(enabled), that the system accepts SSH
         communications.
     choices:
       - enabled
       - disabled
   ...

**BAD**

.. code-block:: yaml

   ...
   login:
     description:
       - Specifies, when checked C(enabled), that the system accepts SSH
         communications.
     choices:
       - enabled
       - disabled
     default: None
   ...


Do not decompose to a \*_device method if the using method is itself a \*_device method
----------------------------------------------------------------------------------------

This convention is in place to limit the total amount of function decomposition that you will inevitably try to put into the code.

Some level of decomposition is good because it isolates the code that targets the device (called `*_device` methods) from the code that does not communicate with the device.

This method of isolation is how you extend modules when the API code diverges, or when the means of transporting information from and to the device changes.

You can take this decomposition too far, though. Refer to the examples below for an illustration of this. When you go to far, the correction is to merge the two methods.

**GOOD**

.. code-block:: python

   ...
   def import_to_device(self):
       self.client.api.tm.asm.file_transfer.uploads.upload_file(self.want.file)
       tasks = self.client.api.tm.asm.tasks
       result = tasks.import_policy_s.import_policy.create(
           name=self.want.name, filename=name
       )
       return result
   ...

**BAD**

.. code-block:: python

   ...
   def upload_to_device(self):
       self.client.api.tm.asm.file_transfer.uploads.upload_file(self.want.file)

   def import_to_device(self):
       self.upload_to_device()
       tasks = self.client.api.tm.asm.tasks
       result = tasks.import_policy_s.import_policy.create(
           name=self.want.name, filename=name
       )
       return result
   ...

This convention remains valid when the code you are using is a single line. Therefore, if you use the `upload_file` line in many places in the code, it is **still** correct to merge the methods instead of having a different method for it.

The only time when it would be correct to decompose it is if the "other" methods were **not** `*_device` methods.
