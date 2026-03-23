#!/usr/bin/env bash

set -u -x -o pipefail

collection_root=$(pwd | grep -oP ".+\/ansible_collections\/\w+?\/\w+")
targetname=${PWD##*/}
role=$(expr "${targetname}" : '\w*-\(\w*\)-\w*')
role_root="${collection_root}/roles/${role}"
scenario=$(expr "${targetname}" : '\w*-\w*-\(\w*\)')
expected_ansible_version="$(cat "${collection_root}/.ansible-test-core-ref" 2>/dev/null || true)"
expected_ansible_version="${expected_ansible_version#stable-}"
actual_ansible_version="$(
  python - <<'PY'
from ansible.release import __version__
from packaging.version import Version

v = Version(__version__)
print(f"{v.major}.{v.minor}")
PY
)"

# Verify Ansible version
if [ "$(printf '%s\n' "${actual_ansible_version}" "2.14" | sort -V | head -n1)" != "2.14" ]; then
  echo "ansible version 2.14 or greater is required! got ${actual_ansible_version}" >&2
  exit 1
fi

if [ -n "${expected_ansible_version}" ] && [ "${expected_ansible_version}" != "${actual_ansible_version}" ]; then
  echo "ansible version mismatch: expected ${expected_ansible_version}, got ${actual_ansible_version}" >&2
  exit 1
fi

# Install package requirements
apt -y update
apt -y install docker.io

# Define config locations within collection
export MOLECULE_FILE="${collection_root}/.config/molecule/config.yml"
export YAMLLINT_CONFIG_FILE="${collection_root}/.yamllint.yml"

# Unset ansible-test variables that break molecule
unset _ANSIBLE_COVERAGE_CONFIG
unset ANSIBLE_PYTHON_INTERPRETER

# Run molecule test
cd "${role_root}" || { echo "Fail to change directory into ${role_root}"; exit 1; }
molecule -c "${MOLECULE_FILE}" test -s "${scenario}"
