# NOTE:
# 
# You need to install these packages on Ubunutu 12.04 to make this work:
# 
#     sudo apt-get install -y make python-stdeb fakeroot python-all rpm pep8 pylint
# 
#

DOCTEST := python ../scripts/ansible-doc-test.py
MODULE_DIR := .
PYHOOK := 'import sys;sys.path.insert(1,".")'
PYLINT := pylint --additional-builtins=_ --init-hook=$(PYHOOK)

all-tests: flake8 ansible-doc

all-tests-dev: flake8 ansible-doc ansible-doc-dev

pylint: pylint-modules

flake8:
	flake8 library

ansible-doc:
	(cd library; \
		$(DOCTEST) -M $(MODULE_DIR) bigip_command.py; \
		$(DOCTEST) -M $(MODULE_DIR) bigip_device_dns.py; \
$(DOCTEST) -M $(MODULE_DIR) bigip_device_ntp.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_dns_facts.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_dns.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_dns_zone.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_gtm_datacenter.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_hostname.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_iapp_service.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_iapp_template.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_irule.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_license.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_partition.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_provision.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_selfip.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_service.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_software.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_sysdb.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_ucs_fetch.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_ucs.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_user_facts.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_user.py; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_vlan.py; \
	)

ansible-doc-dev:
	(cd library; \
	 $(DOCTEST) -M $(MODULE_DIR) bigip_qkview_facts.py; \
	)

pylint-modules:
	(cd library; \
		$(PYLINT) f5/bigiq/bigiq.py; \
	)

fetch-upstream:
	curl -o library/bigip_facts.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_facts.py
	curl -o library/bigip_gtm_wide_ip.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_gtm_wide_ip.py
	curl -o library/bigip_monitor_http.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_monitor_http.py
	curl -o library/bigip_monitor_tcp.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_monitor_tcp.py
	curl -o library/bigip_node.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_node.py
	curl -o library/bigip_pool.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_pool.py
	curl -o library/bigip_pool_member.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_pool_member.py
	curl -o library/bigip_virtual_server.py https://raw.githubusercontent.com/ansible/ansible-modules-extras/devel/network/f5/bigip_virtual_server.py
