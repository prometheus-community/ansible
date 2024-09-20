from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from testinfra_helpers import get_target_hosts
import pytest

testinfra_hosts = get_target_hosts()


@pytest.mark.parametrize("files", [
    "/etc/blackbox_exporter/blackbox_exporter.yml",
    "/etc/systemd/system/blackbox_exporter.service",
    "/usr/local/bin/blackbox_exporter"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_service(host):
    s = host.service("blackbox_exporter")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u blackbox_exporter --since "1 hour ago"')
        print("\n==== journalctl -u blackbox_exporter Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_socket(host):
    s = host.socket("tcp://0.0.0.0:9115")
    assert s.is_listening
