#vim: set tabstop=8:softtabstop=8:shiftwidth=8:noexpandtab

DOCTEST := python ../scripts/ansible-doc-test.py
PYHOOK := 'import sys;sys.path.insert(1,".")'
PYLINT := pylint --additional-builtins=_ --init-hook=$(PYHOOK)

MODULE_TARGET = $(shell echo $@ | sed s/cov-// | tr '-' '_')

.PHONY: docs flake8

all: clean-coverage
	ansible-playbook -i inventory/hosts playbooks/toggle-coverage.yaml -e "f5_module=all toggle=on" --vault-password-file ./vault.txt
	COVERAGE_PROCESS_START=${CURDIR}/.coveragerc ANSIBLE_KEEP_REMOTE_FILES=1 ansible-playbook -i inventory/hosts playbooks/bigip.yaml --vault-password-file ./vault.txt
	ansible-playbook -i inventory/hosts playbooks/toggle-coverage.yaml -e "f5_module=all toggle=off" --vault-password-file ./vault.txt
	flake8 library/*.py

all-tests: flake8 ansible-doc

all-tests-dev: flake8 ansible-doc ansible-doc-dev

pylint: pylint-modules

docs:
	rm docs/modules/* || true
	python scripts/module_formatter.py --module-dir library/ --template-dir scripts/ --output-dir docs/modules/ -v
	cd docs && make html

flake8:
	flake8 library

ansible-doc:
	(cd library; \
		$(DOCTEST) -M . bigip_command.py; \
		$(DOCTEST) -M . bigip_device_dns.py; \
		$(DOCTEST) -M . bigip_device_ntp.py; \
		$(DOCTEST) -M . bigip_device_sshd.py; \
		$(DOCTEST) -M . bigip_dns_facts.py; \
		$(DOCTEST) -M . bigip_dns.py; \
		$(DOCTEST) -M . bigip_dns_zone.py; \
		$(DOCTEST) -M . bigip_gtm_datacenter.py; \
		$(DOCTEST) -M . bigip_hostname.py; \
		$(DOCTEST) -M . bigip_iapp_service.py; \
		$(DOCTEST) -M . bigip_iapp_template.py; \
		$(DOCTEST) -M . bigip_irule.py; \
		$(DOCTEST) -M . bigip_license.py; \
		$(DOCTEST) -M . bigip_partition.py; \
		$(DOCTEST) -M . bigip_provision.py; \
		$(DOCTEST) -M . bigip_selfip.py; \
		$(DOCTEST) -M . bigip_service.py; \
		$(DOCTEST) -M . bigip_software.py; \
		$(DOCTEST) -M . bigip_sysdb.py; \
		$(DOCTEST) -M . bigip_ucs_fetch.py; \
		$(DOCTEST) -M . bigip_ucs.py; \
		$(DOCTEST) -M . bigip_user_facts.py; \
		$(DOCTEST) -M . bigip_user.py; \
		$(DOCTEST) -M . bigip_vlan.py; \
	)

ansible-doc-dev:
	(cd library; \
		$(DOCTEST) -M . bigip_qkview_facts.py; \
	)

clean-coverage:
	$(shell rm cache/coverage/.coverage*)
	$(shell rm .coverage)

bigip-%:
	ANSIBLE_KEEP_REMOTE_FILES=1 ansible-playbook -i inventory/hosts playbooks/${MODULE_TARGET}.yaml --vault-password-file ./vault.txt
	flake8 library/${MODULE_TARGET}.py

cov-bigip-%: clean-coverage
	ansible-playbook -i inventory/hosts playbooks/toggle-coverage.yaml -e "f5_module=${MODULE_TARGET} toggle=on" --vault-password-file ./vault.txt
	COVERAGE_PROCESS_START=${CURDIR}/.coveragerc ANSIBLE_KEEP_REMOTE_FILES=1 ansible-playbook -i inventory/hosts playbooks/${MODULE_TARGET}.yaml --vault-password-file ./vault.txt
	ansible-playbook -i inventory/hosts playbooks/toggle-coverage.yaml -e "f5_module=${MODULE_TARGET} toggle=off" --vault-password-file ./vault.txt
	flake8 library/${MODULE_TARGET}.py

fetch-upstream:
	curl -o library/bigip_device_dns.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_device_dns.py
	curl -o library/bigip_device_ntp.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_device_ntp.py
	curl -o library/bigip_device_sshd.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_device_sshd.py
	curl -o library/bigip_facts.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_facts.py
	curl -o library/bigip_gtm_datacenter.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_gtm_datacenter.py
	curl -o library/bigip_gtm_facts.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_gtm_facts.py
	curl -o library/bigip_gtm_virtual_server.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_gtm_virtual_server.py
	curl -o library/bigip_gtm_wide_ip.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_gtm_wide_ip.py
	curl -o library/bigip_hostname.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_hostname.py
	curl -o library/bigip_irule.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_irule.py
	curl -o library/bigip_monitor_http.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_monitor_http.py
	curl -o library/bigip_monitor_tcp.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_monitor_tcp.py
	curl -o library/bigip_node.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_node.py
	curl -o library/bigip_pool.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_pool.py
	curl -o library/bigip_pool_member.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_pool_member.py
	curl -o library/bigip_routedomain.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_routedomain.py
	curl -o library/bigip_selfip.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_selfip.py
	curl -o library/bigip_snat_pool.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_snat_pool.py
	curl -o library/bigip_ssl_certificate.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_ssl_certificate.py
	curl -o library/bigip_sys_db.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_sys_db.py
	curl -o library/bigip_virtual_server.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_virtual_server.py
	curl -o library/bigip_vlan.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_vlan.py
