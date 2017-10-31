Filing Issues
=============

Issues, you'll inevitably run into them. The F5 Module developers are only human (though lauded as superhuman at times)
and therefore we are bound to make mistakes. When we do, it is incumbent upon you, the reader, to call us to task to
fix these issues. Let's look more at what it takes to file a good, high quality issue, that will allow us to triage
the problem as quickly as possible and get to a solution.

Be verbose
----------

When you file an issue with the F5 Ansible modules, we will present you with an Issue template. In it we will ask you
questions about your environment, what F5 product and version you are using, etc.

What we're really interested in here is gathering information so that we can reproduce your environment. We refer to
this reproduction as a "repro". For us to be successful in repro'ing your issue, we need...no, fanatically demand!...
information about your environment. The more the merrier...to a degree.

Some things we want to know are

* What F5 product?
* What version of that product?
* What Ansible version?
* What python version?
* Whether or not you are using a module in Ansible upstream or one directly from this repo (we have hashes for this)
* Ansible plays that reproduce the problem
* If this is a feature request, `tmsh` commands that can be used to meet your needs
* If this is a feature request for a module, an example (in your own YAML) what you think the parameters to the
  module would look like.
* Whether you have uploaded a qkview to F5 (we will ask you to contact us offline if you have so we can find your
  account)

and the list goes on and on. It all helps, us get a better idea of how your device is configured and how your Ansible
environment is configured.

Some of the things that we **do not** want, and will **never** ask for are

* passwords
* license keys
* for you to **publicly** disclose your company or company contact info. We may as you to contact us "offline"
  though.

Do not comment on closed issues
-------------------------------

I need to harp on this because this is something that some people do...and it's not something you should do.

Two things happen when you comment on closed issues

- We can't repro is properly in our code-base
- We don't usually see the notification for it

Let's take a moment to illustrate why commenting on old issues is a problem for our code base.

You see, when you open an Issue with us, we will create new files in the integration test directory that
are named after your issue.

For example, if you open an issue and it is given the number 1234, then we will create an `issue-01234.yaml`
in our source tree. This file is related to your issue and no other issues. It is where we, the developers,
will work to ensure that your problem is solved and that we have a historical record of your problem so that
all future work we do on the F5 Ansible modules will continue to work for whatever problem it is that we
solved.

This is our means by which we repro your issue, or (in technical mumbo-jumbo) "create a repro" of your
issue.

If you do not create a **new** issue, then this who process is thrown into chaos. We would need to re-visit
old stuff and make changes to previously working code. We would now have a conflict where-by we wouldnt know
which issue this code was meant to fix. We wouldn't have a clean repro that we could archive as time went on,
etc etc etc.

Plain and simple, **do not** comment on closed issues.
