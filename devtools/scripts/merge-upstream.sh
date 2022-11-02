#!/usr/bin/env bash

rm -rf /tmp/f5_modules_collection/ansible_collections
cp -R /tmp/f5ansible/.github /tmp/f5_modules_collection/
cp -R /tmp/f5ansible/ansible_collections /tmp/f5_modules_collection/.
cp /tmp/f5_modules_collection/ansible_collections/f5networks/f5_modules/README.md /tmp/f5_modules_collection/.

echo "Finished merging changes from upstream"
echo "Commit, tag and push to update Gitlab"
