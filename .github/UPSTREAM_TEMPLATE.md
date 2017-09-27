<!--- Verify first that your issue/request is not already reported in GitHub -->

##### ISSUE TYPE
<!--- Pick one below and delete the rest: -->
 - Upstream request

##### COMPONENT NAME
<!--- Name of the module/role/task -->

##### ANSIBLE VERSION
<!--- Paste verbatim output from “ansible --version” between quotes below -->
```

```

##### PYTHON VERSION
<!--- Paste verbatim output from “python -V” between quotes below -->
```

```

##### BIGIP VERSION
<!---
Paste a list of BIG-IP versions this was tested on.
This is usually reflected in the playbook that runs the functional test.

Check the tested versions
-->
- [ ] 12.0.0 (BIGIP-12.0.0.0.0.606)
- [ ] 12.1.0 (BIGIP-12.1.0.0.0.1434)
- [ ] 12.1.0-hf1 (BIGIP-12.1.0.1.0.1447-HF1)
- [ ] 12.1.0-hf2 (BIGIP-12.1.0.2.0.1468-HF2)
- [ ] 12.1.1 (BIGIP-12.1.1.0.0.184)
- [ ] 12.1.1-hf1 (BIGIP-12.1.1.1.0.196-HF1)
- [ ] 12.1.1-hf2 (BIGIP-12.1.1.2.0.204-HF2)
- [ ] 12.1.2 (BIGIP-12.1.2.0.0.249)
- [ ] 12.1.2-hf1 (BIGIP-12.1.2.1.0.264-HF1)
- [ ] 13.0.0 (BIGIP-13.0.0.0.0.1645)
- [ ] 13.0.0-hf1 (BIGIP-13.0.0.1.0.1668-HF1)

##### CHECKLIST
<!---
Ensure all the following are complete
-->
#### Module code related
- [ ] Module code has `EXAMPLES`
- [ ] Module code has `DOCUMENTATION`
- [ ] Module code has `RETURN`
- [ ] Module code has `ANSIBLE_METADATA`
- [ ] Module code conforms to coding standards (v3). This includes a `Parameters` class, `ModuleManager` class, and `ArgumentSpec` class.
- [ ] Module includes GPL3 license at top of the file and F5 Networks copyright.
- [ ] Module imports are not `from *`
- [ ] If this module is new to Ansible, the `version_added` key of the `DOCUMENTATION` variable is set to `2.5`.
- [ ] If this module is not new to Ansible, but you have added accepted parameters to it, the `version_added` key for each of those new parameters is `2.5`.

#### Integration test related
- [ ] Playbook exists to do functional tests
- [ ] Role directory with functional tests exists
- [ ] Module code has been tested on major releases post 12.x. If a major release cannot be supported, document "why" in the `notes` section of the module 
`DOCUMENTATION`

#### Unit test related
- [ ] Unit tests in `tests/unit` for the product exist
- [ ] `TestParameters` unit test class exists and has content
- [ ] `TestManager` unit test class (or `*Managers` if required) exists and has content

#### QC related
- [ ] Module code passes `pycodestyle library/MODULE_NAME.py`
- [ ] Unit test code passes `pycodestyle test/unit/PRODUCT/test_MODULE_NAME.py`

#### Docs related
- [ ] Docs exist and build correctly (`make docs`)
- [ ] Docs have been merged to `f5-ansible` so they can be rebuilt by ReadTheDocs.

#### Upstream vendor related, with f5-sdk

This must be done inside of Ansible's source tree. (`cd local/ansible`)

- [ ] Module code in Ansible repo passes `ansible-test units --python 2.7 MODULE_NAME`
- [ ] Module code in Ansible repo passes `ansible-test units --python 3.5 MODULE_NAME`
- [ ] Module code in Ansible repo passes `ansible-test units --python 3.6 MODULE_NAME`
- [ ] Module code in Ansible repo passes `ansible-test sanity --test validate-modules`
- [ ] Module code in Ansible repo passes `ansible-test sanity --test pep8`

#### Upstream vendor related, without f5-sdk

This must be done inside of Ansible's source tree. (`cd local/ansible`) 

- [ ] Module code in Ansible repo passes `ansible-test sanity --test import --python 2.7`
- [ ] Module code in Ansible repo passes `ansible-test sanity --test import --python 3.5`
- [ ] Module code in Ansible repo passes `ansible-test sanity --test import --python 3.6`
- [ ] Module code in Ansible repo passes `nosetests test/units/modules/network/f5/test_MODULE_NAME.py` using venv made with requirements.bare.txt

#### Upstream vendor related, misc
- [ ] Module PR has been mentioned as a comment for the next Networking Team meeting here https://github.com/ansible/community/issues/248

#### Upstream vendor, sanity related
- [ ] Command `bash test/ansible/sanity/integration-test-idempotent-names.sh` passes

##### SUMMARY
<!--- Explain the problem briefly -->
