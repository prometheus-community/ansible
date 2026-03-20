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
import re
from ansible.release import __version__

match = re.match(r'^(\d+\.\d+)', __version__)
print(match.group(1))
PY
}

initial_ansible_version="$(get_ansible_core_version)"
ansible_series="$(get_ansible_core_series)"
ansible_ref="stable-${ansible_series}"

if [ "$(printf '%s\n' "${initial_ansible_version}" "2.14" | sort -V | head -n1)" != "2.14" ]; then
       echo "ansible version 2.14 or greater is required!" >&2
       exit 1
fi

# Pin ansible-core to the already-installed version for all pip installs below.
# This prevents pip from upgrading ansible-core while resolving Molecule or test dependencies.
#constraints_file="$(mktemp)"
#trap 'rm -f "${constraints_file}"' EXIT
#printf 'ansible-core==%s\n' "${initial_ansible_version}" > "${constraints_file}"
 

requirements_file="$(mktemp)"
trap 'rm -f "${requirements_file}"' EXIT

# Install package requirements
apt -y update
apt -y install docker.io

env

have_python_test_requirements=0
: > "${requirements_file}"

if [ -f "${collection_root}/test-requirements.txt" ] || [ -f "${role_root}/test-requirements.txt" ]; then
  printf 'ansible-core @ https://github.com/ansible/ansible/archive/%s.tar.gz\n' "${ansible_ref}" >> "${requirements_file}"

  if [ -f "${collection_root}/test-requirements.txt" ]; then
    printf -- '-r %s\n' "${collection_root}/test-requirements.txt" >> "${requirements_file}"
    have_python_test_requirements=1
  fi

  if [ -f "${role_root}/test-requirements.txt" ]; then
    printf -- '-r %s\n' "${role_root}/test-requirements.txt" >> "${requirements_file}"
    have_python_test_requirements=1
  fi
fi

if [ "${have_python_test_requirements}" -eq 1 ]; then
  python -m pip install --upgrade -r "${requirements_file}"
  python -m pip check
fi


# # Install python test requirements from collection
# if [ -f "${collection_root}/test-requirements.txt"  ]; then
#   python -m pip install --upgrade -c "${constraints_file}" -r "${collection_root}/test-requirements.txt"
# fi
# 
# # Install python test requirements from role
# if [ -f "${role_root}/test-requirements.txt"  ]; then
#   python -m pip install --upgrade -c "${constraints_file}" -r "${role_root}/test-requirements.txt"
# fi
# 
# # Verify installed Python packages have compatible dependencies
# python -m pip check

# Install molecule collection requirements
ansible-galaxy collection install git+https://github.com/ansible-collections/community.docker.git
# Install collection requirements
ansible-galaxy collection install -r "${collection_root}/requirements.yml"

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
molecule -c "${collection_root}/.config/molecule/config.yml" test -s "${scenario}"
