---
name: redhat-cert-test
description: "Run the repository-specific Red Hat certification check locally for f5-ansible, mirroring importer, lint, and sanity gates across the pinned ansible-core matrix. Use when workflow dispatch is unavailable or when you need a pre-PR local certification signal."
argument-hint: "Optional: namespace.collection:version to test a Galaxy release instead of local sources."
user-invocable: true
---

# Local Certification Check

## When To Use
- Reproduce certification workflow behavior without GitHub Actions.
- Validate import readiness before opening a PR.
- Run the exact importer gate this repo needs, with no inputs.

## Procedure
1. From repository root, run:
   bash .github/skills/redhat-cert-test/scripts/redhat-cert-test.sh

## What This Runs
- ansible-core matrix: 2.16, 2.18, 2.20
- galaxy-importer: 0.4.31
- ansible-lint: 24.12.2 for ansible-core <=2.18, 25.2.0 for >=2.19
- fixed collection root: ansible_collections/f5networks/f5_modules
- importer config:
  - CHECK_REQUIRED_TAGS=True
  - RUN_ANSIBLE_LINT=True

## Notes
- This skill runs locally and does not change branch protection or required checks.
- Runtime artifacts are written to .github/skills/redhat-cert-test/artifacts/.
- Default mode enforces Python 3.12 for strict Red Hat parity. Set STRICT_PYTHON_312=false to allow compatible fallback interpreters.
- Output ends with PASS on success.
- On failure, output starts with FAIL and includes step context, last log lines, and suggested fixes.
