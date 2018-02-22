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
