from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from testinfra_helpers import get_target_hosts
import pytest

testinfra_hosts = get_target_hosts()


@pytest.mark.parametrize("files", [
    "/etc/systemd/system/snmp_exporter.service",
    "/usr/local/bin/snmp_exporter",
    "/etc/snmp_exporter/snmp.yml"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_service(host):
    s = host.service("snmp_exporter")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u snmp_exporter --since "1 hour ago"')
        print("\n==== journalctl -u snmp_exporter Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


@pytest.mark.parametrize("sockets", [
    "tcp://127.0.0.1:9116",
    "tcp://127.0.1.1:9116",
])
def test_socket(host, sockets):
    assert host.socket(sockets).is_listening
