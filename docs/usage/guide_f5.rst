:orphan: true

F5 BIG-IP Guide
===============

BIG-IP systems can inspect, secure, balance, and accelerate the traffic that passes through your network.

F5 provides modules for Ansible that you can use to deploy, provision, configure, and orchestrate BIG-IP systems. BIG-IP can be physical hardware or a virtual edition (BIG-IP VE) running in a public or private cloud.

About the API
`````````````

The primary API that's included with BIG-IP is called iControl REST. The Python library that interacts with iControl REST is called ``f5-sdk``.

To work with the F5 Modules for Ansible, you should install ``f5-sdk``, as well as:

- ``bigsuds``, the F5 SOAP API that was used for modules prior to Ansible 2.2
- ``netaddr``, which helps with address manipulation
- ``deepdiff``, to compare and find the differences between objects


For details:

- `Learn more about the f5-sdk Python library <http://f5-sdk.readthedocs.io/en/latest/userguide/index.html>`_

- `Access the f5-sdk Python library <https://github.com/F5Networks/f5-common-python>`_

- `Learn more about iControl REST <https://devcentral.f5.com/Wiki/Default.aspx?Page=HomePage&NS=iControlREST>`_


Connecting to BIG-IP
````````````````````

Any BIG-IP user with administrative rights can use the F5 Modules for Ansible.

To secure the user's password so it is not stored in plain text in your playbook or inventory file, you can use `Ansible Vault <https://docs.ansible.com/ansible/2.4/vault.html>`_.

You do not need to exchange key pairs between the machine running Ansible and BIG-IP, because the F5 modules use the API, rather than SSH, to connect.

In addition, your playbook must contain ``delegate_to: localhost``, so that the modules run locally on the machine running Ansible. Without this setting, the modules try to run on BIG-IP and fail, because the supporting Python libraries are not on BIG-IP.


Common parameters
`````````````````

Every F5 module accepts the following parameters:

server
   Host name or IP address of BIG-IP.

user
   The user who can connect to BIG-IP. This user must have administrative privileges.

password
   Password for the user. Use Ansible Vault to encrypt the password, rather than storing it as plain text in your playbook or inventory file.

validate_certs
   Use to validate self-signed SSL certificates on personally-controlled sites.


Common Tasks
````````````

Use the F5 Modules for Ansible to perform actions against BIG-IP.

For reference information for each module, see `this list <http://docs.ansible.com/ansible/latest/list_of_network_modules.html#f5>`_.

License BIG-IP
++++++++++++++

If you have a BIG-IP license, you can use Ansible to license BIG-IP. This example shows the full playbook.

.. code-block:: yaml

   ---

   - name: License BIG-IP
     hosts: f5-test
     connection: local

     vars:
         bigip_license: "XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX"

     tasks:
         - name: License BIG-IP
           bigip_license:
               server: "{{ ansible_host }}"
               user: "{{ bigip_username }}"
               password: "{{ bigip_password }}"
               validate_certs: "{{ validate_certs }}"
               server_port: "{{ bigip_port }}"
               key: "{{ bigip_license }}"
           delegate_to: localhost


Provision BIG-IP
++++++++++++++++

Then you can use Ansible to provision BIG-IP modules.

.. code-block:: yaml

     tasks:
         - name: Provision ASM at "nominal" level
           bigip_provision:
               server: "{{ ansible_host }}"
               user: "{{ bigip_username }}"
               password: "{{ bigip_password }}"
               validate_certs: "{{ validate_certs }}"
               module: asm
               level: nominal
           delegate_to: localhost

For more ideas on how you might use Ansible for initial BIG-IP setup `see this doc <https://devcentral.f5.com/codeshare/automate-f5-initial-setup-icontrol-amp-ansible-930>`_.

Create pool members, a pool, and a virtual server
+++++++++++++++++++++++++++++++++++++++++++++++++

You can use the F5 Modules for Ansible to create a pool and add members to it, and to add the pool to the virtual server.

For a full walkthrough of this example, `see this doc <http://clouddocs.f5.com/products/orchestration/ansible/devel/usage/playbook_tutorial.html>`_.

.. code-block:: yaml

     tasks:
         - name: Create a pool
           bigip_pool:
               server: "{{ ansible_host }}"
                  user: "{{ bigip_username }}"
               password: "{{ bigip_password }}"
               validate_certs: "{{ validate_certs }}"
               lb_method: "ratio-member"
               name: "web_pool"
               slow_ramp_time: "120"
           delegate_to: localhost

         - name: Create node1
           bigip_node:
               server: "{{ ansible_host }}"
               user: "{{ bigip_username }}"
               password: "{{ bigip_password }}"
               validate_certs: "{{ validate_certs }}"
               host: "10.10.10.10"
               name: "node-1"
           delegate_to: localhost

         - name: Create node2
           bigip_node:
               server: "{{ ansible_host }}"
               user: "{{ bigip_username }}"
               password: "{{ bigip_password }}"
               validate_certs: "{{ validate_certs }}"
               host: "10.10.10.20"
               name: "node-2"
           delegate_to: localhost

         - name: Add nodes to pool
           bigip_pool_member:
               server: "{{ ansible_host }}"
               user: "{{ bigip_username }}"
               password: "{{ bigip_password }}"
               validate_certs: "{{ validate_certs }}"
               description: "webserver-1"
               host: "{{ item.host }}"
               name: "{{ item.name }}"
               pool: "web"
               port: "80"
           delegate_to: localhost
           with_items:
               - host: "10.10.10.10"
                 name: "node-1"
               - host: "10.10.10.20"
                 name: "node-2"

         - name: Create a virtual server
           bigip_virtual_server:
               server: "{{ ansible_host }}"
               user: "{{ bigip_username }}"
               password: "{{ bigip_password }}"
               validate_certs: "{{ validate_certs }}"
               description: "virtual server"
               destination: "10.10.20.20"
               name: "VS1"
               pool: "web_pool"
               port: "80"
               snat: "Automap"
               all_profiles:
                   - "http"
                   - "clientssl"
           delegate_to: localhost


Delete the virtual server
+++++++++++++++++++++++++

To delete an object, set the state to ``absent``.

.. code-block:: yaml

         - name: Delete virtual server
           bigip_virtual_server:
               server: "{{ ansible_host }}"
               user: "{{ bigip_username }}"
               password: "{{ bigip_password }}"
               validate_certs: "{{ validate_certs }}"
               name: "VS1"
               partition: "Common"
               state: "absent"
           delegate_to: localhost

`Details about this module <http://docs.ansible.com/ansible/latest/bigip_virtual_server_module.html>`_.

Modify the virtual server's port
++++++++++++++++++++++++++++++++

You can use Ansible to update existing objects.

.. code-block:: yaml

         - name: Modify virtual server port
           bigip_virtual_server:
               server: "{{ ansible_host }}"
               user: "{{ bigip_username }}"
               password: "{{ bigip_password }}"
               validate_certs: "{{ validate_certs }}"
               name: "VS1"
               partition: "Common"
               port: "8080"
               state: "present"
           delegate_to: localhost

`Details about this module <http://docs.ansible.com/ansible/latest/bigip_virtual_server_module.html>`_.


Import SSL certificates
+++++++++++++++++++++++

You can use Ansible to import SSL certificates to BIG-IP.

.. code-block:: yaml

         - name: Import PEM Certificate from local disk
           bigip_ssl_certificate:
               server: "{{ ansible_host }}"
               user: "{{ bigip_username }}"
               password: "{{ bigip_password }}"
               validate_certs: "{{ validate_certs }}"
               name: "certificate-name"
               cert_src: "/path/to/cert.crt"
               key_src: "/path/to/key.key"
               state: "present"
           delegate_to: localhost


`Details about this module <http://docs.ansible.com/ansible/latest/bigip_ssl_certificate_module.html>`_.


Wait for BIG-IP to be ready
+++++++++++++++++++++++++++

Between tasks, you may want to wait for BIG-IP to be ready to accept the next changes.

`Here <https://github.com/F5Networks/f5-ansible/tree/devel/examples/0003-wait-for-bigip>`_ is an example of how to do this.


Run tmsh commands
+++++++++++++++++

TMSH is the command-line language you can use to administer BIG-IP. In cases where a module is not available, you might want to run specific TMSH commands.

.. code-block:: yaml

         - name: run multiple commands on remote nodes
           bigip_command:
               server: "{{ ansible_host }}"
               user: "{{ bigip_username }}"
               password: "{{ bigip_password }}"
               validate_certs: "{{ validate_certs }}"
               commands:
               - show sys version
               - list ltm virtual
           delegate_to: localhost

`Details about this module <http://docs.ansible.com/ansible/latest/bigip_command_module.html>`_.


Deploy iRules
+++++++++++++

iRules are a BIG-IP-specific scripting syntax that you can use to intercept, inspect, transform, and direct inbound or outbound application traffic.

F5 `provides a module <http://docs.ansible.com/ansible/latest/bigip_irule_module.html>`_ you can use to deploy iRules.


More Information
````````````````

F5 provides informal and community-based support for the F5 Modules for Ansible.

For help using the modules, `see this doc <http://clouddocs.f5.com/products/orchestration/ansible/devel/usage/support.html>`_.


.. seealso::

   `F5 Modules for Ansible documentation <http://clouddocs.f5.com/products/orchestration/ansible/devel/>`_
       Overview documentation to help you get started, as well as content for developers who want to contribute to the project.
   `F5 module-specific reference documentation <http://docs.ansible.com/ansible/latest/list_of_network_modules.html#f5>`_
       Details on all the F5 modules.
   `F5 modules in development <https://github.com/F5Networks/f5-ansible/issues>`_
       Modules actively being worked on by F5.
   `Automate F5 BIG-IP by using Ansible webinar <https://www.ansible.com/blog/automating-f5-big-ip-using-ansible-webinar>`_
       A more detailed Q&A about the F5 modules.
   `Dig deeper into Ansible and F5 integration <https://devcentral.f5.com/articles/dig-deeper-into-ansible-and-f5-integration-25984>`_
       More examples of using Ansible to configure BIG-IP.
   `Use Ansible to automate F5 VMware deployments <https://devcentral.f5.com/articles/ve-on-vmware-part-2-ansible-deployment-29790>`_
       Deploy BIG-IP VE in VMware by using the F5 modules for Ansible.
