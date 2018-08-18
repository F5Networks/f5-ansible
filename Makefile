#vim: set tabstop=8:softtabstop=8:shiftwidth=8:noexpandtab

PYHOOK := 'import sys;sys.path.insert(1,".")'
PYLINT := pylint --additional-builtins=_ --init-hook=$(PYHOOK)

MODULE_TARGET = $(shell echo $@ | sed s/cov-// | tr '-' '_')

export ANSIBLE_KEEP_REMOTE_FILES=1
export ANSIBLE_CONFIG=./test/integration/ansible.cfg

generate-certs:
	cd test/integration && ansible-playbook -i inventory/hosts bigip_ssl_certificate.yaml --tags generate_certs

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
	cp library/plugins/action/bigip.py local/ansible/lib/ansible/plugins/action/ && \
    cp library/module_utils/network/f5/* local/ansible/lib/ansible/module_utils/network/f5/ && \
    cp library/utils/module_docs_fragments/f5.py local/ansible/lib/ansible/utils/module_docs_fragments/

find-ignores:
	cd local/ansible && ! find . -name *ignore* | egrep -v "(gitignore|dockerignore)" | xargs egrep "(bigip|bigiq)" -R

pyclean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
