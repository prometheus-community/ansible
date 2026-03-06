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

python -m pip install molecule-plugins[docker]
ansible-galaxy collection install -r "$collection_root/requirements.yml"

# Install ansible version specific requirements
# 2.19 <= version
if [ "$(printf '%s\n' "2.19.0.0" "$ansible_version" | sort -V | head -n1)" = "2.19.0.0" ]; then
       python -m pip install molecule
# 2.15 <= version < 2.19
elif [ "$(printf '%s\n' "2.15.0.0" "$ansible_version" | sort -V | head -n1)" = "2.15.0.0" ]; then
       python -m pip install molecule
       ansible-galaxy collection install 'https://github.com/ansible-collections/community.general.git,stable-11'
# 2.14 <= version < 2.15
elif [ "$(printf '%s\n' "2.14.0.0" "$ansible_version" | sort -V | head -n1)" = "2.14.0.0" ]; then
       python -m pip install molecule
       ansible-galaxy collection install 'https://github.com/ansible-collections/community.general.git,stable-11' 'https://github.com/ansible-collections/ansible.posix.git,stable-1'
# 2.12 <= version < 2.14
elif [ "$(printf '%s\n' "2.12.0.0" "$ansible_version" | sort -V | head -n1)" = "2.12.0.0" ]; then
       python -m pip install "molecule<6"
       ansible-galaxy collection install 'https://github.com/ansible-collections/community.general.git,stable-11' 'https://github.com/ansible-collections/ansible.posix.git,stable-1'
else
       echo "ansible version 2.12 or greater is required!" >&2
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
