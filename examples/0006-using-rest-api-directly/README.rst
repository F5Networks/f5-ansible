Use the REST API directly
=========================

This playbook example shows how to use native Ansible modules to use the REST API directly.

There may be reasons you want to interact with the REST API directly, and Ansible caters to your desire to do this. However, the REST API is a work in progress; you may encounter issues with the methods in this playbook, and F5 does not support them.

The REST APIs change between versions of BIG-IP. Keep this in mind if you upgrade your BIG-IPs or if you use the `uri`_ module directly against multiple, varied versions of BIG-IP. For this situation, F5 recommends you use the ``bigip_facts`` module to at least get the current version so that you can use ``when`` conditionals on your tasks as needed.

If you find yourself using the method illustrated in this playbook, consider filing an issue and requesting to have a module developed to handle your use case.

Authentication
--------------

The secret to using the REST API with the F5 Modules for Ansible is to first authenticate to it and get a token. From that point on, all further operations should use that token.

Default lifetime of a token is 20 minutes. After that, you will need to re-auth to get a new token.

For more information about the iControl REST API:

* https://devcentral.f5.com/wiki/iControl.HomePage.ashx

Notes
-----

You assume the following risks when you use the REST API directly.

* The attributes for the different REST API resources are documented here:
  https://devcentral.f5.com/wiki/iControlREST.APIRef.ashx. This content,
  however, does not indicate which version the particular API refers to.

* Some REST API resources support an "example" suffix. This can be helpful for determining
  attributes for specific versions of BIG-IP.
  https://devcentral.f5.com/wiki/iControlREST.iControlRestUserGuide_v1300_10.ashx

* If you use the ``uri`` module, you will have no ability to do file chunking. This means that
  you cannot upload files.

* The REST API is always truthy. You will find attributes that, instead of being boolean False
  and True, will always be boolean True and the attribute name will change to accommodate this.
  For example ``vlansDisabled: true``, ``vlansEnabled: true``.

* Not all APIs support the common HTTP verbs (GET, POST, PUT, PATCH).

* The ``generation`` attribute of a resource may not be reliable.

* Local Traffic Policy APIs changed in 12.1.x to require the use of Draft policies.
  GTM APIs changes in 12.x to support a new schema for additional record types, and OCSP
  stapling APIs changed in 13.x. Be sure to test any playbooks that use the iControl REST
  API directly to ensure consistent behavior between versions.

* You cannot ``DELETE`` a collection. For example, do not send a ``DELETE`` to
  ``/mgmt/tm/ltm/virtual`` and expect it to delete all the virtuals. It will not.

* You must delete all objects that depend on an object before you can delete the object
  itself. For example, it is difficult to delete a partition that has been used for
  any moderate period of time, because you need to know all the resources that exist in
  the partition and delete them first.

* It's not possible to trace all of an object's dependencies. Therefore, you cannot know
  which other objects use the object in question without querying every API endpoint and
  comparing.

* Some API URLs include redundant information (such as pool members repeating the partition
  name in its self link). Using the pool members example, refer to the URL
  ``/mgmt/tm/ltm/pool/~Common~my-pool/members/~Common~1.1.1.1:80``. Note the duplicate
  (but required) mention of ``~Common``.

* Resource names translate forward slashes to tilde. Therefore, / becomes ~.
  For example, ``~Common~my-pool``.

* You must delete your token after you are done with your work. iControl REST only supports
  a limited number of active tokens. If you exceed this number, you will get an error of
  "maximum active login tokens" and no longer be able to create new tokens until you delete
  existing tokens. https://devcentral.f5.com/wiki/iControl.Authentication_token_resource_API.ashx

* Certain modules have further limitations. For example:

  * APM has no REST API exposure. Therefore, you cannot configure it with the ``uri`` module.
  * ASM has concurrency limitations, therefore, you cannot run many ASM REST calls concurrently.

* While most APIs are synchronous, several are asynchronous. Therefore, you must use
  subsequent Ansible tasks to poll for their status and make use of Ansible's ``retries``
  and ``delay`` attributes.

* All of BIG-IQ's APIs are asynchronous. It is your job to use them in a synchronous way
  by polling.

* Some APIs reference resources at other APIs (such as LTM virtuals referencing LTM
  profiles). In many cases, in the first API, there is no indication where in the API the
  second resource is. For example, in virtuals, LTM profiles will list the profile name
  ``/Common/foo``, but it will not tell you that it is a ``diametersession`` profile.

* The full API encompasses nearly 2500+ URLs.

* Some resources in specific modules (ASM in particular) use uuids in their URLs instead
  of names. Therefore you will need to keep track of the human-readable names in another
  medium so that you can keep track of what is required.

* Some of the API resources must be updated by doing a ``PUT`` to their resources reference,
  the full payload, instead of updating individual attributes. For example, LTM policy
  conditions and actions have an ``actionsReference`` attribute that refers to a
  ``/actions`` URL. You may not update any resources at that URL though. For example, if
  there were a ``foo`` action with a selfLink that ended in ``/actions/foo``, you would not
  be able to update its attributes. If you want to change the actions, you must put ALL
  the actions new and only to the ``/actions`` URL.

* **All** of the ``selfLink`` attributes start with ``https://localhost/`` regardless of
  whether your BIG-IP is actually named that or not.

* Many resources have a ``/stats`` URL associated with them. This resource is a deeply
  nested combination of lists and dicts.

* Some resources that appear to be resources are actually links to stats APIs, even if
  the URL does not end with ``/stats``. For example, ``/mgmt/tm/cm/failover-status`` or
  ``/mgmt/tm/sys/version``.

* All of the BIG-IQ APIs as of 5.4.0 will raise an exception if navigating to a URL that
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
