Getting involved
================

So you want to get involved with this project. Great!

Becoming involved in this project can take a variety of angles. The
maintainers spend their time camping this repository as well as contributing
upstream to the Ansible core product. We can be reached on either forum.

Before you jump feet first in to coding, let me give you some idea of the
workload involved in module development. This is not intended to scare
you away, but only to set your expectations.

What is expected from you
-------------------------

First and foremost, we expect you to *bring a good attitude*. These modules
are developed out of our own personal interests in Ansible; there is
no official team here.

With that said, we want to keep the environment from getting bogged down
in a bad mood.

The development of a module will require some effort on your part. Often
times the countless reviews might seem frustrating, but believe us, we do
it for good reason.

By becoming involved with developing a module, you're accepting that your
contribution will probably not be accepted right off the bat. If you're
willing to work with us though, and understand the direction we're headed
in, you will more than likely find your module landing here.

We expect that you *stay up to date* with the documentation of this site
concerning module development. As time goes on, things change and new
practices are adopted. As this happens, we try to keep the documentation
up to date with these changes.

If you develop a module use an out-of-date convention, we will tell you
so upon review. It is then expected that you take the initiative to fix
it.

Part of Ansible's requirements for this is that the people listed in
the author field (usually those who wrote the module) take responsibility
for the ongoing maintenance and support of the module.

Understandably this might be a big issue for you, so we are offering to
assist. When your module is merged to our repo here, we lists ourselves
as one of the authors of the code.

With this in place, and with the addition of us opening the PR with Ansible
upstream, we think this will be sufficient to meet their needs for ongoing
maintenance. This is a joint effort though, so lets work together to ensure
that the module stays in Core. Modules that can no longer be supported
by their authors are removed from Ansible.

What to work on
---------------

While module development is the primary focus of most contributors, it's
understandable that you may not know how to write Python, or may not have
any interest in writing code to begin with.

That's ok. Here are some existing things you can do to assist.

Documentation
~~~~~~~~~~~~~

This is always needed. I write documentation that focuses on many of the
moving parts here, but I can't cover it all and will inevitably miss things.

Submitting documentation improvements is encouraged.

Unit tests
~~~~~~~~~~

The unit tests in the `test/` directory can always use more love. Unit
tests run fast and so more of them is not a burden on the test runner.

Add more test cases for your particular usage scenarios or any scenarios
that may have been missed.

I personally only add enough unit tests to be reasonably comfortable that
the code will execute right. This, unfortunately, does not cover many of
the functional test cases. So writing unit test versions of functional
tests is of huge benefit.

New module ideas
~~~~~~~~~~~~~~~~

We don't have modules to cover all of the ways our products are used.
If you find that a module is missing from the repo and you think needs
to be added, I will entertain those ideas on the Github Issues page

New functionality for an existing module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Even the existing modules do not cover all the bells and whistles that
customers use.

If a module is missing a parameter that you think it should have, raise
and issue and we will consider it.

Postman collections
~~~~~~~~~~~~~~~~~~~

The Ansible modules make use of the F5 Python SDK for all of their work.
In the SDK, all work is accomplished via the product REST APIs and this
just happens to fit in perfectly with the tool Postman.

If you want to help us work on new modules without involving yourself
in Python code, a great way to start is to write Postman collections
for the APIs that configure on the BIG-IP what you want to configure.

If you provide us with the Postman collections, this makes it really
easy for us to write the Ansible module itself.

This is the approach that many of the F5 teams who do not work in
software land all day long take because it is super effective. Bonus
points for collections that address differences in APIs between
versions of BIG-IP

Finding bugs (via usage)
~~~~~~~~~~~~~~~~~~~~~~~~
Using the modules is the best way to iron out bugs. By using the modules
in the way that **you** expect them to work is a great way to find bugs.

During the development process, we write tests with specific user personas
in mind. Your usage patterns may not reflect those personas though and
that might break the module.

Using the modules is the best way to get both code and documentation
correct. If it's not obvious to you via the documentation about how a
module works, then I guarantee it is unclear to many more people.

Righting those wrongs helps you and future users.

More example playbooks
~~~~~~~~~~~~~~~~~~~~~~

Playbooks show people how to make use of the module when paired with
other modules. Playbooks also are the way that people inevitably use
all these modules, so if you write playbooks that make use of them,
this allows people to copy/paste the actual usage for their own benefit.

More roles for f5devcentral
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ansible's role features provide the opportunity for us to build new
sets of configuration for an F5 product.

There has been some effort to begin writing role that would be useful
for different scenarios (such as the `bigip-hardening` role) but this
effort has not been fully tackle yet.

Anyone can write roles as they are just collections of files, templates,
modules, and tasks that you are already writing for some purpose.

Writing more roles helps spread the usage of the modules.

More ways if you're at F5
~~~~~~~~~~~~~~~~~~~~~~~~~

If you're an F5 employee, there are even more ways to help. Refer to
the *go/ansible* link for more details.

Keeping F5 out of "legacy" files
--------------------------------

When Ansible introduces some new check that causes a whole lot of errors
(such as when they added pep8 checking) they put all of the findings in
a legacy file and fix the code that they're interested.

On one hand, this allows them to fix what they need to fix.

On the other hand, it results in problems like this

.. code-block:: bash

   ERROR: build/lib/ansible/modules/system/capabilities.py:139:55: E202 whitespace before ']'
   ERROR: build/lib/ansible/modules/system/capabilities.py:166:1: E302 expected 2 blank lines, found 1
   ERROR: build/lib/ansible/modules/system/capabilities.py:170:22: E251 unexpected spaces around keyword / parameter equals
   ERROR: build/lib/ansible/modules/system/capabilities.py:170:24: E251 unexpected spaces around keyword / parameter equals
   ... 10,000+ lines here ...
   ERROR: build/lib/ansible/playbook/base.py:450:28: E225 missing whitespace around operator
   ERROR: build/lib/ansible/playbook/base.py:452:28: E225 missing whitespace around operator
   ERROR: The 1 sanity test(s) listed below (out of 1) failed. See error output above for details.

It turns out that there is some post-processing that happens to whittle
down this huge list. What is post-processed is enumerated here

* local/ansible/test/sanity/pep8/legacy-ignore.txt

While this ends up limiting the amount of errors that are raised by automated
testing, it also puts a bandage over the problem without fixing the actual
problems.

I consider this a poor excuse for a "fix". So it's your, or *our*, job to make
sure that F5 *anything* never makes it in this list. But it doesn't stop there.

As a good netizen, it is also your job to assist in eliminating these legacy
files (the text files, not the modules) by **FIXING** all the errors that are
raised.

Ultimately, this makes F5's job easier because when we run the commands to check
for this stuff, we're no longer seeing a hundred-bajillion errors being raised
by their tools.

Conclusion
----------

One final thing that will require effort on your part that, frankly, we
cannot help with, is that of endorsement.

The Ansible work here is by no means supported by F5. If you want that to
change, then you will need to initiate that change. Speaking with your SEs,
AMs, SAs, etc etc, is the best way to drive that change.

When we run our mouths about orchestration tools, it falls on deaf ears.
If this is valuable to your organization, then say so.
