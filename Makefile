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

all-tests: style

docs:
	rm docs/modules/* || true
	python devtools/bin//plugin_formatter.py --module-dir library/ --template-dir devtools/templates/ --output-dir docs/modules/ -v
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

upgrade-ansible:
	pip install --upgrade git+https://github.com/ansible/ansible.git

clean-images:
	docker rmi --force $$(docker images -a -q)

clean-containers:
	docker rm $$(docker ps -a -q)

jenkins:
	openstack stack create -t heat/jenkins-secondary.yaml -e heat/jenkins-secondary-params.yaml jenkins-secondary-01 --wait

generate-certs:
	cd test/integration && ansible-playbook -i inventory/hosts bigip_ssl_certificate.yaml --tags generate_certs

# Install project requirements
requirements:
	pip install --user -r requirements.test.txt

# Build and test docs in a Docker container
docker-test:
	./docs/scripts/docker-docs.sh \
	pip install --user -r requirements.test.txt
	./docs/scripts/test-docs.sh



