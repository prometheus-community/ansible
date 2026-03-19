#!/usr/bin/env bash

set -u -o pipefail

collection_root=$(pwd | grep -oP ".+\/ansible_collections\/\w+?\/\w+")
targetname=${PWD##*/}
role=$(expr "${targetname}" : '\w*-\(\w*\)-\w*')
role_root="${collection_root}/roles/${role}"
scenario=$(expr "${targetname}" : '\w*-\w*-\(\w*\)')
initial_ansible_version="$("${pythonLocation}/pip" show ansible | grep Version: | sed -E 's/^Version: (.*)/\1/')"
ansible_version="${initial_ansible_version}"

if [ "$(printf '%s\n' "${ansible_version}" "2.14" | sort -V | head -n1)" != "2.14" ]; then
       echo "ansible version 2.14 or greater is required!" >&2
       exit 1
fi

# Pin ansible-core to the already-installed version for all pip installs below.
# This prevents pip from upgrading ansible-core while resolving Molecule or test dependencies.
constraints_file="$(mktemp)"
trap 'rm -f "${constraints_file}"' EXIT
printf 'ansible-core==%s\n' "${ansible_version}" > "${constraints_file}"
# version >= 2.19
if [ "$(printf '%s\n' "2.19" "${ansible_version}" | sort -V | head -n1)" = "2.19" ]; then
    printf 'molecule-plugins>=25.8.12\n' >> "${constraints_file}"
fi

# Install package requirements
apt -y update
apt -y install docker.io

# Install python test requirements from collection
if [ -f "${collection_root}/test-requirements.txt"  ]; then
  python -m pip install --upgrade -c "${constraints_file}" -r "${collection_root}/test-requirements.txt"
fi

# Install python test requirements from role
if [ -f "${role_root}/test-requirements.txt"  ]; then
  python -m pip install --upgrade -c "${constraints_file}" -r "${role_root}/test-requirements.txt"
fi

# Verify installed Python packages have compatible dependencies
python -m pip check

# Install molecule collection requirements
ansible-galaxy collection install git+https://github.com/ansible-collections/community.docker.git
# Install collection requirements
ansible-galaxy collection install -r "${collection_root}/requirements.yml"

# Downgrade collections for older versions of ansible (https://github.com/ansible/ansible/issues/78539)
# version <= 2.18
if [ "$(printf '%s\n' "2.18.999.999" "${ansible_version}" | sort -V | head -n1)" = "${ansible_version}" ]; then
    ansible-galaxy collection install 'git+https://github.com/ansible-collections/community.general.git,stable-11'
fi
# version <= 2.14
if [ "$(printf '%s\n' "2.14.999.999" "${ansible_version}" | sort -V | head -n1)" = "${ansible_version}" ]; then
    ansible-galaxy collection install 'git+https://github.com/ansible-collections/ansible.posix.git,stable-1'
fi

# Define config locations within collection
export MOLECULE_FILE="${collection_root}/.config/molecule/config.yml"
export YAMLLINT_CONFIG_FILE="${collection_root}/.yamllint.yml"

# Unset ansible-test variables that break molecule
unset _ANSIBLE_COVERAGE_CONFIG
unset ANSIBLE_PYTHON_INTERPRETER

final_ansible_version="$("${pythonLocation}/pip" show ansible | grep Version: | sed -E 's/^Version: (.*)/\1/')"
if [ "${final_ansible_version}" != "${initial_ansible_version}" ]; then
  echo "ansible version changed during script execution: ${initial_ansible_version} -> ${final_ansible_version}" >&2
  exit 1
fi

# Run molecule test
cd "${role_root}" || { echo "Fail to change directory into ${role_root}"; exit 1; }
molecule -c "${collection_root}/.config/molecule/config.yml" test -s "${scenario}"
