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
	python scripts/module_formatter.py --module-dir library/ --template-dir scripts/ --output-dir docs/modules/ -v

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

bigip-device-dns:
	ansible-playbook -i inventory/hosts tests/bigip_device_dns.yaml -vvvv
	flake8 library/bigip_device_dns.py

bigip-device-ntp:
	ansible-playbook -i inventory/hosts tests/bigip_device_ntp.yaml -vvvv
	flake8 library/bigip_device_ntp.py

bigip-device-sshd:
	ansible-playbook -i inventory/hosts tests/bigip_device_sshd.yaml -vvvv
	flake8 library/bigip_device_sshd.py

bigip-facts:
	ansible-playbook -i inventory/hosts tests/bigip_facts.yaml -vvvv
	flake8 library/bigip_facts.py

bigip-gtm-datacenter:
	ansible-playbook -i inventory/hosts tests/bigip_gtm_datacenter.yaml -vvvv
	flake8 library/bigip_gtm_datacenter.py

bigip-gtm-facts:
	ansible-playbook -i inventory/hosts tests/bigip_gtm_facts.yaml -vvvv
	flake8 library/bigip_gtm_facts.py

bigip-gtm-virtual-server:
	ansible-playbook -i inventory/hosts tests/bigip_gtm_virtual_server.yaml -vvvv
	flake8 library/bigip_gtm_virtual_server.py

bigip-gtm-wide-ip:
	ansible-playbook -i inventory/hosts tests/bigip_gtm_wide_ip.yaml -vvvv
	flake8 library/bigip_gtm_wide_ip.py

bigip-hostname:
	ansible-playbook -i inventory/hosts tests/bigip_hostname.yaml -vvvv
	flake8 library/bigip_hostname.py

bigip-irule:
	ansible-playbook -i inventory/hosts tests/bigip_irule.yaml -vvvv
	flake8 library/bigip_irule.py

bigip-monitor-http:
	ansible-playbook -i inventory/hosts tests/bigip_monitor_http.yaml -vvvv
	flake8 library/bigip_monitor_http.py

bigip-monitor-tcp:
	ansible-playbook -i inventory/hosts tests/bigip_monitor_tcp.yaml -vvvv
	flake8 library/bigip_monitor_tcp.py

bigip-node:
	ansible-playbook -i inventory/hosts tests/bigip_node.yaml -vvvv
	flake8 library/bigip_node.py

bigip-pool:
	ansible-playbook -i inventory/hosts tests/bigip_pool.yaml -vvvv
	flake8 library/bigip_pool.py

bigip-pool-member:
	ansible-playbook -i inventory/hosts tests/bigip_pool_member.yaml -vvvv
	flake8 library/bigip_pool_member.py

bigip-routedomain:
	ansible-playbook -i inventory/hosts tests/bigip_routedomain.yaml -vvvv
	flake8 library/bigip_routedomain.py

bigip-selfip:
	ansible-playbook -i inventory/hosts tests/bigip_selfip.yaml -vvvv
	flake8 library/bigip_selfip.py

bigip-ssl-certificate:
	ansible-playbook -i inventory/hosts tests/bigip_ssl_certificate.yaml -vvvv
	flake8 library/bigip_ssl_certificate.py

bigip-sys-db:
	ansible-playbook -i inventory/hosts tests/bigip_sys_db.yaml -vvvv
	flake8 library/bigip_sys_db.py

bigip-sys-global:
	ansible-playbook -i inventory/hosts tests/bigip_sys_global.yaml -vvvv
	flake8 library/bigip_sys_global.py

bigip-user-facts:
	ansible-playbook -i inventory/hosts tests/bigip_user_facts.yaml -vvvv
	flake8 library/bigip_user_facts.py

bigip-virtual-server:
	ansible-playbook -i inventory/hosts tests/bigip_virtual_server.yaml -vvvv
	flake8 library/bigip_virtual_server.py

bigip-vlan:
	ansible-playbook -i inventory/hosts tests/bigip_vlan.yaml -vvvv
	flake8 library/bigip_vlan.py

fetch-upstream:
	curl -o library/bigip_device_dns.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_device_dns.py
	curl -o library/bigip_device_ntp.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_device_ntp.py
	curl -o library/bigip_device_sshd.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_device_sshd.py
	curl -o library/bigip_facts.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_facts.py
	curl -o library/bigip_gtm_datacenter.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_gtm_datacenter.py
	curl -o library/bigip_gtm_virtual_server.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_gtm_virtual_server.py
	curl -o library/bigip_gtm_wide_ip.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_gtm_wide_ip.py
	curl -o library/bigip_irule.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_irule.py
	curl -o library/bigip_monitor_http.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_monitor_http.py
	curl -o library/bigip_monitor_tcp.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_monitor_tcp.py
	curl -o library/bigip_node.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_node.py
	curl -o library/bigip_pool.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_pool.py
	curl -o library/bigip_pool_member.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_pool_member.py
	curl -o library/bigip_routedomain.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_routedomain.py
	curl -o library/bigip_selfip.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_selfip.py
	curl -o library/bigip_ssl_certificate.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_ssl_certificate.py
	curl -o library/bigip_sys_db.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_sys_db.py
	curl -o library/bigip_virtual_server.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_virtual_server.py
	curl -o library/bigip_vlan.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_vlan.py
