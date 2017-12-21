Getting involved
================

Thank you for getting involved with this project.

You can contribute in a number of different ways.

Before you jump feet first into coding, here is some information that can help set your expectations.

Developing and supporting your module
-------------------------------------

When you develop a module, it goes through review before F5 accepts it. This review process may be difficult at times, but it ensures the published modules are good quality.

You should *stay up to date* with this site's documentation about module development. As time goes on, things change and F5 and the industry adopt new practices; F5 tries to keep the documentation updated to reflect these changes.

If you develop a module that uses an out-of-date convention, F5 will let you know, and you should take the initiative to fix it.

Ansible requires that the people listed in the author field (usually those who wrote the module) take responsibility for the ongoing maintenance and support of the module.

Understandably, this might be a big issue for you, so when your module merges to the F5 repo, F5 becomes one of the authors of the code.

With F5 as the co-author and F5 opening the PR with Ansible upstream, this should meet Ansible's needs for ongoing maintenance.

This is a joint effort though, so let's work together to ensure that the module stays in Core. Ansible removes modules that the authors can no longer support.

What to work on
---------------

While module development is the primary focus of most contributors, it's understandable that you may not know how to write Python, or may not have any interest in writing code to begin with.

That's OK. Here are some things you can do to assist.

Documentation
`````````````

Documentation help is always needed. F5 encourages you to submit documentation improvements.

Unit tests
``````````

The unit tests in the `test/` directory can always use work. Unit tests run fast and are not a burden on the test runner.

F5 encourages you to add more test cases for your particular usage scenarios or any other scenarios that are missing tests.

F5 adds enough unit tests to be reasonably comfortable that the code will execute correctly. This, unfortunately, does not cover many of the functional test cases. Writing unit test versions of functional tests is hugely beneficial.

New modules
```````````

Modules do not cover all of the ways you might use F5 products. If you find that a module is missing from the repo and you think F5 should add it, put those ideas on the Github Issues page.

New functionality for an existing module
````````````````````````````````````````

If a module is missing a parameter that you think it should have, raise the issue and F5 will consider it.

Postman collections
```````````````````

The Ansible modules make use of the F5 Python SDK. In the SDK, all work is via the product REST APIs. This just happens to fit in perfectly with the Postman tool.

If you want to work on new modules without involving yourself in Python code, a great way to start is to write Postman collections for the APIs that configure BIG-IP.

If you provide F5 with the Postman collections, F5 can easily write the Ansible module itself.

And you get bonus points for collections that address differences in APIs between versions of BIG-IP.

Bugs
````

Using the modules is the best way to iron out bugs. Using the modules in the way that **you** expect them to work is a great way to find bugs.

During the development process, F5 writes tests with specific user personas in mind. Your usage patterns may not reflect those personas.

Using the modules is the best way to get good code and documentation. If the documentation isn't clear to you, it's probably not clear to others.

Righting those wrongs helps you and future users.

Example playbooks
`````````````````

Playbooks show you how to make use of a module when paired with other modules. Playbooks also are the way that people inevitably use all of these modules, so if you write playbooks that make use of them, people can copy/paste the actual usage for their own benefit.

Roles for F5 DevCentral
```````````````````````

Ansible roles provide the opportunity to build new sets of configurations for an F5 product.

Anyone can write roles. They are just collections of files, templates, modules, and tasks that you are already writing for some purpose.

Writing more roles helps spread the usage of the modules.


Keeping F5 out of "legacy" files
--------------------------------

When Ansible introduces a new check that causes a lot of errors (such as when they added pep8 checking), they put the findings in a legacy file and fixed the specific code.

On one hand, this allows Ansible to fix what they need to fix.

On the other hand, it results in problems like this:

.. code-block:: bash

   ERROR: build/lib/ansible/modules/system/capabilities.py:139:55: E202 whitespace before ']'
   ERROR: build/lib/ansible/modules/system/capabilities.py:166:1: E302 expected 2 blank lines, found 1
   ERROR: build/lib/ansible/modules/system/capabilities.py:170:22: E251 unexpected spaces around keyword / parameter equals
   ERROR: build/lib/ansible/modules/system/capabilities.py:170:24: E251 unexpected spaces around keyword / parameter equals
   ... 10,000+ lines here ...
   ERROR: build/lib/ansible/playbook/base.py:450:28: E225 missing whitespace around operator
   ERROR: build/lib/ansible/playbook/base.py:452:28: E225 missing whitespace around operator
   ERROR: The 1 sanity test(s) listed below (out of 1) failed. See error output above for details.

It turns out that there is some post-processing that whittles down this huge list. Here is what is post-processed:

- local/ansible/test/sanity/pep8/legacy-ignore.txt

While this limits the number of errors that automated testing raises, it does not fix the core problem.

It is everyone's job to make sure that anything from F5 never makes it on this list. But it doesn't stop there.

It is also your job to assist in eliminating these legacy files (the text files, not the modules) by **FIXING** all the errors that running the code raises.

Ultimately, this makes F5's job easier because when F5 runs the commands to check for this stuff, F5 no longer sees a large number of errors raised by their tools.
