### How to Use F5 Ansible with `ansible-core` ≥ 2.20 and Python 3.8 on BIG-IP / BIG-IQ

#### Overview

If you have upgraded your Ansible Control Node to **`ansible-core` ≥ 2.20**, you may encounter the following error when running playbooks against F5 BIG-IP or BIG-IQ devices:

```text
[ERROR]: Task failed: Module failed: Ansible requires Python 3.9 or newer on the target. Current version: 3.8.12
```

**You do NOT need to downgrade Ansible or modify the Python runtime on your BIG-IP.** 

F5 BIG-IP (TMOS 17.5.x through 21.1.x) ships with an internal, vendor-supported Python 3.8.12 runtime. This error only occurs if a playbook attempts to treat the BIG-IP as a generic Linux host and push Python code directly to the appliance over SSH. 

When playbooks follow F5 network automation standards, **Ansible never runs Python code on the BIG-IP appliance itself**. All F5 collection modules execute on your **Ansible Control Node** and interact with the device remotely over HTTPS (iControl REST / AS3).

---

### 3 Steps to Avoid Target Python Issues

#### Step 1: Always Set `gather_facts: false`

Ansible defaults to `gather_facts: true`. When targeting a BIG-IP over SSH or a generic connection, Ansible automatically attempts to push and execute its Linux fact-gathering module (`ansible.builtin.setup`) on TMOS, triggering the target Python version check.

**Add `gather_facts: false` at the top of your play:**

```yaml
---
- name: Configure BIG-IP
  hosts: bigip
  gather_facts: false    # <-- REQUIRED: Prevents Ansible from running Linux setup on TMOS
  connection: local      # <-- Ensures modules run locally on your control node

  tasks:
    - name: Create a VLAN
      f5networks.f5_modules.bigip_vlan:
        name: internal
        tag: 10
        provider: "{{ bigip_provider }}"
```

> **Tip (Global Setting):** If you manage many playbooks, you can disable implicit fact gathering globally by adding this to your `ansible.cfg`:
> ```ini
> [defaults]
> gathering = explicit
> ```

---

#### Step 2: Use F5 Fact Modules Instead of Standard Linux Facts

If your playbooks rely on facts (such as hostname, version, or interfaces), do not use Ansible's default fact gathering. Instead, use F5's dedicated API fact module, which collects appliance data over HTTPS:

```yaml
  tasks:
    - name: Collect BIG-IP system information via API
      f5networks.f5_modules.bigip_device_info:
        gather_subset:
          - system-info
        provider: "{{ bigip_provider }}"
      register: device_info

    - name: Display TMOS version
      ansible.builtin.debug:
        msg: "BIG-IP version is {{ device_info.system_info.base_mac }}"
```

---

#### Step 3: Avoid `ansible.builtin.command` and `shell` over SSH

Generic Linux modules (`command`, `shell`, `copy`, `template`, `lineinfile`) require remote Python on the target host to run their wrappers. On BIG-IP, these will fail under Ansible 2.20+.

* **To run TMSH commands via REST (Recommended):**
  Use `f5networks.f5_modules.bigip_command` (runs on the control node, sends commands over iControl REST):
  ```yaml
    - name: Run TMSH command via iControl REST
      f5networks.f5_modules.bigip_command:
        commands:
          - show sys version
        provider: "{{ bigip_provider }}"
  ```

* **To run raw CLI commands over SSH (Zero target-Python requirement):**
  If your environment requires SSH CLI access, use `ansible.builtin.raw` instead of `command` or `shell`. `raw` executes directly through the SSH subsystem without shipping module payloads or invoking Python on TMOS:
  ```yaml
    - name: Run TMSH command via raw SSH
      ansible.builtin.raw: tmsh show sys version
      register: result
  ```

---

### Summary Checklist

| Setting / Practice | Recommended Value | Reason |
| :--- | :--- | :--- |
| **Control Node Python** | Python ≥ 3.10 | Required by `ansible-core` ≥ 2.16 |
| **Playbook Fact Gathering** | `gather_facts: false` | Prevents remote execution of `setup` on TMOS |
| **Connection Method** | `connection: local` or `httpapi` | Keeps module execution on the control node |
| **Fact Gathering Module** | `bigip_device_info` | Retrieves facts via HTTPS REST API |
| **Command Execution** | `bigip_command` or `raw` | Avoids target Python dependencies |
| **Appliance Python Upgrade** | **Do NOT attempt** | Modifying TMOS system packages voids F5 appliance support |
