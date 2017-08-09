#vim: set tabstop=8:softtabstop=8:shiftwidth=8:noexpandtab

DOCTEST := python ../scripts/ansible-doc-test.py
PYHOOK := 'import sys;sys.path.insert(1,".")'
PYLINT := pylint --additional-builtins=_ --init-hook=$(PYHOOK)

MODULE_TARGET = $(shell echo $@ | sed s/cov-// | tr '-' '_')

.PHONY: docs style

all: clean-coverage
	ansible-playbook -i inventory/hosts playbooks/toggle-coverage.yaml -e "f5_module=all toggle=on" -vvvv
	COVERAGE_PROCESS_START=${CURDIR}/.coveragerc ANSIBLE_KEEP_REMOTE_FILES=1 ansible-playbook -i inventory/hosts playbooks/bigip.yaml -vvvv
	ansible-playbook -i inventory/hosts playbooks/toggle-coverage.yaml -e "f5_module=all toggle=off" -vvvv
	pycodestyle library/*.py

all-tests: pycodestyle

docs:
	rm docs/modules/* || true
	python scripts/plugin_formatter.py --module-dir library/ --template-dir scripts/ --output-dir docs/modules/ -v
	cd docs && make html

style:
	pycodestyle

export ANSIBLE_KEEP_REMOTE_FILES=1
export ANSIBLE_CONFIG=./test/integration/ansible.cfg

bigip_%:
	cd test/integration && ansible-playbook -i inventory/hosts ${MODULE_TARGET}.yaml -vvvv && cd -

iworkflow_%:
	cd test/integration && ansible-playbook -i inventory/hosts ${MODULE_TARGET}.yaml -vvvv && cd -

unit:
	pytest -s test/

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

upgrade-ansible:
	pip install --upgrade git+https://github.com/ansible/ansible.git
