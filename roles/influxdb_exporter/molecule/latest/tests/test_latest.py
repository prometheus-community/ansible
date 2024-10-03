from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from testinfra_helpers import get_target_hosts
import pytest

testinfra_hosts = get_target_hosts()


@pytest.mark.parametrize("files", [
    "/etc/systemd/system/influxdb_exporter.service",
    "/usr/local/bin/influxdb_exporter"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_service(host):
    s = host.service("influxdb_exporter")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u influxdb_exporter --since "1 hour ago"')
        print("\n==== journalctl -u influxdb_exporter Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_socket(host):
    s = host.socket("tcp://0.0.0.0:9122")
    assert s.is_listening
