from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()


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
    sockets = [
        "tcp://127.0.0.1:9000"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
