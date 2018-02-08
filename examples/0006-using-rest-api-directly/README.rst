Using the REST API directly
===========================

This Playbook provides an example of how one can use native Ansible modules to
use the REST API directly.

There may be reasons for which you want to do this, and Ansible caters to your
desire to do this. Beware however, that the REST API is the "Wild West" of ways
to interact with your BIG-IP. You will likely encounter quirks.

The F5 Modules for Ansible maintainers **cannot** help you if you encounter a
problem while using the method described in this playbook.

The secret to using the REST API in Ansible is that you must first authenticate
to it and get a token. From that point on, all further operations should use that
token.

Default lifetime of a token is 20 minutes. After that, you will need to re-auth
to get a new token.

APIs change between versions so, in some sense, there is a large risk to using
the REST APIs directly if you will be upgrading your BIG-IPs, or, be using the
`uri`_ module directly against a number of BIG-IPs that vary in version. For
this situation, it is recommended that you use the ``bigip_facts`` module to
at least get the current version so that you can use ``when`` conditionals on
your tasks as needed.

If you find yourself using the method illustrated in this playbook, consider
filing an issue to have a real module developed to handle your use case.

Additional resources on using the iControl REST API

* https://devcentral.f5.com/wiki/iControl.HomePage.ashx

Please note
-----------

The following are things you **must** be aware of when following this technique.
These are all risks that you accept by using the REST API directly.

* The attributes for the different rest API resources is, at best, documented here
  https://devcentral.f5.com/wiki/iControlREST.APIRef.ashx. This series of pages,
  however, does not tell you which version the particular API refers to.

* Some rest API resources support a "example" suffix.  This can be helpful for determining
  attributes for specific versions of BIG-IP.
  https://devcentral.f5.com/wiki/iControlREST.iControlRestUserGuide_v1300_10.ashx

* Using the ``uri`` module, you will have no ability to do file chunking. This means that
  you cannot upload files.

* The REST API is always truthy. Therefore you will find attributes that, instead
  of being boolean False and True, will always be boolean True and the attribute name
  will change to accommodate this. For example ``vlansDisabled: true``, ``vlansEnabled: true``.

* Not all APIs support the common HTTP verbs (GET, POST, PUT, PATCH)

* Never trust the ``generation`` attribute of a resource.

* The iControl REST API can have breaking changes between versions.  Examples are Local Traffic
  Policy support of Draft policies in 12.1.x, GTM APIs changes in 12.x to support a new schema
  for additional record types, OCSP stapling APIs changed in 13.x.  Be sure to test any playbooks
  that uses iControl REST API directly to ensure consistent behavior between versions.

* You cannot ``DELETE`` a collection. For example, do not send a ``DELETE`` to
  ``/mgmt/tm/ltm/virtual`` expecting it to delete all the virtuals. It will not.

* You must delete all objects that depend on an object before you can delete the object
  itself. For example, it's nearly impossible to delete a partition that has been used for
  any moderate period of time, because you need to know all the resources that exist in
  the partition and delete them first.

* It's not possible to trace all of an objects dependencies. Therefore, you cannot know
  what other objects use the object in question, without querying every API endpoint and
  comparing.

* Some API URLs include redundant information (such as pool members repeating the partition
  name in it's self link). Using the pool members example, refer to the illogical URL
  ``/mgmt/tm/ltm/pool/~Common~my-pool/members/~Common~1.1.1.1:80``. Note the duplication
  (bu required) mention of ``~Common``.

* Names of resources translate forward slashes to tilde. Therefore, / becomes ~.
  For example, ``~Common~my-pool``.

* You must delete your token after you are done doing your work. iControl REST only supports
  a limited number of active tokens.  If you exceed this number you will get an error of
  "maximum active login tokens" and no longer be able to create new tokens until you delete
  existing tokens.  https://devcentral.f5.com/wiki/iControl.Authentication_token_resource_API.ashx

* Certain modules have further limitations. For example,

  * APM has no REST API exposure. Therefore, you cannot configure it with the URI module.
  * ASM has concurrency limitations, therefore, you cannot run many ASM REST calls concurrently.

* While most APIs are synchronous, several are asynchronous. Therefore, you must use
  subsequent Ansible tasks to poll for their status and make use of Ansible's ``retries``
  and ``delay`` attributes.

* All of BIGIQs APIs are asynchronous. It is your job to use them in a synchronous way
  by polling.

* Some APIs reference resources at other APIs (such as LTM virtuals referencing LTM
  profiles). In many cases, there is no indication in the first API where in the API the
  second resource is. For example in virtuals, LTM profiles will list the profile name
  ``/Common/foo``, but will not tell you that it is a ``diametersession`` profile.

* The full API encompasses nearly 2500+ URLs.

* Some resources in specific modules (ASM in particular uses uuids in their URLs instead
  of names. Therefore you will need to keep track of the human readable names in another
  medium so that you remember what to access at which API.

* Some of the API resources must be updated by doing a ``PUT`` to their resources reference,
  the full payload instead of updating individual attributes. For example LTM policy
  conditions and actions. There is an ``actionsReference`` attribute that refers to a
  ``/actions`` url. You may not update any resources at that url though. For example, if
  there were an ``foo`` action with a selfLink that ended in ``/actions/foo``, you would not
  be able to update its attributes. If you want to change the actions, you must put ALL
  the actions new and only to the ``/actions`` url.

* **All** of the ``selfLink`` attributes start with ``https://localhost/`` regardless of
  whether your BIG-IP is actually named that or not.

* Many resources have a ``/stats`` URL associated with them. This resource is a deeply
  nested combination of lists and dicts. Often, it is un-intuitive to use.

* Some resources that you think are resources, are actually links to stats APIs even if
  the url does not end with ``/stats``. For example, ``/mgmt/tm/cm/failover-status`` or
  ``/mgmt/tm/sys/version``.

* All of the BIG-IQ APIs as of 5.4.0 will raise an exception if navigating to a url that
  is a collection of other child URLs. Therefore, unlike BIG-IP, you cannot walk an API
  tree by fetching the next known URL; there are no "OrganizingCollections" in BIG-IQ
  (this is a term used in the F5-SDK to refer to a collection of links).

* Some attributes cannot be set upon POST and require that you first create the
  resource in a POST and then followup with a PATCH or PUT to the attribute you
  want to set.

* Using the REST API directly is **not** idempotent. This example playbook makes use of
  fake idempotentency similar to: https://github.com/F5Networks/f5-ansible/tree/devel/examples/0004-faking-idempotency-with-bigip-command
  This is done by checking for an object before creating/deleting.

.. _F5 Python SDK: https://github.com/F5Networks/f5-common-python
.. _uri: https://docs.ansible.com/ansible/latest/uri_module.html
