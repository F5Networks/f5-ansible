Using the REST API directly
===========================

This Playbook provides an example of how one can use native Ansible modules to
use the REST API directly.

There may be reasons for which you want to do this, and Ansible caters to your
desire to do this. Beware however, that the REST API is the "Wild West" of ways
to interact with your BIG-IP. You will likely encounter quirks.

The secret to using the REST API in Ansible is that you must first authenticate
to it and get a token. From that point on, all further operations should use that
token.

Default lifetime of a token is 20 minutes. After that, you will need to re-auth
to get a new token.

APIs change between versions so, in some sense, there is a large risk to using
the REST APIs directly if you will be upgrading your BIG-IPs, or, be using the
``uri`` module directly against a number of BIG-IPs that vary in version. For
this situation, it is recommended that you use the ``bigip_facts`` module to
at least get the current version so that you can use ``when`` conditionals on
your tasks as needed.

If you find yourself using the method illustrated in this playbook, consider
filing an issue to have a real module developed to handle your use case.

Issues
------

The following are things you **must** be aware of when following this technique.
These are all risks that you accept by using the REST API directly.

All of these issues were discovered while writing the `F5 Python SDK`_, therefore
I'm reiterating them here for your awareness. The F5 Modules for Ansible maintainers
go to great lengths to hide these issues from you in Ansible modules.

* The attributes for the different rest API resources is, at best, documented here
  https://devcentral.f5.com/wiki/iControlREST.APIRef.ashx. This series of pages,
  however, does not tell you which version the particular API refers to.

* Using the URI module you will have no ability to do file chunking this means that
  you cannot upload files.

* The REST API is always truthy. Therefore you will find attributes that, instead
  of being boolean False and True, will always be boolean True and the attribute name
  will change to accommodate this. For example ``vlansDisabled: true``, vlansEnabled: true``.

* Not all APIs support the common HTTP verbs (GET, POST, PUT, PATCH)

* Never trust the ``generation`` attribute of a resource.

* Some APIs will not work. By this I mean the values you set the attributes to will be
  invalid even if you received them in this format from the API. The classic example is
  PUTing what you GET and failing.

* Return values may or may not contain accurate information.

* GTM APIs changed in 12.x, breaking backwards compatibility.

* OCSP stapling APIs changed in 13.x, breaking backwards compatibility. This act of breaking
  backwards compatibility is not unusual.

* You cannot ``DELETE`` a collection. For example, do not send a ``DELETE`` to
  ``/mgmt/tm/ltm/virtual`` expecting it to delete all the virtuals.

* You must delete all objects that depend on an object before you can delete the object
  itself. For example, its nearly impossible to delete a partition that has been used for
  and moderate period of time because you need to know all the resources that exist in
  the partition and delete them first. And, speaking of which...

* It's not possible to trace all of an objects dependencies. Therefore, you cannot know
  what other objects use your object in question without querying every API endpoint and
  comparing by hand.

* Some API URLs include redundant information (such as pool members repeating the partition
  name in it's self link). This is not unusual across the API.

* Names of resources translate forward slashes to tilde. Therefore, / becomes ~.
  For example, ``~Common~my-pool``.

* You must delete your token after you are done doing your work. BIGIPs can run out of
  file descriptors (and kill all future API calls) if too many tokens are created. This
  limitation exists for admin accounts as well.

* Certain modules have further limitations. For example,
  * APM has no REST API exposure. Therefore, you cannot configure it with the URI module
  * ASM has concurrency limitations, therefore, you cannot run many ASM REST calls
    concurrently.

* While most APIs are synchronous, several are asynchronous. Therefore, you must use
  future tasks to poll for their status and make use of Ansible's ``retries`` and ``delay``
  attributes.

* All of BIGIQs APIs are asynchronous. It is your job to use them in a synchronous way
  by polling.

* Some APIs reference resources at other APIs (such as LTM virtuals referencing LTM
  profiles). In many cases, there is no indication in the first API where in the API the
  second resource is. For example in virtuals, LTM profiles will list the profile name
  ``/Common/foo``, but will not tell you that it is a ``diametersession`` profile. This
  is not unusual across the API.

* The full API encompasses nearly 2500+ URLs.

* Some resources in specific modules (ASM in particular uses uuids in their URLs instead
  of names. Therefore you will need to keep track of the human readable names in another
  medium so that you remember what to access at which API.

* Some of the API resources must be updated by ``PUT``ing to their resources reference,
  the full payload instead of updating individual attributes. For example LTM policy
  conditions and actions. There is an ``actionsReference`` attribute that refers to a
  ``/actions`` url. You may not update any resources at that url though. For example, if
  there were an ``foo`` action with a selfLink that ended in ``/actions/foo`, you would not
  be able to update its attributes. If you want to change the actions, you must put ALL
  the actions new and only to the ``/actions`` url.

* **All** of the ``selfLink`` attributes start with ``https://localhost/`` regardless of
  whether your BIG-IP is actually named that or not.

* Many resources have a ``/stats`` URL associated with them. This resource is a deeply
  nested combination of lists and dicts. Often, it is very intuitive how to use. This
  is not unusual.

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

* The HTTP return code is not trustworthy. This is illustrated to great effect in the
  ``/mgmt/tm/sys/util`` suite of APIs, which will happily return one of a number of
  ``400`` errors even if they succeed.

.. _F5 Python SDK: https://github.com/F5Networks/f5-common-python
