from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from testinfra_helpers import get_target_hosts
import pytest

testinfra_hosts = get_target_hosts()


def test_directories(host):
    dirs = [
        "/var/lib/nvidia_gpu_exporter"
    ]
    for dir in dirs:
        d = host.file(dir)
        assert not d.exists


def test_service(host):
    s = host.service("nvidia_gpu_exporter")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u nvidia_gpu_exporter --since "1 hour ago"')
        print("\n==== journalctl -u nvidia_gpu_exporter Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_protecthome_property(host):
    s = host.service("nvidia_gpu_exporter")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"


@pytest.mark.parametrize("sockets", [
    "tcp://127.0.1.1:9835",
])
def test_socket(host, sockets):
    assert host.socket(sockets).is_listening
