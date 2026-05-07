from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from testinfra_helpers import get_target_hosts
import pytest

testinfra_hosts = get_target_hosts()


def test_service(host):
    s = host.service("cadvisor")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u cadvisor --since "1 hour ago"')
        print("\n==== journalctl -u cadvisor Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_protecthome_property(host):
    s = host.service("cadvisor")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"


@pytest.mark.parametrize("sockets", [
    "tcp://127.0.0.1:8000",
])
def test_socket(host, sockets):
    assert host.socket(sockets).is_listening


def test_forbidden_access(host):
    output = host.check_output('curl -s -o /dev/null -w "%{http_code}" -L http://127.0.0.1:8000/')
    assert '401' in output


def test_granted_access(host):
    output = host.check_output('curl -s -o /dev/null -w "%{http_code}" -L http://127.0.0.1:8000/ -u foo:bar')
    assert '200' in output
