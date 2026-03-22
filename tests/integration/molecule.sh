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

# Pin ansible-core to the already-installed version for all pip installs below.
# This prevents pip from upgrading ansible-core while resolving Molecule or test dependencies.
#constraints_file="$(mktemp)"
#trap 'rm -f "${constraints_file}"' EXIT
#printf 'ansible-core==%s\n' "${initial_ansible_version}" > "${constraints_file}"
 

requirements_file="$(mktemp)"
trap 'rm -f "${requirements_file}"' EXIT

# Fixes for missing metadata
ls -l /root/ansible/pyproject.toml /root/ansible/setup.py /root/ansible/setup.cfg 2>/dev/null || true
python -m pip install -e /root/ansible
python -m pip show ansible-core || true

# Debug
echo "=== python / ansible debug ==="
pwd
whoami
python -V
command -v python
command -v ansible
env | sort

python - <<'PY'
import sys
print("sys.executable:", sys.executable)
print("sys.path:")
for p in sys.path:
    print("  ", p)

try:
    import ansible
    print("ansible.__file__:", ansible.__file__)
except Exception as e:
    print("import ansible failed:", repr(e))

try:
    from ansible.release import __version__
    print("ansible.release.__version__:", __version__)
except Exception as e:
    print("import ansible.release failed:", repr(e))
PY

ls -ld /root/ansible || true
find /root/ansible -maxdepth 3 \( -name release.py -o -name '*.dist-info' -o -name pyproject.toml -o -name PKG-INFO \) 2>/dev/null || true
python -m pip show ansible-core || true
echo "=== end debug ==="


echo '=== metadata inspect ==='

cat /root/ansible/lib/ansible_core.egg-info/PKG-INFO 2>/dev/null | sed -n '1,20p' || true

python - <<'PY'
from importlib.metadata import distributions, distribution

print("distribution('ansible-core'):")
try:
    d = distribution("ansible-core")
    print("  dist name:", d.metadata.get("Name"))
    print("  dist version:", d.version)
    print("  dist path:", d._path)
except Exception as e:
    print("  failed:", repr(e))

print("all installed dists containing 'ansible':")
for d in distributions():
    name = d.metadata.get("Name")
    if name and "ansible" in name.lower():
        print("  name:", name)
        print("  version:", d.version)
        print("  path:", d._path)
        print("  ---")
PY

python -m pip show ansible || true
python -m pip show ansible-core || true
ls -la /root/ansible/lib || true
ls -la /root/ansible/bin || true

echo '=== end metadata inspect ==='

# Install package requirements
apt -y update
apt -y install docker.io

have_python_test_requirements=0
: > "${requirements_file}"

if [ -f "${collection_root}/tests/integration/requirements.txt" ] || [ -f "${role_root}/test-requirements.txt" ]; then
  printf 'ansible-core @ https://github.com/ansible/ansible/archive/%s.tar.gz\n' "${ansible_ref}" >> "${requirements_file}"

  if [ -f "${collection_root}/tests/integration/requirements.txt" ]; then
    printf -- '-r %s\n' "${collection_root}/tests/integration/requirements.txt" >> "${requirements_file}"
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

# # Install molecule collection requirements
# ansible-galaxy collection install git+https://github.com/ansible-collections/community.docker.git
# # Install collection requirements
# ansible-galaxy collection install -r "${collection_root}/requirements.yml"

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
