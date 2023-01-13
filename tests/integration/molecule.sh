#!/usr/bin/env bash

collection_root=$(pwd | grep -oP ".+\/ansible_collections\/\w+?\/\w+")
targetname=${PWD##*/}
role=$(expr "$targetname" : '\w*-\(\w*\)-\w*')
role_root="$collection_root/roles/$role"
scenario=$(expr "$targetname" : '\w*-\w*-\(\w*\)')
ansible_version="$(ansible --version | head -1 | sed 's/[^0-9\.]*//g')"

# Install package requirements
apt -y update
apt -y install docker.io

# Install test requirements from role
if [ -f "$role_root/test-requirements.txt"  ]; then
	python -m pip install -r "$role_root/test-requirements.txt"
fi
# Install test requirements from collection
if [ -f "$collection_root/test-requirements.txt"  ]; then
	python -m pip install -r "$collection_root/test-requirements.txt"
fi

# Install ansible version specific requirements
if [ "$(printf '%s\n' "2.12" "$ansible_version" | sort -V | head -n1)" = "2.12" ]; then 
       python -m pip install molecule molecule-plugins[docker]
else
       python -m pip install molecule molecule-docker
       ansible-galaxy collection install community.docker
       ansible-galaxy collection install -r "$collection_root/requirements.yml"
fi

# Define config locations within collection
export MOLECULE_FILE=$collection_root/.config/molecule/config.yml
export YAMLLINT_CONFIG_FILE=$collection_root/.config/yamllint/config.yml

# Unset ansible-test variables that break molecule
unset _ANSIBLE_COVERAGE_CONFIG
unset ANSIBLE_PYTHON_INTERPRETER

# Run molecule test
cd "$role_root"
molecule -c "$collection_root/.config/molecule/config.yml" test -s "$scenario"
