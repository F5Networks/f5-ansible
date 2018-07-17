version 1.0
SOAP based apis
function based modules
no unit tests
https://github.com/F5Networks/f5-ansible/blob/a4c40b31acb4df942d6f2d1c37be5d72c99702ef/library/_bigip_node.py


version 2.0
REST based apis
introduction of classes, removal of functions
classes named after the module
```
class BigIpRouteDomain(object):
    def __init__(self, *args, **kwargs):
        if not HAS_F5SDK:
            raise F5ModuleError("The python f5-sdk module is required")

        # The params that change in the module
        self.cparams = dict()

        # Stores the params that are sent to the module
        self.params = kwargs
        self.api = ManagementRoot(kwargs['server'],
                                  kwargs['user'],
                                  kwargs['password'],
                                  port=kwargs['server_port'],
                                  token=True)
```
monolithic main() function
use of apply_changes()
common methods were uncommon (ie; update_on_device was called update_pools_on_device)
no unit tests
monolithic update methods
```
        if description is not None:
            if 'description' in current:
                if description != current['description']:
                    params['description'] = description
            else:
                params['description'] = description
```
attempts to support both icontrol and soap (https://github.com/F5Networks/f5-ansible/commit/d28922ba86445451056ca5566bfd9a9767fc47ed#diff-0f404d93f4f332d241c6d77b5ba4da5cR662)
no usage of an F5AnsibleClient
no ArgumentSpec class (https://github.com/F5Networks/f5-ansible/commit/d28922ba86445451056ca5566bfd9a9767fc47ed#diff-0f404d93f4f332d241c6d77b5ba4da5cR626)
full example (https://github.com/F5Networks/f5-ansible/blob/8036f539d0a88da42b6d4133f47a43b3891a4432/library/bigip_routedomain.py)

version 2.1
introduction of ArgumentSpec
usage of flush() as ingress point of module (https://github.com/F5Networks/f5-ansible/blob/3dba6410453a9e26c52e108190a155d3d146dbc6/library/bigip_selfip.py#L157_

version 3
changed to exec_module for ingress point
usage of @property begins
usage of standardized classes; ModuleManager, ArgumentSpec, Parameters, Changes
full unit tests
standardized on method names; create, create_on_device, update, update_on_device, remove, remove_from_device, read_current_from_device, absent, present, exec_module,
    remove, exists, _announce_deprecations, should_update, _update_changed_options
A ModuleManager instantiation that only had this
```
        self.have = None
        self.want = Parameters(self.client.module.params)
        self.changes = Changes()
```

version 3.1
introduction of UsableChanges, ReportableChanges
introduction of Difference class
introduction of ApiParameters, ModuleParameters
introduction of stubber to stub out common parts of modules
cleanup_tokens added
ModuleManager changed to this
```
        self.want = ModuleParameters(params=self.client.module.params)
        self.have = ApiParameters()
        self.changes = UsableChanges()
```
Beginning of removal of set_changed_options in favor of a blank self.have (`self.have = ApiParameters()`) and update_changed_options usage



version 3.1.1
Removal of set_changed_options and moving to update_changed_options with an empty self.have. this is an optimization to remove special code handling in the create() method of many modules
refactoring of the AnsibleF5Client class into a plain AnsibleModule class and an F5Client class. Also, a fix for the module tracebacks that are done in the main() method
removal of the following from the DOCUMENTATION var
  requirements:
    - f5-sdk >= 3.0.6
  notes:
    - Requires the f5-sdk Python package on the host This is as easy as
      C(pip install f5-sdk)
removal of common Parameters __init__ and update() methods (an optimization)
Introduction of development module_utils in f5-ansible repo. Requires the following code changes

.. code:: python

   import os
   import sys
   import time

   from distutils.version import LooseVersion

   try:
       # Sideband repository used for dev
       sys.path.insert(0, os.path.abspath('/here/'))

       from ansible.module_utils.basic import AnsibleModule
       from ansible.module_utils.basic import env_fallback
       from library.module_utils.network.f5.bigip import HAS_F5SDK
       from library.module_utils.network.f5.bigip import F5Client
       from library.module_utils.network.f5.common import F5ModuleError
       from library.module_utils.network.f5.common import AnsibleF5Parameters
       from library.module_utils.network.f5.common import cleanup_tokens
       from library.module_utils.network.f5.common import fqdn_name
       from library.module_utils.network.f5.common import f5_argument_spec
   except ImportError:
       # Remove path which was inserted by dev
       sys.path.pop(0)

       try:
           # Upstream Ansible
           from ansible.module_utils.network.f5.bigip import F5Client
           from ansible.module_utils.network.f5.common import AnsibleF5Parameters
           from ansible.module_utils.network.f5.common import cleanup_tokens
           from ansible.module_utils.network.f5.common import fqdn_name
       except ImportError:
           # Upstream Ansible legacy
           from ansible.module_utils.f5_utils import AnsibleF5Client
           from ansible.module_utils.f5_utils import AnsibleF5Parameters
           from ansible.module_utils.f5_utils import fq_name as fqdn_name
           from ansible.module_utils.f5_utils import HAS_F5SDK
           from ansible.module_utils.f5_utils import F5ModuleError

cleanup_tokens moved into module_utils and imported into module. Needs this code in the
last import above.

  .. code:: python

           def cleanup_tokens(client):
               try:
                   resource = client.api.shared.authz.tokens_s.token.load(
                       name=client.api.icrs.token
                   )
                   resource.delete()
               except Exception:
                   pass

support for new and legacy AnsibleF5Client. Requires several changes (noted with *)
1. Change main()
    def main():
        spec = ArgumentSpec()

*        try:
*            # Current bootstrapping method
*
*            # TODO: The argument spec code should be moved into ArgumentSpec class in 2.6
*            argument_spec = f5_argument_spec
*            argument_spec.update(spec.argument_spec)
*            module = AnsibleModule(
*                argument_spec=argument_spec,
*                supports_check_mode=spec.supports_check_mode,
*                mutually_exclusive=[
*                    ['file', 'template']
*                ]
*            )
*            if not HAS_F5SDK:
*                module.fail_json(msg="The python f5-sdk module is required")
*
*            client = F5Client(**module.params)
*        except Exception:
*            # Legacy method of bootstrapping the module
*            # TODO: Remove in 2.6
*            if not HAS_F5SDK:
*                raise F5ModuleError("The python f5-sdk module is required")
*
*            client = AnsibleF5Client(
*                argument_spec=spec.argument_spec,
*                supports_check_mode=spec.supports_check_mode,
*                f5_product_name=spec.f5_product_name,
*                mutually_exclusive=[
*                    ['file', 'template']
*                ]
*            )
*            module = client.module
        try:
*            mm = ModuleManager(module=module, client=client)
            results = mm.exec_module()
            cleanup_tokens(client)
*            module.exit_json(**results)
        except F5ModuleError as e:
            cleanup_tokens(client)
*            module.fail_json(msg=str(e))

    if __name__ == '__main__':
        main()

2. Remove f5_product_name

        # TODO: Remove in 2.6. This is part of legacy bootstrapping
        self.f5_product_name = 'bigip'

3. If a BaseManager is used, its definition should reflect this
    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        module = kwargs.pop('module', None)
        super(V2Manager, self).__init__(client=client, module=module)
        self.want = V2Parameters()
        self.want.client = client
        self.want.update(module.params)

4. A normal ModuleManager's init should include this (and def be changed to include *args and **kwargs)
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        self.module = kwargs.pop('module', None)

5. self.client.check_mode should be changed to
        if self.module.check_mode:

'partition' and 'state' are removed from comon argspec and must now be included
in the the ArgumentSpec in the module
            state=dict(
                default='present',
                choices=['present', 'absent']
            ),
            partition=dict(
                default='Common',
                fallback=(env_fallback, ['F5_PARTITION'])
            )
