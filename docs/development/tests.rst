Tests
=====

Several different CI/CD tools automatically test the modules.

General tests check syntax, and specific tests exercise the functionality of the module.

General tests
-------------

All modules go through a set of general tests. Travis CI runs these tests. You can view the tests in ``.travis.yml`` in the root directory of the ``f5-ansible`` repository.

- flake8
- ansible-lint

Functional tests
----------------

Each Ansible module should have a role associated with it. This role contains all of the functional tests you want run to validate your module.

These tests run against several different test harnesses of BIG-IP VE. You do not need instances of each BIG-IP VE version available to you; the F5 instances have all of the necessary modules enabled for you to test against.

Code coverage
-------------

Upstream, Ansible provides code-coverage metrics for the F5 modules. These metrics are specific to the **UNIT** tests, not the integration/functional tests.

The URL is here:

- https://codecov.io/gh/ansible/ansible/tree/devel/lib/ansible/modules/network/f5

Ansible updates these metrics every 24 hours. Therefore, if you submit new code that includes unit tests, you will not immediately see the results.

Pycodestyle checks
------------------

F5 includes `pycodestyle` checks as part of the linting process. Ansible itself does this and, therefore, F5 must also include the steps.

The tests that F5 runs are from:

- https://github.com/ansible/ansible/blob/devel/test/sanity/pep8/current-ignore.txt

F5 updates these tests for each Ansible release.

Why do I make any error fatal?
``````````````````````````````

The integration tests specify the following in their YAML.

.. code-block:: yaml

   - name: Test the bigip_iapp_service module
     ...
     any_errors_fatal: true
     ...

Why is `any_errors_fatal` specified and set to `true`?

The reason is because of the test layout.

Integration tests build on top of each other. If one of those tests fails, then a cascade of failures will occur. Therefore it's a waste of time to continue with tests; the remainder will never pass.

Take, for example, a type of integration test for bigip_pool. It looks like this:

- Create pool
- Assert creation
- Create pool - idempotent check
- Assert no creation

If any of those tests fail, it is equivalent to all of them failing.

- If the first fails, then all the latter will fail.
- If the second fails, that means the first one is incorrect, and failure occurs.
- If the third fails, then the updating code is wrong and future tests that change parameters will fail.
- If the fourth fails, then the assertion is that the third test is wrong, and future tests that change parameters will fail.

For these reasons, F5 makes the integration tests fail fast.
