#!/usr/bin/env bash

set -u -x -o pipefail

collection_root=$(pwd | grep -oP ".+\/ansible_collections\/\w+?\/\w+")
targetname=${PWD##*/}
role=$(expr "${targetname}" : '\w*-\(\w*\)-\w*')
role_root="${collection_root}/roles/${role}"
scenario=$(expr "${targetname}" : '\w*-\w*-\(\w*\)')

get_ansible_core_version() {
  python -c 'from ansible.release import __version__; print(__version__)'
}

get_ansible_core_series() {
  python - <<'PY'
from ansible.release import __version__
series = '.'.join(__version__.split('.')[:2])
print(series)
PY
}

initial_ansible_version="$(get_ansible_core_version)"
ansible_series="$(get_ansible_core_series)"
ansible_ref="stable-${ansible_series}"

if [ "$(printf '%s\n' "${initial_ansible_version}" "2.14" | sort -V | head -n1)" != "2.14" ]; then
       echo "ansible version 2.14 or greater is required!" >&2
       exit 1
fi

# Install package requirements
apt -y update
apt -y install docker.io

# Pin ansible-core to the already-installed stable- branch version for all pip installs below.
# This prevents pip from upgrading ansible-core while resolving Molecule or test dependencies.
requirements_file="$(mktemp)"
trap 'rm -f "${requirements_file}"' EXIT


python_test_requirements="${collection_root}/tests/integration/requirements.txt"

if [ -f "${python_test_requirements}" ]; then
  printf 'ansible-core @ https://github.com/ansible/ansible/archive/%s.tar.gz\n' "${ansible_ref}" > "${requirements_file}"
  printf -- '-r %s\n' "${python_test_requirements}" >> "${requirements_file}"

  python -m pip install --upgrade -r "${requirements_file}"
  python -m pip check
fi

# Define config locations within collection
export MOLECULE_FILE="${collection_root}/.config/molecule/config.yml"
export YAMLLINT_CONFIG_FILE="${collection_root}/.yamllint.yml"

# Unset ansible-test variables that break molecule
unset _ANSIBLE_COVERAGE_CONFIG
unset ANSIBLE_PYTHON_INTERPRETER

final_ansible_version="$(get_ansible_core_version)"
if [ "${final_ansible_version}" != "${initial_ansible_version}" ]; then
  echo "ansible version changed during script execution: ${initial_ansible_version} -> ${final_ansible_version}" >&2
  exit 1
fi

# Run molecule test
cd "${role_root}" || { echo "Fail to change directory into ${role_root}"; exit 1; }
molecule -c "${MOLECULE_FILE}" test -s "${scenario}"
