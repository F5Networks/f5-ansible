Support
=======

The F5 Ansible modules are developed primarily with the REST API in mind. Due
to this requirement, we often take the approach that newer versions of BIG-IP
are those that are best supported.

The versions of BIG-IP that support these modules typically start at version
12.0.0, but may require later versions than that depending on the REST
functionality that is needed by them.

Incentives
----------

Fortunately or unfortunately, the Ansible modules are not recognized by F5 as
a supported product at this time.

Due to this constraint, you could say that the maintainers of these modules
have limited resources to focus on these full time. We do our best though,
and offload many of the more mundane tasks to automation where possible.

With those constraints in mind, we hope you can see why we are not able to
focus more on older releases of BIG-IP. Consider these modules as an incentive
to upgrade your BIG-IP to a later version.

Finding assistance
------------------

If you need help with anything related to these modules, it is recommended
that you open an issue on Github

https://github.com/F5Networks/f5-ansible/issues

We usually respond promptly and may ask you to contact us offline if we need
to deal with something that would not be appropriate on a public forum.

When communicating with us on the Issues page, we generally recommend that
you do it via Github's UI and not via email. The reason for this is that we
have seen examples where email communication may expose the name of your
company when communicating with us.

Whether your company has an issue with this or not, it's probably best if
we stay vendor neutral when discussing the technical issues on a public
forum. If you need more in-depth technical know-how, you're free to ask
us to ping you offline and we can handle things there.

Credentials and secret things
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It's considered bad form to expose credentials in a Github issue. Please
be diligent of that!

We *do not need any* of the following task arguments to debug your issue

  * user
  * password
  * server
  * server_port

therefore, please be diligent and either

  * Do not provide them (leave them empty with empty quotes "")
  * Provide placeholders for them (such as "admin", "secret", and "lb.mydomain.com")

We are very well equipped in terms of physical and virtual BIG-IPs to be able
to diagnose and test your problems. Therefore we never need this information
to provide your with assistance.