Standards
=========

The F5 modules attempt to follow a set of coding standards that apply to
all new and existing modules.

These standards help new contributors quickly develop new modules.
Additionally, they help existing contributors maintain the current modules.

Standards checking
------------------

Where possible, we try to automate the validation of these coding standards
so that you are aware of mistakes and able to fix them yourself without
having to have the maintainers intervene.

For more information on what tools perform these checks, refer to the tests
page.

Standards
---------

When writing your modules and their accompanying tests and docs, please
follow the below coding standards.

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

All modules must have a DOCUMENTATION preamble
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The DOCUMENTATION preamble is also required by Ansible upstream as it
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

  Missing DOCUMENTATION field


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

  - Tim Rupp (@caphrim007)


**BAD**

  - Tim Rupp <caphrim007@gmail.com>


Use 2 spaces in the DOCUMENTATION, EXAMPLES, and RETURN
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a simple spacing standard to ensure that everything is properly
spaced over.

**GOOD**

  - "foo"


**BAD**

    - "foo"

All modules must support check mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check-mode allows Ansible to run your Playbooks in a dry-mode sort of
operation. This is very handy when you want to run a set of tasks but
are not sure what will happen when you do.

Since BIG-IPs are usually considered a sensitive device to handle, there
should always be a check-mode implemented in your module.

.. _here: http://www.jeffgeerling.com/blog/yaml-best-practices-ansible-playbooks-tasks