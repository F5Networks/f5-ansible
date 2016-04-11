# Test the bigip_irule module
#
# Running this playbook assumes that you have a BIG-IP installation at the
# ready to receive the commands issued in this Playbook.
#
# This playbook additionally defines a number of variables in its vars:
# section that may need to be changed to be relevant to your environment.
# These changes can be made either at runtime with the -e argument, or
# statically specified in the playbook itself.
#
# Usage:
#
#    ansible-playbook -i notahost, tests/bigip_irule.yaml
#
# Examples:
#
#    Run all tests on the bigip_irule module
#
#    ansible-playbook -i notahost, tests/bigip_irule.yaml
#

- name: Test the bigip_irule module
  hosts: f5-test
  gather_facts: false
  connection: local

  vars:
      bigip_username: "admin"
      bigip_password: "admin"
      validate_certs: "no"
      partition: "foo"
      irules:
          - name: "irule-01.tcl"
            src: fixtures/irule-01.tcl
          - name: "irule-02.tcl"
            src: fixtures/irule-02.tcl

  tasks:
      - name: Create iRule in LTM
        bigip_irule:
            name: "{{ irules[0].name }}"
            server: "{{ inventory_hostname }}"
            user: "{{ bigip_username }}"
            password: "{{ bigip_password }}"
            validate_certs: "{{ validate_certs }}"
            module: "ltm"
            content: "{{ lookup('template', 'irules[0].src') }}"
        register: result

      - name: Assert Create iRule in LTM
        assert:
            that:
                - result|changed

      - name: Create iRule in LTM - Idempotent check
        bigip_irule:
            name: "{{ irules[0].name }}"
            server: "{{ inventory_hostname }}"
            user: "{{ bigip_username }}"
            password: "{{ bigip_password }}"
            validate_certs: "{{ validate_certs }}"
            module: "ltm"
            content: "{{ lookup('template', 'irules[0].src') }}"
        register: result

      - name: Assert Create iRule in LTM - Idempotent check
        assert:
            that:
                - not result|changed

      - name: Modify iRule in LTM
        bigip_irule:
            name: "{{ irules[0].name }}"
            server: "{{ inventory_hostname }}"
            user: "{{ bigip_username }}"
            password: "{{ bigip_password }}"
            validate_certs: "{{ validate_certs }}"
            module: "ltm"
            content: "{{ lookup('template', 'irules[1].src') }}"
        register: result

      - name: Assert Modify iRule in LTM
        assert:
            that:
                - result|changed

      - name: Modify iRule in LTM - Idempotent check
        bigip_irule:
            name: "{{ irules[0].name }}"
            server: "{{ inventory_hostname }}"
            user: "{{ bigip_username }}"
            password: "{{ bigip_password }}"
            validate_certs: "{{ validate_certs }}"
            module: "ltm"
            content: "{{ lookup('template', 'irules[1].src') }}"
        register: result

      - name: Assert Modify iRule in LTM - Idempotent check
        assert:
            that:
                - not result|changed

      - name: Delete iRule in LTM
        bigip_irule:
            name: "{{ irules[0].name }}"
            server: "{{ inventory_hostname }}"
            user: "{{ bigip_username }}"
            password: "{{ bigip_password }}"
            validate_certs: "{{ validate_certs }}"
            module: "ltm"
            state: "absent"
        register: result

      - name: Assert Delete iRule in LTM
        assert:
            that:
                - result|changed

      - name: Delete iRule in LTM - Idempotent check
        bigip_irule:
            name: "{{ irules[0].name }}"
            server: "{{ inventory_hostname }}"
            user: "{{ bigip_username }}"
            password: "{{ bigip_password }}"
            validate_certs: "{{ validate_certs }}"
            module: "ltm"
            state: "absent"
        register: result

      - name: Assert Delete iRule in LTM - Idempotent check
        assert:
            that:
                - not result|changed

      - name: Create iRule in missing GTM
        bigip_irule:
            name: "{{ irules[0].name }}"
            server: "{{ inventory_hostname }}"
            user: "{{ bigip_username }}"
            password: "{{ bigip_password }}"
            validate_certs: "{{ validate_certs }}"
            module: "gtm"
            content: "{{ lookup('template', 'irules[0].src') }}"
        register: result

      - name: Assert Create iRule in missing GTM
        assert:
            that:
                - not result|changed
