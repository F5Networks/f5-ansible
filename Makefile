# NOTE:
# 
# You need to install these packages on Ubunutu 12.04 to make this work:
# 
#     sudo apt-get install -y make python-stdeb fakeroot python-all rpm pep8 pylint
# 
#

DOCTEST := ./scripts/ansible-doc-test.py
PYHOOK := 'import sys;sys.path.insert(1,".")'
PYLINT := pylint --additional-builtins=_ --init-hook=$(PYHOOK)

all-tests: flake8 ansible-doc

flake8:
	flake8 .

ansible-doc:
	(
	$(DOCTEST) -M library/ bigip_command.py; \
	$(DOCTEST) -M library/ bigip_device_dns.py; \
	$(DOCTEST) -M library/ bigip_device_ntp.py; \
	$(DOCTEST) -M library/ bigip_dns_facts.py; \
	$(DOCTEST) -M library/ bigip_dns.py; \
	$(DOCTEST) -M library/ bigip_dns_zone.py; \
	$(DOCTEST) -M library/ bigip_gtm_datacenter.py; \
	$(DOCTEST) -M library/ bigip_hostname.py; \
	$(DOCTEST) -M library/ bigip_iapp_service.py; \
	$(DOCTEST) -M library/ bigip_iapp_template.py; \
	$(DOCTEST) -M library/ bigip_irule.py; \
	$(DOCTEST) -M library/ bigip_license.py; \
	$(DOCTEST) -M library/ bigip_partition.py; \
	$(DOCTEST) -M library/ bigip_provision.py; \
	$(DOCTEST) -M library/ bigip_qkview_facts.py; \
	$(DOCTEST) -M library/ bigip_selfip.py; \
	$(DOCTEST) -M library/ bigip_service.py; \
	$(DOCTEST) -M library/ bigip_software.py; \
	$(DOCTEST) -M library/ bigip_sysdb.py; \
	$(DOCTEST) -M library/ bigip_ucs_fetch.py; \
	$(DOCTEST) -M library/ bigip_ucs.py; \
	$(DOCTEST) -M library/ bigip_user_facts.py; \
	$(DOCTEST) -M library/ bigip_user.py; \
	$(DOCTEST) -M library/ bigip_vlan.py; \
	)
