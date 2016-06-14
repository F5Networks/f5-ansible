#vim: set tabstop=8:softtabstop=8:shiftwidth=8:noexpandtab

DOCTEST := python ../scripts/ansible-doc-test.py
PYHOOK := 'import sys;sys.path.insert(1,".")'
PYLINT := pylint --additional-builtins=_ --init-hook=$(PYHOOK)

.PHONY: docs flake8

all-tests: flake8 ansible-doc

all-tests-dev: flake8 ansible-doc ansible-doc-dev

pylint: pylint-modules

docs:
	rm docs/modules/*
	python scripts/module_formatter.py --module-dir library/ --template-dir scripts/ --output-dir docs/modules/

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

pylint-modules:
	(cd library; \
		$(PYLINT) f5/bigiq/bigiq.py; \
	)

bigip-sys-db:
	ansible-playbook -i inventory/hosts tests/bigip_sys_db.yaml -vvvv
	flake8 library/bigip_sys_db.py

bigip-device-sshd:
	ansible-playbook -i inventory/hosts tests/bigip_device_sshd.yaml -vvvv
	flake8 library/bigip_device_sshd.py

bigip-routedomain:
	ansible-playbook -i inventory/hosts tests/bigip_routedomain.yaml -vvvv
	flake8 library/bigip_routedomain.py

fetch-upstream:
	curl -o library/bigip_facts.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_facts.py
	curl -o library/bigip_gtm_wide_ip.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_gtm_wide_ip.py
	curl -o library/bigip_monitor_http.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_monitor_http.py
	curl -o library/bigip_monitor_tcp.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_monitor_tcp.py
	curl -o library/bigip_node.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_node.py
	curl -o library/bigip_pool.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_pool.py
	curl -o library/bigip_pool_member.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_pool_member.py
	curl -o library/bigip_virtual_server.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_virtual_server.py
