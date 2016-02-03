# NOTE:
# 
# You need to install these packages on Ubunutu 12.04 to make this work:
# 
#     sudo apt-get install -y make python-stdeb fakeroot python-all rpm pep8 pylint
# 
#

DOCTEST := ../scripts/ansible-doc-test.py
MODULE_DIR := .
PYHOOK := 'import sys;sys.path.insert(1,".")'
PYLINT := pylint --additional-builtins=_ --init-hook=$(PYHOOK)

all-tests: flake8 ansible-doc
pylint: pylint-modules

flake8:
	flake8 . --exclude ansible-doc-test.py,bigip_qkview_facts.py,bigip_provision.py

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
	 $(DOCTEST) -M $(MODULE_DIR) bigip_qkview_facts.py; \
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

pylint-modules:
	(cd library; \
         $(PYLINT) f5/bigiq/bigiq.py; \
        )
