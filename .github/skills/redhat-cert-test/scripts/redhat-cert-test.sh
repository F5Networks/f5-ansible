#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../" && pwd)"
ARTIFACTS_DIR="$SKILL_ROOT/artifacts"
LOGS_DIR="$ARTIFACTS_DIR/logs"
TMP_DIR="$ARTIFACTS_DIR/tmp"
VENV_BASE_DIR="$ARTIFACTS_DIR/venvs"
DOWNLOAD_BASE_DIR="$ARTIFACTS_DIR/downloads"
EXTRACT_BASE_DIR="$ARTIFACTS_DIR/extract"
COLLECTIONS_CACHE_DIR="$ARTIFACTS_DIR/ansible_collections"

COLLECTION_ROOT="ansible_collections/f5networks/f5_modules"
VENV_DIR="$VENV_BASE_DIR/.venv-cert"
LOG_FILE="$LOGS_DIR/local-certification-check.$$.log"
LAST_STEP="initialization"
IMPORTER_RESULT_FILE="$ARTIFACTS_DIR/importer_result.json"
GALAXY_COLLECTION="${1:-}"
USE_GALAXY=false
TARBALL_PATH=""
PYTHON_VERSION="3.12"
ANSIBLE_VERSIONS=("2.16" "2.18" "2.20")
FAILED_CHECKS=()
STRICT_PYTHON_312="${STRICT_PYTHON_312:-true}"

# Detect Docker availability — CI runs ansible-test with --docker default, which
# uses quay.io/ansible/default-test-container and provides isolated Python
# environments (no pre-installed collections). Without Docker the sanity run is
# NOT identical to CI: netcommon will be on the path and only locally-installed
# Python versions will be tested.
#
# Set ALLOW_NO_DOCKER=true to proceed without Docker (non-identical to CI).
ALLOW_NO_DOCKER="${ALLOW_NO_DOCKER:-false}"
USE_DOCKER=false
DOCKER_UNAVAIL_REASON=""
if ! command -v docker &>/dev/null; then
  DOCKER_UNAVAIL_REASON="docker binary not found — install Docker Desktop"
elif ! docker info >/dev/null 2>&1; then
  DOCKER_UNAVAIL_REASON="Docker daemon not running — open Docker Desktop and wait for it to start, then retry"
else
  USE_DOCKER=true
fi

# Enforce Docker unless user explicitly opts out
if [[ "$USE_DOCKER" == "false" && "$ALLOW_NO_DOCKER" != "true" ]]; then
  echo "ERROR: $DOCKER_UNAVAIL_REASON"
  echo ""
  echo "This skill runs ansible-test with --docker default to be identical to the"
  echo "Red Hat CI pipeline. Without Docker, import failures (ModuleNotFoundError"
  echo "for ansible.netcommon) will not reproduce locally."
  echo ""
  echo "To proceed anyway (non-CI-identical, for quick lint/changelog checks only):"
  echo "  ALLOW_NO_DOCKER=true bash .github/skills/redhat-cert-test/scripts/redhat-cert-test.sh"
  exit 1
fi

print_failure_guidance() {
  echo "Suggested fixes:"
  if grep -q "Missing galaxy.yml at:" "$LOG_FILE"; then
    echo "- Ensure you are running from the repository root and that $COLLECTION_ROOT/galaxy.yml exists."
  fi
  if grep -qi "No module named galaxy_importer\|No module named ansible" "$LOG_FILE"; then
    echo "- The virtual environment may be broken. Delete $VENV_DIR and rerun the script."
  fi
  if grep -qi "Error running \`ansible-galaxy collection build\`" "$LOG_FILE"; then
    echo "- Validate collection metadata in $COLLECTION_ROOT/galaxy.yml and ensure the collection builds cleanly."
  fi
  if grep -qi "required tag\|CHECK_REQUIRED_TAGS" "$LOG_FILE"; then
    echo "- Add missing required Galaxy tags in $COLLECTION_ROOT/galaxy.yml under the tags field."
  fi
  if grep -qi "ImporterError" "$LOG_FILE"; then
    echo "- Review the importer error details in the log and fix the referenced module/doc/metadata issue."
  fi
  if grep -qi "Could not resolve\|Temporary failure\|Name or service not known\|Connection" "$LOG_FILE"; then
    echo "- Check network connectivity and retry; dependency download may have failed."
  fi
  echo "- See full log for exact failure context: $LOG_FILE"
}

fail_with_feedback() {
  local reason="$1"
  local fix="$2"
  local code="${3:-2}"
  echo "FAIL: Local certification check failed"
  echo "Reason: $reason"
  echo "Suggested fix: $fix"
  echo "Log: $LOG_FILE"
  exit "$code"
}

resolve_versions() {
  local uses_line ref
  uses_line="$(grep -E 'uses:[[:space:]]+ansible-collections/partner-certification-checker/.github/workflows/certification-reusable.yml@' .github/workflows/ci.yml | head -n1 || true)"

  if [[ -z "$uses_line" ]]; then
    echo "Could not find reusable workflow reference in .github/workflows/ci.yml."
    return
  fi

  ref="${uses_line##*@}"
  ref="$(echo "$ref" | awk '{print $1}')"
  ref="${ref%%#*}"

  echo "Using reusable workflow @${ref}"
}

get_lint_version() {
  local core_version="$1"
  local minor=$(echo "$core_version" | cut -d. -f2)
  
  if [[ $minor -ge 19 ]]; then
    echo "25.2.0"
  else
    echo "24.12.2"
  fi
}

print_collection_fix_proposals() {
  local phase="$1"
  local core_version="$2"
  local output_file="$3"
  local matched=0
  local fatal_block=""

  fatal_block="$(awk '
    /FATAL: The [0-9]+ sanity test\(s\) listed below/ {capture=1; next}
    capture && /^FAILED: ansible-test sanity/ {capture=0}
    capture && NF {print}
  ' "$output_file")"

  echo "Collection-side fix proposals for ansible-core $core_version ($phase):"

  if grep -q "No module named 'ansible_collections\." "$output_file"; then
    matched=1
    mapfile -t missing_deps < <(
      grep -o "ansible_collections\.[^']*" "$output_file" \
        | sed 's/^ansible_collections\.//' \
        | awk -F. 'NF >= 2 { print $1 "." $2 }' \
        | sort -u
    )
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
      for dep_name in "${missing_deps[@]}"; do
        echo "- Declare $dep_name in $COLLECTION_ROOT/galaxy.yml under dependencies and keep imports fully qualified so importer and sanity load the same sibling collection."
      done
    else
      echo "- A collection dependency import failed. Declare the missing collection in $COLLECTION_ROOT/galaxy.yml and ensure its modules are installed as sibling collections during validation."
    fi
    echo "- If a missing collection is only needed for runtime execution, guard that import so module argument_spec introspection can run without opening the transport stack during sanity checks."
  fi

  if grep -q "import-error:" "$output_file"; then
    matched=1
    echo "- Import failures mean one or more modules cannot be imported cleanly for ansible-test. Move heavy runtime imports into execute paths or helper methods so module import and argument_spec loading stay side-effect free."
  fi

  if printf '%s\n' "$fatal_block" | grep -qx "validate-modules"; then
    matched=1
    echo "- validate-modules failures usually come from drift between DOCUMENTATION and argument_spec. Reconcile option names, types, defaults, aliases, and choices in the failing modules before rerunning sanity."
  fi

  if printf '%s\n' "$fatal_block" | grep -qx "action-plugin-docs"; then
    matched=1
    echo "- action-plugin-docs failed. For each failing action plugin, make its DOCUMENTATION consistent with the paired module, or remove stale option docs from the action plugin if the module is the canonical source of documentation."
  fi

  if grep -qi "required tag\|CHECK_REQUIRED_TAGS" "$output_file"; then
    matched=1
    echo "- The collection metadata is missing required Galaxy tags. Add the missing tags to $COLLECTION_ROOT/galaxy.yml so importer validation passes."
  fi

  if grep -qi "ImporterError" "$output_file"; then
    matched=1
    echo "- ImporterError indicates a collection content issue, not a harness issue. Fix the referenced module docs, examples, or metadata in the collection and rerun the same ansible-core version."
  fi

  if [[ $matched -eq 0 ]]; then
    echo "- No known failure signature matched. Inspect the failing file paths above and fix the referenced collection code or metadata in this repository, then rerun the same ansible-core version."
  fi
}

cleanup_docker_test_artifacts() {
  # Each ansible-core version pulls a distinct quay.io/ansible/default-test-container
  # tag. Across the full 2.16/2.18/2.20 matrix these accumulate and can exhaust
  # local Docker disk space. Remove only this skill's own leftover containers and
  # images after each version so disk usage never grows across the run — this
  # does not touch unrelated images/build cache from other projects.
  local leftover_containers
  leftover_containers="$(docker ps -aq --filter "name=ansible-test-controller-" 2>/dev/null || true)"
  if [[ -n "$leftover_containers" ]]; then
    docker rm -f $leftover_containers >/dev/null 2>&1 || true
  fi

  local test_images
  test_images="$(docker images -q "quay.io/ansible/default-test-container" 2>/dev/null || true)"
  if [[ -n "$test_images" ]]; then
    docker rmi -f $test_images >/dev/null 2>&1 || true
  fi
}

on_error() {
  local exit_code=$?
  echo
  echo "FAIL: Local certification check failed"
  echo "Step: $LAST_STEP"
  echo "Exit code: $exit_code"
  echo "Log: $LOG_FILE"
  echo
  echo "Last 40 log lines:"
  tail -n 40 "$LOG_FILE" || true
  echo
  print_failure_guidance
  exit "$exit_code"
}

trap on_error ERR

mkdir -p "$LOGS_DIR" "$TMP_DIR" "$VENV_BASE_DIR" "$DOWNLOAD_BASE_DIR" "$EXTRACT_BASE_DIR" "$COLLECTIONS_CACHE_DIR"
exec > >(tee -a "$LOG_FILE") 2>&1

download_from_galaxy() {
  local collection="$1"
  local download_dir="$DOWNLOAD_BASE_DIR/galaxy-download-$$"
  
  mkdir -p "$download_dir"
  LAST_STEP="downloading collection from Galaxy"
  ansible-galaxy collection download "$collection" -p "$download_dir" >/dev/null 2>&1
  
  TARBALL_PATH="$(find "$download_dir" -name "*.tar.gz" | head -n1)"
  if [[ -z "$TARBALL_PATH" ]]; then
    fail_with_feedback "Failed to download $collection from Galaxy" "Ensure the collection exists and is published on Galaxy"
  fi
}

usage() {
  cat <<'EOF'
Usage: redhat-cert-test.sh [COLLECTION]

Without COLLECTION:
  Runs the certification check against the repository's local collection.
  Example: bash .github/skills/redhat-cert-test/scripts/redhat-cert-test.sh

With COLLECTION:
  Runs the certification check against a Galaxy-published collection.
  COLLECTION format: namespace.collection:version (e.g., f5networks.f5_modules:6.1.0)
  Example: bash .github/skills/redhat-cert-test/scripts/redhat-cert-test.sh f5networks.f5_modules:6.1.0

Tests against ansible-core versions: 2.16, 2.18, 2.20
Uses Python 3.12 by default (matching Red Hat's execution environment)

Sanity mode (auto-detected):
  Docker available  → ansible-test sanity -v --color --coverage --junit --docker default
                      Identical to CI. Reproduces all Python-version and import failures.
  Docker absent     → script exits with an error by default.
                      Set ALLOW_NO_DOCKER=true to proceed without Docker
                      (not CI-identical; import failures will not reproduce).

Requires Docker Desktop to be running. Start Docker Desktop before running this script.

Environment variables:
  STRICT_PYTHON_312=true|false (default: true)
    - true: requires python3.12 for all test runs (strict parity mode)
    - false: allows version-compatible fallback interpreters
  ALLOW_NO_DOCKER=true|false (default: false)
    - false: exits if Docker is unavailable (default, enforces CI parity)
    - true: runs without Docker (not CI-identical, import errors will not reproduce)
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

cd "$REPO_ROOT"

if [[ -n "$GALAXY_COLLECTION" ]]; then
  USE_GALAXY=true
  if [[ ! "$GALAXY_COLLECTION" =~ ^[a-z0-9_]+\.[a-z0-9_]+:[0-9]+(\.[0-9]+)+$ ]]; then
    fail_with_feedback "Invalid collection format" "Use namespace.collection:version (e.g., f5networks.f5_modules:6.1.0)"
  fi
else
  if [[ ! -f "$COLLECTION_ROOT/galaxy.yml" ]]; then
    fail_with_feedback "Missing galaxy.yml at $COLLECTION_ROOT/galaxy.yml" "Run from the f5-ansible repository root"
  fi
fi

echo "Log file: $LOG_FILE"
if [[ "$USE_DOCKER" == "true" ]]; then
  echo "Sanity mode: --docker default (CI-identical)"
else
  echo "Sanity mode: no Docker (ALLOW_NO_DOCKER=true — NOT identical to CI)"
fi

if [[ "$USE_GALAXY" == true ]]; then
  echo "Mode: Galaxy collection ($GALAXY_COLLECTION)"
  download_from_galaxy "$GALAXY_COLLECTION"
else
  echo "Mode: Local repository"
fi

LAST_STEP="resolving workflow versions"
resolve_versions

# Run a standalone, CI-identical ansible-lint production profile once (separate
# job in Red Hat's reusable workflow). This must run before the per-version
# sanity matrix and must NOT be routed through galaxy-importer (no --exclude
# flags). Use the first ansible-core version in the matrix to resolve the
# ansible-lint version the same way the CI job does.
LAST_STEP="running production ansible-lint (CI-equivalent)"
echo "Running standalone ansible-lint --profile=production (CI-equivalent)"
LINT_CORE_VERSION="${ANSIBLE_VERSIONS[0]}"
LINT_VER=$(get_lint_version "$LINT_CORE_VERSION")
LINT_VENV="$VENV_BASE_DIR/.venv-lint-${LINT_CORE_VERSION}"
if [[ ! -d "$LINT_VENV" ]]; then
  echo "  Creating lint virtualenv: $LINT_VENV"
  PYTHON_BIN=""
  if command -v python3.12 &>/dev/null; then
    PYTHON_BIN=python3.12
  elif command -v python3.11 &>/dev/null; then
    PYTHON_BIN=python3.11
  else
    PYTHON_BIN=python3
  fi
  "$PYTHON_BIN" -m venv "$LINT_VENV"
fi
# shellcheck source=/dev/null
source "$LINT_VENV/bin/activate"
python -m pip install --upgrade pip >/dev/null 2>&1
LAST_STEP="installing ansible-core and ansible-lint for standalone lint"
echo "  Installing ansible-core $LINT_CORE_VERSION and ansible-lint $LINT_VER"
pip install --quiet "ansible-core==${LINT_CORE_VERSION}.*" "ansible-lint==${LINT_VER}" >/dev/null 2>&1 || {
  echo "WARNING: Failed to install ansible-core/ansible-lint for standalone lint; skipping standalone lint step"
  deactivate 2>/dev/null || true
}

LAST_STEP="running standalone ansible-lint"
if [[ -d "$COLLECTION_ROOT" ]]; then
  (cd "$COLLECTION_ROOT" && ansible-lint --profile=production) 2>&1 | tee "$TMP_DIR/lint-production-output.log" || {
    echo "FAILED: standalone ansible-lint --profile=production"
    FAILED_CHECKS+=("lint-production")
    deactivate 2>/dev/null || true
  }
else
  echo "Skipping standalone lint: collection root $COLLECTION_ROOT not found"
fi
deactivate 2>/dev/null || true

# Test each ansible-core version
for ANSIBLE_VERSION in "${ANSIBLE_VERSIONS[@]}"; do
  echo ""
  echo "=========================================="
  echo "Testing against ansible-core $ANSIBLE_VERSION"
  echo "=========================================="
  
  # Select Python interpreter. Strict mode pins to Python 3.12 for Red Hat parity.
  VENV="${VENV_DIR}-${ANSIBLE_VERSION}"
  ANSIBLE_MINOR="$(echo "$ANSIBLE_VERSION" | cut -d. -f2)"

  LAST_STEP="preparing venv for ansible-core $ANSIBLE_VERSION"
  if [[ ! -d "$VENV" ]]; then
    echo "Creating virtual environment: $VENV"
    PYTHON_BIN=""
    if [[ "$STRICT_PYTHON_312" == "true" ]]; then
      if command -v python3.12 &>/dev/null; then
        PYTHON_BIN="python3.12"
      else
        echo "  SKIP: python3.12 is required in strict mode but is not available"
        FAILED_CHECKS+=("missing-python3.12-$ANSIBLE_VERSION")
        continue
      fi
    else
      if [[ $ANSIBLE_MINOR -ge 20 ]]; then
        # ansible-core 2.20+ requires Python 3.12+
        for v in python3.12 python3.13 python3.14; do
          command -v "$v" &>/dev/null && PYTHON_BIN="$v" && break
        done
      elif [[ $ANSIBLE_MINOR -ge 18 ]]; then
        # ansible-core 2.18+ requires Python 3.11+
        for v in python3.12 python3.13 python3.11 python3.14; do
          command -v "$v" &>/dev/null && PYTHON_BIN="$v" && break
        done
      else
        # ansible-core 2.16/2.17 requires Python 3.10+
        for v in python3.12 python3.11 python3.10 python3.13; do
          command -v "$v" &>/dev/null && PYTHON_BIN="$v" && break
        done
      fi
    fi
    if [[ -z "$PYTHON_BIN" ]]; then
      echo "  SKIP: No compatible Python found for ansible-core $ANSIBLE_VERSION"
      FAILED_CHECKS+=("no-compatible-python-$ANSIBLE_VERSION")
      continue
    fi
    echo "  (using $PYTHON_BIN)"
    "$PYTHON_BIN" -m venv "$VENV"
  fi

  # shellcheck source=/dev/null
  source "$VENV/bin/activate"
  python -m pip install --upgrade pip >/dev/null 2>&1

  LAST_STEP="installing ansible-core $ANSIBLE_VERSION"
  echo "  [1/5] Installing ansible-core $ANSIBLE_VERSION"
  if ! pip install "ansible-core==$ANSIBLE_VERSION.*" >/dev/null 2>&1; then
    echo "  FAILED: Could not install ansible-core $ANSIBLE_VERSION (Python version incompatible)"
    FAILED_CHECKS+=("install-$ANSIBLE_VERSION")
    deactivate 2>/dev/null || true
    continue
  fi
  
  LAST_STEP="installing importer and lint toolchain for $ANSIBLE_VERSION"
  echo "  [2/5] Installing galaxy-importer and ansible-lint"
  pip install "galaxy-importer==0.4.31" "invoke" >/dev/null 2>&1
  
  LINT_VER=$(get_lint_version "$ANSIBLE_VERSION")
  pip install "ansible-lint==$LINT_VER" >/dev/null 2>&1
  
  LAST_STEP="installing collection dependencies for $ANSIBLE_VERSION"
  echo "  [3/5] Installing collection dependencies"
  
  # Determine which galaxy.yml to use
  GALAXY_YML_PATH="$COLLECTION_ROOT/galaxy.yml"
  TEMP_EXTRACT=""
  if [[ "$USE_GALAXY" == true ]]; then
    TEMP_EXTRACT="/tmp/collection-extract-$$"
    mkdir -p "$TEMP_EXTRACT"
    tar -xzf "$TARBALL_PATH" -C "$TEMP_EXTRACT" --strip-components=1
    GALAXY_YML_PATH="$TEMP_EXTRACT/galaxy.yml"
  fi
  
  # Parse and install dependencies from galaxy.yml into the local ansible_collections/
  # cache directory and expose it through ANSIBLE_COLLECTIONS_PATH
  if [[ -f "$GALAXY_YML_PATH" ]]; then
    mapfile -t DEP_NAMES < <(awk '/^dependencies:/{flag=1;next}/^[^ ]/{flag=0}flag{gsub(/^[[:space:]]+/,"",$0);gsub(/:.*/,"",$0);if(NF) print}' "$GALAXY_YML_PATH")
    for dep_name in "${DEP_NAMES[@]}"; do
      if [[ -n "$dep_name" ]]; then
        echo "  - Installing dependency: $dep_name"
        ansible-galaxy collection install "$dep_name" -p "$ARTIFACTS_DIR" --force-with-deps >/dev/null 2>&1 || true
      fi
    done
  fi
  export ANSIBLE_COLLECTIONS_PATH="$COLLECTIONS_CACHE_DIR:$REPO_ROOT/ansible_collections"
  
  # Cleanup temp extraction if Galaxy mode
  [[ -n "$TEMP_EXTRACT" ]] && rm -rf "$TEMP_EXTRACT"
  
  LAST_STEP="running build/import validation for $ANSIBLE_VERSION"
  echo "  [4/5] Running build/import validation"
  cat > "$TMP_DIR/galaxy-importer.cfg" <<'EOF'
[galaxy-importer]
CHECK_REQUIRED_TAGS=True
# Disable galaxy-importer internal linting; Red Hat runs a separate
# ansible-lint --profile=production job from the collection root.
RUN_ANSIBLE_LINT=False
EOF
  export GALAXY_IMPORTER_CONFIG="$TMP_DIR/galaxy-importer.cfg"
  rm -f "$TMP_DIR"/f5networks-f5_modules-*.tar.gz
  rm -f "$IMPORTER_RESULT_FILE"
  IMPORT_OUTPUT="$(mktemp "$TMP_DIR/redhat-cert-import-${ANSIBLE_VERSION}.XXXXXX")"
  
  if [[ "$USE_GALAXY" == true ]]; then
    (cd "$TMP_DIR" && python -m galaxy_importer.main "$TARBALL_PATH" --output-path "$TMP_DIR") 2>&1 | tee "$IMPORT_OUTPUT" | tail -20 || {
      echo "FAILED: Import validation failed for ansible-core $ANSIBLE_VERSION"
      FAILED_CHECKS+=("import-$ANSIBLE_VERSION")
      print_collection_fix_proposals "import" "$ANSIBLE_VERSION" "$IMPORT_OUTPUT"
    }
  else
    (cd "$TMP_DIR" && python -m galaxy_importer.main --git-clone-path "$REPO_ROOT/$COLLECTION_ROOT" --output-path "$TMP_DIR") 2>&1 | tee "$IMPORT_OUTPUT" | tail -20 || {
      echo "FAILED: Import validation failed for ansible-core $ANSIBLE_VERSION"
      FAILED_CHECKS+=("import-$ANSIBLE_VERSION")
      print_collection_fix_proposals "import" "$ANSIBLE_VERSION" "$IMPORT_OUTPUT"
    }
  fi
  
  LAST_STEP="running ansible-test sanity for $ANSIBLE_VERSION"
  echo "  [5/5] Running ansible-test sanity"
  SANITY_OUTPUT="$(mktemp "$TMP_DIR/redhat-cert-sanity-${ANSIBLE_VERSION}.XXXXXX")"
  cd "$COLLECTION_ROOT" 2>/dev/null || cd .

  if [[ "$USE_DOCKER" == "true" ]]; then
    # Identical to CI: quay.io/ansible/default-test-container provides isolated
    # Python 3.8-3.13 without pre-installed collections, reproducing the exact
    # environment where netcommon ModuleNotFoundError failures appear.
    echo "    (Docker available — running with --docker default [quay.io/ansible/default-test-container])"
    SANITY_CMD="ansible-test sanity -v --color --coverage --junit --docker default"
  else
    # Docker not available — not identical to CI. netcommon will already be on
    # the path and only locally-installed Python versions will be tested.
    echo "    WARNING: NOT identical to CI — $DOCKER_UNAVAIL_REASON"
    echo "    Import errors (ModuleNotFoundError for netcommon) will not reproduce."
    SANITY_CMD="ansible-test sanity -v"
  fi

  if $SANITY_CMD 2>&1 | tee "$SANITY_OUTPUT" | tail -20; then
    echo "PASSED: ansible-test sanity for ansible-core $ANSIBLE_VERSION"
  else
    echo "FAILED: ansible-test sanity for ansible-core $ANSIBLE_VERSION"
    FAILED_CHECKS+=("sanity-$ANSIBLE_VERSION")
    print_collection_fix_proposals "sanity" "$ANSIBLE_VERSION" "$SANITY_OUTPUT"
  fi
  cd - >/dev/null 2>&1 || cd .

  if [[ "$USE_DOCKER" == "true" ]]; then
    echo "  Cleaning up Docker test containers/images for ansible-core $ANSIBLE_VERSION to free disk space"
    cleanup_docker_test_artifacts
  fi
  
  deactivate 2>/dev/null || true
done

echo ""
echo "=========================================="
echo "Summary"
echo "=========================================="

if [[ ${#FAILED_CHECKS[@]} -eq 0 ]]; then
  echo "PASS: All certification checks passed"
  echo "  Tested against: ${ANSIBLE_VERSIONS[*]}"
  echo "  Python version: $PYTHON_VERSION"
  echo "  Strict Python 3.12 mode: $STRICT_PYTHON_312"
  echo "  Docker mode (CI parity): $USE_DOCKER"
  echo "  Artifacts: $ARTIFACTS_DIR"
  exit 0
else
  echo "FAIL: Some checks failed:"
  for failed in "${FAILED_CHECKS[@]}"; do
    echo "  - $failed"
  done
  echo "  Docker mode (CI parity): $USE_DOCKER"
  echo "Log: $LOG_FILE"
  echo "Artifacts: $ARTIFACTS_DIR"
  exit 1
fi
