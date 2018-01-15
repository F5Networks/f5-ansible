Get Help
========

F5 Ansible modules are not currently supported by F5 Technical Support.

However, F5 provides informal support through a number of channels.

File an issue
-------------

If you need help with anything related to the F5 Modules for Ansible, you should open an issue |github_issue|.

.. |github_issue| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible/issues" target="_blank">on GitHub</a>

When communicating with F5 on the Issues page, use the GitHub user interface, rather than email.

For best practices, see :doc:`Filing issues <filing-issues>`.

Get community support on Slack
------------------------------

We encourage you to use |slackansible| for discussion and assistance on the F5 Modules for Ansible.

F5 employees are members of this community and typically monitor the channel Monday-Friday 9-5 PST. They will offer best-effort assistance.

.. |slackansible| raw:: html

   <a href="https://f5cloudsolutions.slack.com" target="_blank">the F5 Ansible channel on Slack</a>

Send email
----------

Contact us at solutionsfeedback@f5.com for general feedback or enhancement requests.

Exposing confidential information
---------------------------------

When submitting a request for help or feedback, you should NEVER:

- Enter any private or personally identifying information about you, your network, organization, etc.
- Enter any passwords/credentials, logs, IP addresses, or servers/server ports.
- Expect that F5 Technical Support will reply to your request. They will not.
- Expect that an F5 employee will immediately respond. Employees offer best-effort assistance, but there may be times when responses are delayed.

If you need more in-depth technical assistance, you can ask us to contact you privately.

Supported BIG-IP versions
-------------------------

The F5 Modules for Ansible are supported on BIG-IP VE versions later than 12.0.0.

For a detailed list of BIG-IP VE versions that are currently supported, see |k5903|.

.. |k5903| raw:: html

   <a href="https://support.f5.com/csp/article/K5903" target="_blank">this solution article</a>

When a version of BIG-IP reaches end of technical support, it is supported until the next Ansible release.

For example, if a version of BIG-IP reaches end of technical support on January 1, and Ansible releases a new version on March 1, then the F5 Modules for Ansible are supported on that version of BIG-IP until March 1.

F5 does not back-port changes to earlier versions of Ansible.

F5 develops the Ansible modules in tandem with the REST API, and newer versions of BIG-IP provide better support for the REST API.

Supported modules
-----------------

F5 modules are included when you install Ansible. These modules are informally supported by F5 employees.

F5 modules are also in the |github_repo|. These modules are also informally supported by F5 employees, but you should consider these modules to be experimental and not production-ready.

However, if the module's DOCUMENTATION block has a completed ``Tested platforms`` section, then the module is likely complete and ready for use. You can file bugs against modules that are complete.

.. code-block:: python

   # Tested platforms:
   #
   #    - 12.0.0
   #

.. |github_repo| raw:: html

   <a href="https://github.com/F5Networks/f5-ansible/issues" target="_blank">F5 GitHub repository</a>
