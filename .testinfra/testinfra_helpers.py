import os
import testinfra


def get_ansible_version():
    """
    Get the current Ansible version from localhost using the 'debug' module.

    Returns:
        str: The current Ansible version (major.minor).
    """
    localhost = testinfra.get_host(
        "ansible://localhost?ansible_inventory=localhost,"
    )
    local_ansible_version = localhost.ansible("debug", "var=ansible_version")
    ansible_version = '.'.join(
        local_ansible_version['ansible_version']['full'].split('.')[:2]
    )
    return ansible_version


def filter_compatible_hosts(inventory, ansible_version):
    """
    Filter hosts based on Ansible version compatibility.

    Args:
        inventory (str): The inventory file path.
        ansible_version (str): The current Ansible version (major.minor).

    Returns:
        list: A list of compatible hosts that do not have the current Ansible
        version in their exclude_ansible_vers hostvars.
    """
    ansible_runner = testinfra.utils.ansible_runner.AnsibleRunner(inventory)
    all_hosts = ansible_runner.get_hosts('all')
    compatible_hosts = []

    for host in all_hosts:
        # Get host variables
        host_vars = ansible_runner.get_variables(host)

        # Check if the host should be excluded
        if 'exclude_ansible_vers' in host_vars:
            excluded_versions = host_vars['exclude_ansible_vers']
            if ansible_version in excluded_versions:
                continue
        compatible_hosts.append(host)

    return compatible_hosts


def get_target_hosts():
    """
    Get the filtered target hosts based on the current Ansible version.

    Returns:
        list: A list of hosts that are compatible with
        the current Ansible version.
    """
    # Get current Ansible version
    current_ansible_version = get_ansible_version()

    # Get the inventory file from environment
    inventory_file = os.environ['MOLECULE_INVENTORY_FILE']

    # Filter the hosts based on the exclusion criteria
    return filter_compatible_hosts(inventory_file, current_ansible_version)
