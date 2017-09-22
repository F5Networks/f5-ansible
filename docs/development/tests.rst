Tests
=====

Module testing is performed automatically by several different CI/CD tools.
There are general tests which check syntax as well as specific tests that
exercise the functionality of the module.

General tests
-------------

All modules are run through a set of general tests. These general tests are
run by Travis CI and can be found in the ``.travis.yml`` in the root directory
of the ``f5-ansible`` repository.

  * flake8
  * ansible-lint

Functional tests
----------------

Each ansible module should have a role associated with it that contains all
of the functional tests that you want run to validate your module.

These tests are run against several different test harnesses of BIG-IP VE
that we have available. This provides you with the ability to test your
module against several supported versions of BIG-IP to ensure that it works
correctly.

We provide this service to you because we understand that it may not be the
case that you have instances of BIG-IP availble to you. These instances have
all of the necessary modules enabled for you to test against.

Code coverage
-------------

Upstream, Ansible provides code-coverage metrics for the F5 modules. These
metrics are specific to the **UNIT** tests; not the integration/functional tests.

The URL for viewing this information can be found here

* https://codecov.io/gh/ansible/ansible/tree/devel/lib/ansible/modules/network/f5

These metrics are updated every 24 hours. Therefore, if you submit new code to
Ansible which includes unit tests, you will not immediately see the results.

Pycodestyle checks
------------------

We include `pycodestyle` checks as part of our linting process. This process is
included because Ansible itself does it and, therefore, we too must include the
steps.

The tests that we run are takes from

* https://github.com/ansible/ansible/blob/devel/test/sanity/pep8/current-ignore.txt

They are updated for each Ansible release

Questions
---------

There are several questions regarding the way in that the tests are designed. I've
listed those questions and their answers below.

Why do I make any error fatal?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The integration tests specify the following in their YAML.

.. code-block:: yaml

   - name: Test the bigip_iapp_service module
     ...
     any_errors_fatal: true
     ...

Why is `any_errors_fatal` specified and set to `true`?

The reason is due to the way the tests are laid out. Integration tests build on
top of each other. If one of those tests fails, then a cascade of failures will
occur. Therefore it's a waste of time to continue with tests; the remainder will
never pass.

Take for example a type integration test for bigip_pool. It looks like this.

* Create pool
* Assert creation
* Create pool - idempotent check
* Assert no creation

Note that if any of those tests fail, that it is equivalent to all of them
failing.

* If the first fails, then all the latter will fail.
* If the second fails, that means the first one is incorrect, and therefore we
  have failure.
* If the third fails, then the updating code is wrong and future tests which
  change params will fail
* If the fourth fails, then the assertion is that the third test is wrong, and
  we've already mentioned what that means to future tests.

For those reasons, we make the integration tests fail fast by using the
aforementioned setting in Ansible.
