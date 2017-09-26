Running tests
=============

These tests require a number of variables that are unset and require that you set them before
proceeding. Those variables are

* iso_base
* iso_hotfix
* image_link
* hotfix_link
* image_md5
* hotfix_md5

The tests associated with this module will fail unless **ALL** of these values are overwritten
by values custom to your environment.

And before you ask, if your organization happens to use the actual default we have, **no** we
won't change them.

File locations
==============

When it comes to testing, we usually put the files to test in the local `files` or `templates`
directory relative to the role. Therefore, we have created a set of `.example` files for you
and placed them in the `files` directory.

For your own tests, it will be expected that you either

- Replace the files there with the "real" files
- Provide correct paths when running the testing command shown later in this document

Example test command
====================

The following is an example of a way to override all the values with your custom values.

Note the inclusion of ISO files placed in the `files/` directory. This follows standard
practice for F5 module development.

.. code-block:: bash

   ansible-playbook -i inventory/hosts bigip_software.yaml \
       -e "iso_base={{ role_path }}/files/BIGIP-12.1.1.0.0.184.iso" \
       -e "iso_hotfix={{ role_path }}/files/Hotfix-BIGIP-12.1.1.1.0.196-HF1.iso" \
       -e "image_link=http://server.company.org/12.1.2.iso" \
       -e "hotfix_link=http://server.company.org/12.1.2-HF1.iso" \
       -e "image_md5=http://server.company.org/12.1.2.iso.md5" \
       -e "hotfix_md5=http://server.company.org/12.1.2-HF1.iso.md5"

Excluding remote tests
======================

If you do not have a server available to host images required by the `remote` tests, you can
exclude running those tests by adding the `limit_to` argument and supplying the value
`local`. For example

.. code-block:: bash

   ansible-playbook -i inventory/hosts bigip_software.yaml \
       -e "iso_base={{ role_path }}/files/BIGIP-12.1.1.0.0.184.iso" \
       -e "iso_hotfix={{ role_path }}/files/Hotfix-BIGIP-12.1.1.1.0.196-HF1.iso" \
       -e "limit_to=local"

Note that you are still required to provide the arguments for local testing.
