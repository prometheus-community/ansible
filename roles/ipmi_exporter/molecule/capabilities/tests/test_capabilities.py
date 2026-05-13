from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()


def test_udev_rule_exists(host):
    f = host.file("/etc/udev/rules.d/99-ipmi-exporter.rules")
    assert f.exists
    assert f.is_file


def test_udev_rule_permissions(host):
    f = host.file("/etc/udev/rules.d/99-ipmi-exporter.rules")
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644


def test_udev_rule_content(host):
    f = host.file("/etc/udev/rules.d/99-ipmi-exporter.rules")
    assert 'KERNEL=="ipmi*"' in f.content_string
    assert 'SUBSYSTEM=="ipmi"' in f.content_string
    assert 'GROUP="ipmi-exp"' in f.content_string
    assert 'MODE="0660"' in f.content_string


def test_service(host):
    s = host.service("ipmi_exporter")
    try:
        assert s.is_running
    except AssertionError:
        journal_output = host.run('journalctl -u ipmi_exporter --since "1 hour ago"')
        print("\n==== journalctl -u ipmi_exporter Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise


def test_socket(host):
    sockets = [
        "tcp://127.0.0.1:9290"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
