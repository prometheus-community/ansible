from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("files", [
    "/etc/systemd/system/systemd_exporter.service",
    "/usr/local/bin/systemd_exporter"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_service(host):
    s = host.service("systemd_exporter")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u systemd_exporter --since "1 hour ago"')
        print("\n==== journalctl -u systemd_exporter Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_socket(host):
    s = host.socket("tcp://0.0.0.0:9558")
    assert s.is_listening
