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

Unit tests
----------

* https://pypi.python.org/pypi/responses

Common fixtures
*