# F5 BIG-IP Imperative Collection for Ansible

## Description

This collection provides imperative Ansible modules and plugins for managing F5 BIG-IP and BIG-IQ devices. It enables automation of configuration, deployment, and management tasks for F5 devices, making it easier for network and automation engineers to integrate F5 solutions into their infrastructure-as-code workflows. The collection is designed for users who need to automate F5 device management, streamline operations, and ensure consistency across environments.

## Requirements

- Ansible >= 2.16
- Python >= 3.10 on the Control Node
- Python libraries (also listed in `requirements.txt`):
  - `cryptography`
  - `objectpath`
  - `packaging`

## Installation

This collection is distributed as Red Hat Ansible Certified Content through [Red Hat Ansible Automation Hub](https://console.redhat.com/ansible/automation-hub).

Configure `ansible.cfg` with your Automation Hub server and API token. Retrieve the token from the [Automation Hub token page](https://console.redhat.com/ansible/automation-hub/token):

```ini
[galaxy]
server_list = automation_hub

[galaxy_server.automation_hub]
url=https://console.redhat.com/api/automation-hub/content/published/
auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
token=<your_api_token>
```

Install the collection with the Ansible Galaxy command-line tool:

```
ansible-galaxy collection install f5networks.f5_modules
```

You can also include it in a `requirements.yml` file and install with `ansible-galaxy collection install -r requirements.yml`:

```yaml
collections:
  - name: f5networks.f5_modules
```

To upgrade to the latest version:

```
ansible-galaxy collection install f5networks.f5_modules --upgrade
```

To install a specific version (e.g., 1.0.0):

```
ansible-galaxy collection install f5networks.f5_modules:==1.0.0
```

Install the Python library dependencies on the control node:

```
pip install -r ~/.ansible/collections/ansible_collections/f5networks/f5_modules/requirements.txt
```

> **Note:** Adjust the path if the collection was installed to a custom collections path or via Ansible Galaxy to a user or system directory.

See [using Ansible collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

## Example Usage

To use a module from this collection, reference the full namespace, collection, and module name:

```yaml
---
- name: Using F5 BIG-IP Collection
  hosts: f5
  connection: local
  tasks:
    - f5networks.f5_modules.bigip_pool:
        name: my-pool
        ...
```

## Running the Collection in an Execution Environment (EE)

You can run this collection inside an Ansible Execution Environment (EE) container. This approach ensures all required package dependencies and minimum supported Python versions are installed in an isolated container, minimizing environment-related issues during runtime.

To use the collection in an EE, add it to your `requirements.yml` file. For example:

```yaml
---
collections:
  - name: ansible.netcommon
    version: ">=2.0.0"
  - name: f5networks.f5_modules
```

When building your EE container, include this requirements file. For more information on building and using EEs, see the [Red Hat documentation on creating and using execution environments][execenv].

The collection's Python dependencies (`cryptography`, `objectpath`, and `packaging`) are installed automatically when the EE is built with `ansible-builder`.

For F5-specific EE usage and advanced scenarios, refer to the [F5 execenv documentation][f5execenv].

## Testing

This collection has been tested on:
- F5 BIG-IP and BIG-IQ virtual editions
- Supported Ansible versions (>=2.16)
- Python 3.10+

Testing includes unit, integration, and system tests. Some modules may require access to a live F5 device or a suitable test environment. Known exceptions and workarounds are documented in the module documentation.

## Support

As Red Hat Ansible Certified Content, this collection is entitled to support through the Ansible Automation Platform (AAP) using the **Create issue** button on the top right corner.

If a support case cannot be opened with Red Hat and the collection has been obtained either from Galaxy or GitHub, you can report issues on the [GitHub issue tracker](https://github.com/F5Networks/f5-ansible/issues).

Please refer to the [F5 support policy][support_policy] for details.

## Release Notes

See the [Changelog](https://clouddocs.f5.com/products/orchestration/ansible/devel/f5_modules/CHANGELOG.html) for release notes.

## License Information

Published under [GPL V3](https://www.gnu.org/licenses/gpl-3.0.txt). See the [LICENSE](LICENSE) file included in the collection for details.

## Contributor License Agreement
Individuals or business entities who contribute to this project must complete and submit the [F5 Contributor License Agreement](https://clouddocs.f5.com/products/orchestration/ansible/devel/usage/contributor.html) to Ansible_CLA@f5.com prior to their code submission being included in this project.


## Copyright

Copyright 2025 F5 Networks Inc.

[execenv]: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/creating_and_using_execution_environments/index
[f5execenv]: https://clouddocs.f5.com/products/orchestration/ansible/devel/usage/exec-env.html
[support_policy]: https://f5.com/support/support-policies
