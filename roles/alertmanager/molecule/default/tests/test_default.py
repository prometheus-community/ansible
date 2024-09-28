from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()


@pytest.mark.parametrize("dirs", [
    "/etc/alertmanager",
    "/etc/alertmanager/templates",
    "/var/lib/alertmanager"
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("files", [
    "/usr/local/bin/alertmanager",
    "/usr/local/bin/amtool",
    "/etc/alertmanager/alertmanager.yml",
    "/etc/systemd/system/alertmanager.service"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_service(host):
    s = host.service("alertmanager")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u alertmanager --since "1 hour ago"')
        print("\n==== journalctl -u alertmanager Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_socket(host):
    assert host.socket("tcp://0.0.0.0:9093").is_listening
