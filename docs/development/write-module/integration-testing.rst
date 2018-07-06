Integration/Functional tests
============================

This is probably the most important part of testing.

When you submit your module, you must submit functional tests, so that you and F5 can agree
that a module works on a particular platform.

When you submit a new PR, F5 will test your module on a variety of versions automatically, and
will provide feedback if issues exist.

Structure of tests
------------------

When you stub a new module, test file stubs are automatically created. There are several parts to
these stubs, and ultimately to the integration tests. All integration tests are composed of plain-old
Ansible features and components.

* A Playbook
* A Role
* Files
* Templates
* Inventory

The playbook
````````````

All integration tests begin their life in the ``Playbook``. The Playbook used by the tests is a regular
Playbook that you might find in regular Ansible deployments. For the module being developed, `here is the
Playbook that is used`_.

As might be expected, this Playbook has all the components of a "normal" Playbook. It specifies hosts,
has a name, declares variables, and includes a Role.

The Playbook and its contents are shown below.

.. code-block:: python

   - name: Test the bigip_policy_rule module
     hosts: "f5-test[0]"
     connection: local
     any_errors_fatal: true

     vars:
       limit_to: '*'
       __metadata__:
         version: 1.0
         tested_platforms:
           - NA
         callgraph_exclude:
           - pycallgraph.*

           # Ansible related
           - ansible.module_utils.basic.AnsibleModule.*
           - ansible.module_utils.basic.*
           - ansible.module_utils.parsing.*
           - ansible.module_utils._text.*
           - ansible.module_utils.six.*

     environment:
       F5_SERVER: "{{ ansible_host }}"
       F5_USER: "{{ bigip_username }}"
       F5_PASSWORD: "{{ bigip_password }}"
       F5_SERVER_PORT: "{{ bigip_port }}"
       F5_VALIDATE_CERTS: "{{ validate_certs }}"

     roles:
       - bigip_policy_rule

Because most of this is a normal Playbook, this tutorial will just cover the parts that are interesting.

The first interesting bit is the large ``vars`` section. Frankly speaking, this can be ignored by
most contributors as it is not something that is used by the functional tests directly. Its
purpose is to provide metadata to the module developers for use in tracking testing and things.

+------------------+-------------------------------------------------------------------------------------------------+
| Variable         | Purpose                                                                                         |
+==================+=================================================================================================+
| ``limit_to``     | * Not currently used                                                                            |
|                  | * In the future, this var may allow you to select the tests that you want to run.               |
+------------------+-------------------------------------------------------------------------------------------------+
| ``__metadata__`` | * Special variable used by F5 only to track F5-specific interests.                              |
|                  | * Playbook metadata versions are described more :doc:`in this document <../playbook-metadata>`. |
+------------------+-------------------------------------------------------------------------------------------------+

The ``environment`` section is also interesting in the context of the F5 modules. The modules support
specifying common connection parameters in the environment like this so that you do not need to specify
them in each task. To keep the size of the tasks small, the developers use this method.

The role
````````

The Role contains all of the tests that will be run as part of the integration test suite.
Roles are written, and use all the same conventions, that normal Ansible Roles use.

Roles for integration tests can be found in the ``targets`` directory, right alongside the test
Playbook. Inside this directory are sub-directories. Each is named after the module under test.

For the purposes of this tutorial, the `Role directory can be found here`_.

This role has everything you would associate with a normal role in Ansible.

* If your test requires static files, then a ``files/`` directory should be in your role.
* If your test requires template data (for example, iRules) for its input, then a ``templates/``
  directory should be in your role.
* All roles will perform some work to test the module, so a ``tasks/`` directory should be in
  your role.

When Ansible executes a role, it calls one file and one file only. That file is:

* ``tasks/main.yaml``

All integration tests will originate from this file.

Additional files that are commonly found in the ``tasks/`` directory alongside the
``main.yaml`` file include:

* ``setup.yaml``
* ``teardown.yaml``

These files, as their names suggest, are used for setting up the integration tests that
*will* run, and tearing down the integration tests that *have* run, respectively.

Now let's dig in to what a test should look like.

Test content
------------

The implementation for the functional tests related to the module being developed in this
tutorial `can be found here`_.

The test itself will follow the pattern below.

- Perform some operation with the module
- Assert a change (and optionally other values)
- Perform the same operation again (identical)
- Assert no change

All of the tests work like this, and it is a decent smoke test for all modules.

Here is an example of a test from the module under development in this tutorial.

.. code-block:: yaml

   - name: Create rule for published policy, no actions, no conditions
     bigip_policy_rule:
       policy: "{{ policy_name1 }}"
       name: rule1
     register: result

   - name: Assert Create rule for published policy, no actions, no conditions
     assert:
       that:
         - result is changed

   - name: Create rule for published policy, no actions, no conditions - Idempotent check
     bigip_policy_rule:
       policy: "{{ policy_name1 }}"
       name: rule1
     register: result

   - name: Assert Create rule for published policy, no actions, no conditions - Idempotent check
     assert:
       that:
         - result is not changed

All tests that change data should include a subsequent test that tries to perform the same test,
but whose result you do *not* expect to change.

These are idempotent tests because they ensure that the module only changes settings if needed.

.. note::

   The test code itself is identical to the previous test. The test name includes the string
   ``"- Idempotent check"``. This gives reviewers the ability to visually note that this is an
   idempotent test. Additionally, it allows them to call out this specific test if running
   the Playbook with the ``--start-at-task`` argument.

   The assertion checks that the result has *not* changed. This is the important part, because
   it ensures that the test itself was idempotent.

Test variables
--------------

Information specific to the tests that you need to run should be in the `defaults/main.yaml`
file of your test role.

By putting them there, you allow individuals to override values in your test by providing
arguments to the CLI at runtime.

Calling the test
----------------

Tests are run in two ways.

* Use a ``make`` command
* Run the playbook directly

The methods have different pros and cons depending on your objective. For those concerned
with developing modules, you will likely prefer the latter method: running playbooks directly.

+------------------+-------------------------------------------------------+------------------------------------------+
| Method           | Pros                                                  | Cons                                     |
+==================+=======================================================+==========================================+
| ``make`` command | * Not a lot to type                                   | * No debug output                        |
|                  | * Commands available for all modules                  | * No ability to step through tests       |
|                  | * Useful when verifying an otherwise known good test  | * No ability to start at specific tests  |
+------------------+-------------------------------------------------------+------------------------------------------+
| Run Playbook     | * Supports all Ansible commands                       | * Requires more typing                   |
|                  | * Supports skipping                                   | * Requires knowledge of Ansible commands |
|                  | * Supports debug                                      |                                          |
|                  | * Supports stepping                                   |                                          |
|                  | * Supports specifying overriding arguments            |                                          |
|                  | * Supports tag selection                              |                                          |
+------------------+-------------------------------------------------------+------------------------------------------+

Since this tutorial is interested in development of a module, it will use the "Run Playbook"
method.

To run the tests without ``make``, first, change to the following directory:

* ``test/integration``

Next, find the playbook that matches the module you wish to test. Using this playbook, run
`ansible-playbook` as you normally would. A hosts file is provided in the ``inventory`` directory.

An example command might be:

.. code-block:: bash

   ansible-playbook -i inventory/hosts bigip_policy_rule.yaml -vvvv --step

This is the most flexible option during debugging, and it is the recommended way to test the
modules.

Including supplementary information
-----------------------------------

If you include files inside of the ``files/``, ``templates``, or other directories in which the
content of that file was auto-generated or pulled from a third party source, you should
include a ``README.md`` file in your role's directory.

In this file, you can include steps to reproduce any of the input items that you include in
the role subdirectories.

In addition, this is a good location to include references to third-party file locations if
you have included them in the tests. For example, if you were to include iRules or other
things that you downloaded and included from DevCentral or similar.

The ``README.md`` is there for future developers to reference the information needed to re-create
any of the inputs to your tests.

Other testing notes
-------------------

When writing your tests, you **should** concern yourself with "undoing" what you have done
previously to the test environment.

The test environment boots harnesses for each suite of tests. This means that all tests run on
the same harness. Therefore, someone might accidentally use changes you made in one of the integration
tests as a basis for subsequent tests. This makes using the ``ansible-playbook`` previously mentioned
arguments (``--step``, ``--start-at-task``, ``--tags``, etc.) much more difficult.

Therefore, please clean up after yourself. Since you need to test the ``absent`` case in most
cases, this is a good opportunity to do that. The ``teardown.yaml`` file can also be used to
teardown any resources that were created to assist in testing your module.

Conclusion
----------

If you've made it this far, then give yourself a pat on the back. This officially concludes the
mainline tutorial concerning module development. At this point you should be much more familiar
with the parts that make up a module, as well as the assortment of supporting files for the
module.

Feel free to peruse the other development-related docs on the site, and keep an eye out for
future documents that detail more technical methods for development. Finally, since the
process of module development (and the conventions that are used) are continually changing,
be sure to frequently refer back to these pages for updates to your existing knowledge.

.. _can be found here: https://github.com/F5Networks/f5-ansible/blob/devel/test/integration/targets/bigip_policy_rule/tasks/main.yaml
.. _here is the Playbook that is used: https://github.com/F5Networks/f5-ansible/blob/devel/test/integration/bigip_policy_rule.yaml
.. _Role directory can be found here: https://github.com/F5Networks/f5-ansible/tree/devel/test/integration/targets/bigip_policy_rule
