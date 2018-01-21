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

all-tests:
	pycodestyle .
	bash test/ansible/sanity/correct-defaultdict-import.sh
	bash test/ansible/sanity/correct-iteritems-import.sh
	bash test/ansible/sanity/incorrect-comparisons.sh
	bash test/ansible/sanity/integration-test-idempotent-names.sh
	bash test/ansible/sanity/q-debugging-exists.sh
	python test/ansible/sanity/f5-sdk-install-missing-code-highlighting.py
	python test/ansible/sanity/short-description-ends-with-period.py

docs:
	rm docs/modules/* || true
	python devtools/bin/plugin_formatter.py --module-dir library/ --template-dir devtools/templates/ --output-dir docs/modules/ -v --limit-to $(shell ls -m library/bigip* library/bigiq* library/iworkflow* | sed -e 's/library\///g' | sed -e 's/.py//g' | sed -e 's/, /,/g' | tr -d '\n')
	cd docs && make html

style:
	pycodestyle .

export ANSIBLE_KEEP_REMOTE_FILES=1
export ANSIBLE_CONFIG=./test/integration/ansible.cfg

bigip_%:
	cd test/integration && ansible-playbook -i inventory/hosts ${MODULE_TARGET}.yaml -vvvv && cd -

bigiq_%:
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
	docker pull f5devcentral/containthedocs
	./docs/scripts/test-docs.sh

# Build and test docs in a Docker container
docker-test-debug:
	docker pull f5devcentral/containthedocs
	./docs/scripts/test-docs-debug.sh

# Deploy docs to clouddocs
docker-deploy:
	./docs/scripts/deploy-docs.sh publish-product-docs-to-prod orchestration/ansible devel

sync-to-upstream:
	ls local/ansible/lib/ansible/modules/network/f5/* | grep -v .pyc | egrep "(bigip|bigiq)" | xargs -I {} basename -s '.py' {} | xargs -I {} f5ansible module-upstream {} && \
	cp plugins/action/bigip.py local/ansible/lib/ansible/plugins/action/ && \
    cp library/module_utils/network/f5/* local/ansible/lib/ansible/module_utils/network/f5/ && \
    cp library/utils/module_docs_fragments/f5.py local/ansible/lib/ansible/utils/module_docs_fragments/

find-ignores:
	cd local/ansible && ! find . -name *ignore* | egrep -v "(gitignore|dockerignore)" | xargs egrep "(bigip|bigiq)" -R
