EXAMPLES variable
=================

The EXAMPLES variable contains the most common use cases for this module.

Setting the banner is the most common case, but you are free to add to these examples.

These examples also serve as a basis for the functional tests.

For this module, the ``EXAMPLES`` variable looks like this:

.. code-block:: python

   EXAMPLES = '''
   - name: Set the banner for the SSHD service from a string
     bigip_device_sshd:
       banner: enabled
       banner_text: banner text goes here
       password: secret
       server: lb.mydomain.com
       user: admin
     delegate_to: localhost

   - name: Set the banner for the SSHD service from a file
     bigip_device_sshd:
       banner: enabled
       banner_text: "{{ lookup('file', '/path/to/file') }}"
       password: secret
       server: lb.mydomain.com
       user: admin
     delegate_to: localhost

   - name: Set the SSHD service to run on port 2222
     bigip_device_sshd:
       password: secret
       port: 2222
       server: lb.mydomain.com
       user: admin
     delegate_to: localhost
   '''

This variable should go **after** the ``DOCUMENTATION`` variable.

The examples that you provide should always have the following:

**delegate_to: localhost**

You should run the BIG-IP modules on the Ansible controller only. The best practice is to
use ``delegate_to:`` here so that you get in the habit of using it.

**common args**

The common args are:

- ``password`` should always be ``secret``
- ``server`` should always be ``lb.mydomain.com``
- ``user`` should always be ``admin``
