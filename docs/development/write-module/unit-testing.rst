Unit Testing
============

Unit testing ensures that the general execution of the module code is correct. It is
the fastest way to test, requires no F5 products, and is what the developers recommended be used
when doing the initial development of a module.

While both forms of testing are important, the unit tests will not tell you if you have a fully
functioning module. Functional tests are the only things that can provide anything close to this
assurance. Nevertheless, unit tests are required by the F5 module developers. When contributing
code to upstream Ansible, only unit tests may be submitted to the core product. This is because
the Ansible developers do not have the ability to test F5 products.

Filesystem location
-------------------

All unit tests are located in the following directory:

* ``tests/unit/``

Changing to this directory will show a number of files that are named after different modules.
For example:

.. code-block:: bash

   -rw-r--r--    1 trupp  OLYMPUS\Domain Users    3507 Jan 24 17:20 test_bigip_config.py
   -rw-r--r--    1 trupp  OLYMPUS\Domain Users    4138 Feb 15 11:21 test_bigip_configsync_action.py
   -rw-r--r--    1 trupp  OLYMPUS\Domain Users   16007 Feb 22 09:27 test_bigip_data_group.py
   -rw-r--r--    1 trupp  OLYMPUS\Domain Users   12692 Jan 24 17:20 test_bigip_device_connectivity.py
   -rw-r--r--    1 trupp  OLYMPUS\Domain Users    4323 Jan 24 17:20 test_bigip_device_dns.py
   -rw-r--r--    1 trupp  OLYMPUS\Domain Users    5547 Jan 24 17:20 test_bigip_device_group.py

These files are the unit test files themselves. The ``test/unit/`` directory also includes another
directory of interest:

* ``fixtures/``

This directory contains a number of static data files that are used by the different unit tests.

As will be seen later during test development, the files in the ``fixtures/`` directory can be
easily loaded by using functions in the unit test file. Examples of fixture files are:

.. code-block:: bash

   -rw-r--r--  1 trupp  OLYMPUS\Domain Users     912 Nov 14 19:22 load_tm_sys_syslog.json
   -rw-r--r--  1 trupp  OLYMPUS\Domain Users     893 Jan 24 17:20 load_tm_sys_ucs.json
   -rw-r--r--  1 trupp  OLYMPUS\Domain Users     969 Nov 14 19:22 load_vcmp_guest.json
   -rw-r--r--  1 trupp  OLYMPUS\Domain Users     808 Nov 14 19:22 load_vlan.json
   -rw-r--r--  1 trupp  OLYMPUS\Domain Users     510 Dec 18 18:37 load_vlan_interfaces.json

.. note::

   Fixture files are often in JSON format, because the REST API returns information in this format. Unit tests use these REST response payloads to verify the
   tests' correctness.

Tutorial module implementation
------------------------------

The implementation of the tutorial module's unit tests `can be found here`_. Additionally, you
will need to have the following fixture files downloaded and placed in the ``fixtures``
directory.

* `load_ltm_policy_draft_rule_http-uri_forward.json`_

General things to know about unit tests
---------------------------------------

Unit tests for the F5 Modules for Ansible are written using `pytest`_.

For ``pytest`` to be able to run your unit tests, your tests **must** follow these rules.

* Classes, if used, must start with the string ``Test``. Spelling must be exact.
* Methods or functions containing tests must start with the string ``test_``. Spelling must be
  exact.
* Unit tests do not need to do any form of cleanup. Pytest handles cleanup for you automatically.

Writing a unit test
-------------------

Let's take the time now to write the unit tests for the module that was developed in this
tutorial. During the initial stubber run, the ``f5ansible`` command produced a unit test file that included a sampling of what will need to be done.

Let's touch on those boilerplate blocks before investigating the actual testing code.

Import block
````````````

At the top of the unit test file (like at the top of many Python source code) there are a series
of ``import`` statements. These tell Python to include different bodies of code that come either
pre-installed with Python, or as separate packages that you should have installed.

.. note::

   All of the dependencies for typical F5 modules for Ansible are pre-installed for you in the
   development Docker containers that were mentioned at the beginning of the tutorial.

Some of the imports of interest are:

* The SkipTest import
* The dev versus prod import

First, the ``SkipTest`` import. This import is defined as such:

.. code-block:: python

   from nose.plugins.skip import SkipTest
   if sys.version_info < (2, 7):
       raise SkipTest("F5 Ansible modules require Python >= 2.7")

The purpose of this import is to declare that the F5 modules **require** Python versions
greater than, or equal to, 2.7. Over time, it is expected that this check will change to require
Python 3 and beyond. Therefore, be sure to keep aware of this and do not find yourself in a
situation where you are unable to upgrade either your operating system, or Python, to later
versions.

Next, the dev/prod import. This import is defined as such:

.. code-block:: python

   try:
       from library.bigip_policy_rule import Parameters
       from library.bigip_policy_rule import ModuleParameters
       from library.bigip_policy_rule import ApiParameters
       from library.bigip_policy_rule import ModuleManager
       from library.bigip_policy_rule import ArgumentSpec
       from library.module_utils.network.f5.common import F5ModuleError
       from library.module_utils.network.f5.common import iControlUnexpectedHTTPError
       from test.unit.modules.utils import set_module_args
   except ImportError:
       try:
           from ansible.modules.network.f5.bigip_policy_rule import Parameters
           from ansible.modules.network.f5.bigip_policy_rule import ModuleParameters
           from ansible.modules.network.f5.bigip_policy_rule import ApiParameters
           from ansible.modules.network.f5.bigip_policy_rule import ModuleManager
           from ansible.modules.network.f5.bigip_policy_rule import ArgumentSpec
           from ansible.module_utils.network.f5.common import F5ModuleError
           from ansible.module_utils.network.f5.common import iControlUnexpectedHTTPError
           from units.modules.utils import set_module_args
       except ImportError:
           raise SkipTest("F5 Ansible modules require the f5-sdk Python library")

The purpose of this import block is the same as the purpose of a similar import block that
existed in the actual module code. The content in the ``try`` section attempts to import
development code (code in the f5-ansible Github repository) and if that fails, it will attempt
to load product code (code in the upstream Ansible Github repository).

This differentiation is used by the F5 module developers to allow for development out-of-band
of the upstream Ansible product.

Therefore, this import block serves a similar purpose to the module's block. The major difference
is that the things that are imported are different. The unit test is interested in importing
the classes that are defined in the module. It will test these classes later.

.. note::

   An ongoing disagreement exists among developers as to what constitutes a "unit" for test.
   F5 considers the "unit" under test **the class**, not **the methods of the class**.

Fixture setup
`````````````

After the import block, the fixture setup block can be found. It is implemented like so.

.. code-block:: python

   fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
   fixture_data = {}


   def load_fixture(name):
       path = os.path.join(fixture_path, name)

       if path in fixture_data:
           return fixture_data[path]

       with open(path) as f:
           data = f.read()

       try:
           data = json.loads(data)
       except Exception:
           pass

       fixture_data[path] = data
       return data

The first assignment in this block is used to declare two things:

* Where the fixtures can be found
* A cache for the fixtures to prevent re-reads from disk

After the assignment statements comes the definition of the ``load_fixture`` function. This
function is what is responsible for using the two assignments above.

Parameter unit tests
````````````````````

The first set of unit tests that are stubbed (and the tests which are likely to be written
first) are the ``Parameters`` class unit tests.

The parameters tests are typically defined by a class named ``TestParameters``. The purpose of
this class is to test the different combinations of arguments that one can send to the different
parameter classes (``ApiParameters`` and ``ModuleParameters``).

Usually, you will provide the class an argument, and then assert that some property of the
``Parameters`` class is equal to an expected value.

Using the module being developed as an example, refer to the code below.

.. code-block:: python

   def test_module_parameters_policy(self):
       args = dict(
           policy='Policy - Foo'
       )
       p = ModuleParameters(params=args)
       assert p.policy == 'Policy - Foo'

As stated previously, the test sets some property to some known value. It then creates an
instance of the ``Parameters`` class under test--in this case ``ModuleParameters``. It provides
the defined arguments to this class in the same way that the Ansible module does.

Finally, it performs an assertion to check that some expected ``@property`` is equal to some
expected value.

All of the ``Parameter`` tests resemble this format.

F5 imposes no limit on the number of tests you are allowed to write. The general rule of thumb
is to follow code-coverage reports to determine what tests are missing.

ModuleManager unit tests
````````````````````````

The second set of unit tests that will be stubbed out are the ``ModuleManager`` tests. There
may be either a single class, or multiple classes, for testing the module manager(s). For
instance, if the Ansible module under test is a factory module (such as several GTM modules)
there may be two classes for module manager tests.

The basic definition of a ``ModuleManager`` test class is shown below.

.. code-block:: python

   class TestManager(unittest.TestCase):

       def setUp(self):
           self.spec = ArgumentSpec()

In the above stub, a method names ``setUp`` is defined. This is typical of all manager test
classes. The job of this method is to, (according to the `unittest documentation`_)

...define instructions that will be executed before and after each test method

In this case, the unit tests will require an ``ArgumentSpec`` definition before they can run.
By putting this definition here, it can be used in all of the remaining unit tests in the class.

Actual tests
````````````

The actual unit tests of the ``ModuleManager`` should include (at a minimum) the following
tests:

* A creation test
* An update test
* A deletion test
* An idempotent creation test
* An idempotent update test
* An idempotent deletion test

You are unlikely to find all of these tests for every module that exists, but it is still a goal
of module development to produce this minimum set of tests.

Below is the implementation of a creation test.

.. code-block:: python

   def test_create_policy_rule_no_existence(self, *args):
       set_module_args(dict(
           name="rule1",
           state='present',
           policy='policy1',
           actions=[
               dict(
                   type='forward',
                   pool='baz'
               )
           ],
           conditions=[
               dict(
                   type='http_uri',
                   path_begins_with_any=['/ABC']
               )
           ],
           password='password',
           server='localhost',
           user='admin'
       ))

       module = AnsibleModule(
           argument_spec=self.spec.argument_spec,
           supports_check_mode=self.spec.supports_check_mode
       )

       # Override methods to force specific logic in the module to happen
       mm = ModuleManager(module=module)
       mm.exists = Mock(return_value=False)
       mm.publish_on_device = Mock(return_value=True)
       mm.draft_exists = Mock(return_value=False)
       mm._create_existing_policy_draft_on_device = Mock(return_value=True)
       mm.create_on_device = Mock(return_value=True)

       results = mm.exec_module()

       assert results['changed'] is True

The basic design of a test follows these steps:

- Define some parameters using ``set_module_args``
- Create an instance of ``AnsibleModule``
- Create an instance of ``ModuleManager``
- Stub out all of the methods that communicate with the API using simple ``Mock`` classes
- Call ``exec_module`` to drive the test
- Assert changes on the result

Most of the above is self-explanatory, but the fourth item on the list warrants some explanation.

The purpose of the F5 Ansible module unit tests is to confirm that:

- a series of arguments
- invokes a known series of methods
- to produce a known result

That's it. You do not need to mock the actual API calls. The best way to test actual API calls is via functional tests.

Therefore, to put it simply, the F5 module unit tests are there to test drive code
execution paths.

Using the above as an example, given the parameters that are set, if the ``Mock``ed calls are
called during execution of the module, then the module will logically return the asserted
result.

If, however, a problem exists in the logic of the module such that a different code path
is taken than expected, then ``pytest`` will fail because it will attempt to call an API
method. This failure should pique your interest because it means there is a bug in the module.

Unit tests are meant to confirm code path execution. Nothing more.

Conclusion
----------

This section introduced you to tests, showed how and where they are laid out, and introduced
you to writing two forms of test: a ``Parameters`` test and a ``ModuleManager`` test. With these
tools, the remainder of the work falls on the shoulders of the developer. Ansible **will**
run these tests as part of their basic test suite. Therefore, it is important that they are:

* Correct
* Fast

*Hundreds* of tests exist in the F5 Ansible code-base. If the F5 unit tests are slowing down the
total execution time of the test suite (beyond reason of course) then this should be
considered a bug and fixed.

In the next section, the concept of integration tests will be explored in greater depth.
Integration tests are the most important tests that can be run because they confirm or reject
the correctness of a module.

.. _can be found here: https://github.com/ansible/ansible/blob/stable-2.5/lib/ansible/modules/network/f5/bigip_policy_rule.py
.. _load_ltm_policy_draft_rule_http-uri_forward.json: https://github.com/ansible/ansible/tree/stable-2.5/test/units/modules/network/f5/fixtures/load_ltm_policy_draft_rule_http-uri_forward.json
.. _pytest: https://docs.pytest.org/en/latest/
.. _unittest documentation: https://docs.python.org/2/library/unittest.html
