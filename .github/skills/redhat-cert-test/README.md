# Red Hat Certification Local Test

Replicates the complete Red Hat Ansible Automation Hub certification workflow
locally, including all three gates tested by Red Hat:

1. **Build/Import** — `galaxy-importer` with `CHECK_REQUIRED_TAGS=True` and `RUN_ANSIBLE_LINT=True`
2. **Lint** — `ansible-lint` at the production profile
3. **Sanity** — `ansible-test sanity` across all certified ansible-core versions

Tested ansible-core matrix: **2.16**, **2.18**, **2.20**  
Default Python: **3.12** (matches Red Hat's execution environment)


## Prerequisites

| Tool | Notes |
|------|-------|
| Docker Desktop (running) | Required by default. Sanity runs with `--docker default` (`quay.io/ansible/default-test-container`), identical to Red Hat CI. Without it, import failures (e.g. `ModuleNotFoundError`) will not reproduce. |
| `python3.12` | Required for strict mode (default). Used to run the harness itself (installing ansible-core, invoking `ansible-test`), not the sanity Python versions, which come from the container. Install via `brew install python@3.12` |
| `ansible-galaxy` | Provided by any ansible-core install |
| Network access | Downloads dependencies from Galaxy and pulls the test container image on first run |

If Docker is unavailable, the script exits with guidance by default. Set
`ALLOW_NO_DOCKER=true` to proceed anyway for quick lint/changelog checks only —
this mode is **not CI-identical** and will not reproduce import failures.


## Usage

Run from the **repository root**:

```bash
# Test local collection (current working tree)
bash .github/skills/redhat-cert-test/scripts/redhat-cert-test.sh

# Test a specific published Galaxy release
bash .github/skills/redhat-cert-test/scripts/redhat-cert-test.sh f5networks.f5_modules:1.42.0
```

### Modes

| Variable | Default | Meaning |
|----------|---------|---------|
| `STRICT_PYTHON_312` | `true` | Requires `python3.12` to run the harness. Fails fast with a clear message if not installed. Set to `false` to allow version-compatible fallback interpreters. |
| `ALLOW_NO_DOCKER` | `false` | If Docker is unavailable, exits with an error by default. Set to `true` to run sanity without Docker (not CI-identical; import failures will not reproduce). |

```bash
# Strict mode (default — matches Red Hat's environment exactly)
STRICT_PYTHON_312=true bash .github/skills/redhat-cert-test/scripts/redhat-cert-test.sh

# Fallback mode (uses best available compatible Python per ansible-core version)
STRICT_PYTHON_312=false bash .github/skills/redhat-cert-test/scripts/redhat-cert-test.sh

# Without Docker (not CI-identical — for quick lint/changelog checks only)
ALLOW_NO_DOCKER=true bash .github/skills/redhat-cert-test/scripts/redhat-cert-test.sh
```


## What It Tests

### Gate 1 — Build/Import (`galaxy-importer 0.4.31`)

- Builds a tarball from the collection and runs it through the same importer Red Hat uses
- Validates metadata, documentation, required tags, and module structure
- Runs ansible-lint at the production profile as part of import

### Gate 2 — Ansible Lint

| ansible-core | ansible-lint version |
|-------------|---------------------|
| 2.16, 2.18  | 24.12.2             |
| 2.19+       | 25.2.0              |

### Gate 3 — Sanity (`ansible-test sanity`)

Runs all applicable sanity tests including:
- `action-plugin-docs` — action plugins must have a matching module
- `import` — all plugins must be importable on all tested Python versions
- `validate-modules` — module documentation must match argument_spec
- `yamllint`, `compile`, `shebang`, `symlinks`, and others

**Python versions tested:** determined by the `quay.io/ansible/default-test-container`
image for each ansible-core version (identical to Red Hat CI), not by what's
installed locally. For example, ansible-core 2.20's container tests Python
3.9–3.14. Only the harness itself (installing ansible-core and invoking
`ansible-test`) needs a local Python 3.12.

If `ALLOW_NO_DOCKER=true` is set, only locally-installed Python versions are
tested and this is not equivalent to CI.

After each ansible-core version finishes, the script removes its own leftover
`ansible-test-controller-*` containers and `default-test-container` images to
keep Docker disk usage from growing across the 2.16/2.18/2.20 matrix.


## Collection Dependencies

The script reads `galaxy.yml` and installs declared collection dependencies into
the local `ansible_collections/` tree before running sanity, so `ansible-test`
can resolve cross-collection imports at analysis time.


## Artifacts

All runtime output is written under `.github/skills/redhat-cert-test/artifacts/`
and is excluded from git.

```
artifacts/
  logs/       # Per-run certification logs (local-certification-check.*.log)
  tmp/        # Per-run importer and sanity output captures
  venvs/      # Per-version virtual environments (.venv-cert-2.16, etc.)
  downloads/  # Galaxy collection tarballs (Galaxy mode only)
```

Clear venvs to force a clean reinstall:

```bash
rm -rf .github/skills/redhat-cert-test/artifacts/venvs/
```


## Output

The script prints a clear summary at the end:

```
==========================================
Summary
==========================================
PASS: All certification checks passed
  Tested against: 2.16 2.18 2.20
  Python version: 3.12
  Strict Python 3.12 mode: true
  Artifacts: .github/skills/redhat-cert-test/artifacts
```

On failure, each failing gate prints the test name, the collection-side fix
proposal, and the path to the full log:

```
FAILED: ansible-test sanity for ansible-core 2.20
Collection-side fix proposals for ansible-core 2.20 (sanity):
- action-plugin-docs failed. For each failing action plugin ...
```


## Relationship to CI

The `redhat_certification` job in `.github/workflows/ci.yml` runs
the same three-gate check via the upstream reusable workflow on every PR to
`devel`. This script lets you reproduce and debug
failures locally before pushing.

If the certification job is listed as a required status check in branch
protection, this script is the correct way to reproduce a CI failure locally.
