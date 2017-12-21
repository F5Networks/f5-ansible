Filing issues
=============

If you run into any issues while working with the F5 modules for Ansible, you should submit them.

For F5 to triage as quickly as possible, please follow these guidelines.

Be verbose
----------

When you file an issue with the F5 Ansible modules, an Issue template appears.

F5 will try to reproduce your environment, so in the template, please provide as much information as possible.

Some things F5 wants to know are:

- Which F5 product
- Which version of that product
- Which Ansible version
- Which Python version
- Are you using a module in Ansible upstream or one directly from this repo (there are hashes for this)
- Which Ansible plays reproduce the problem
- If this is a feature request, which `tmsh` commands meet your needs
- If this is a feature request for a module, provide an example (in your own YAML) and what you think the parameters to the would look like
- If you have uploaded a qkview to F5

The Issue template asks these questions.

If the issue seems to be a bug, add the label `bug-report` to it.

Some of the things that F5 **does not** want, and will **never** ask for are:

- passwords
- license keys
- **public** disclosure of your company or company contact info


Do not comment on closed issues
-------------------------------

**Important:** Please do not comment on closed issues.

When you comment on closed issues:

- F5 cannot reproduce the issue properly in the code base.
- F5 doesn't usually receive the notification for it.

Why is commenting on old issues a problem for the code base?

When you open an issue, F5 creates new files with your issue name in the integration test directory.

For example, if you open an issue and give it the number 1234, then F5 creates `issue-01234.yaml` in the source tree. This file is specific to your issue and no other issues.

When the F5 developers solve the problem, they ensure that future F5 Ansible modules continue to work.

If you do not create a **new** issue:

- F5 might accidentally change code that was already working.
- It is harder to track which issue any new code relates to.
- It is harder to repro other issues over time.

Because of this, F5 asks that you not comment on closed issues.
