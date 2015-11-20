## f5-ansible-modules

This repository is a stop-gap place where we will be dropping Ansible
modules relevant to F5 products while we work with the Ansible community
to get them upstreamed.

Some modules, by their nature, may never make their way upstream, so this
will be where they live.

### Phase out policy

When a module in this repository is officially accepted into the upstream
Ansible project, it should be **removed** from this repository so as not
to confuse users.

From that point forward, development, bug fixes, etc should take place on
the Ansible github repository and follow their development workflow.

Should there be a desire, for any reason, to keep the modules in this repo,
I would suggest creating an "unsupported" sub directory and moving them to
there. A README should be included in that directory pointing to the upstream
Ansible repo that includes the modules. This should prevent any interested
parties from unassumingly downloading outdated code.
