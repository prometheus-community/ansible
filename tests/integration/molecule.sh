#!/usr/bin/env bash

set -u -o pipefail

collection_root=$(pwd | grep -oP ".+\/ansible_collections\/\w+?\/\w+")
targetname=${PWD##*/}
role=$(expr "${targetname}" : '\w*-\(\w*\)-\w*')
role_root="${collection_root}/roles/${role}"
scenario=$(expr "${targetname}" : '\w*-\w*-\(\w*\)')
ansible_version="$(ansible --version | head -1 | sed 's/[^0-9\.]*//g')"

# Install package requirements
apt -y update
apt -y install docker.io

# Install test requirements from role
if [ -f "${role_root}/test-requirements.txt"  ]; then
  python -m pip install --upgrade -r "${role_root}/test-requirements.txt"
fi
# Install test requirements from collection
if [ -f "${collection_root}/test-requirements.txt"  ]; then
  python -m pip install --upgrade -r "${collection_root}/test-requirements.txt"
fi

# Install ansible version specific requirements
if [ "$(printf '%s\n' "2.14" "${ansible_version}" | sort -V | head -n1)" = "2.14" ]; then 
       ansible-galaxy collection install git+https://github.com/ansible-collections/community.docker.git
       ansible-galaxy collection install -r "${collection_root}/requirements.yml"
       # version >= 2.19
       if [ "$(printf '%s\n' "2.19" "${ansible_version}" | sort -V | head -n1)" = "2.19" ]; then
              python -m pip install -U --no-deps "molecule-plugins[docker]>=25.8.12"
       else
              python -m pip install -U --no-deps "molecule-plugins[docker]"
       fi
       # version <= 2.18
       if [ "$(printf '%s\n' "2.18.999.999" "${ansible_version}" | sort -V | head -n1)" = "${ansible_version}" ]; then
              ansible-galaxy collection install 'git+https://github.com/ansible-collections/community.general.git,stable-11'
       fi
       # version <= 2.14
       if [ "$(printf '%s\n' "2.14.999.999" "${ansible_version}" | sort -V | head -n1)" = "${ansible_version}" ]; then
              ansible-galaxy collection install 'git+https://github.com/ansible-collections/ansible.posix.git,stable-1'
       fi
else
       echo "ansible version 2.14 or greater is required!" >&2
       exit 1
fi

# Define config locations within collection
export MOLECULE_FILE=${collection_root}/.config/molecule/config.yml
export YAMLLINT_CONFIG_FILE=${collection_root}/.yamllint.yml

# Unset ansible-test variables that break molecule
unset _ANSIBLE_COVERAGE_CONFIG
unset ANSIBLE_PYTHON_INTERPRETER

# Run molecule test
cd "${role_root}" || { echo "Fail to change directory into ${role_root}"; exit 1; }
molecule -c "${collection_root}/.config/molecule/config.yml" test -s "${scenario}"
