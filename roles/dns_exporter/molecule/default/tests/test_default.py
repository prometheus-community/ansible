from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()


def test_directories(host):
    dirs = [
        "/var/lib/dns_exporter"
    ]
    for dir in dirs:
        d = host.file(dir)
        assert d.is_directory
        assert d.exists


def test_files(host):
    files = [
        "/etc/systemd/system/dns_exporter.service",
        "/usr/local/bin/dns_exporter"
    ]
    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.is_file


def test_permissions_didnt_change(host):
    dirs = [
        "/etc",
        "/root",
        "/usr",
        "/var"
    ]
    for file in dirs:
        f = host.file(file)
        assert f.exists
        assert f.is_directory
        assert f.user == "root"
        assert f.group == "root"


def test_user(host):
    assert host.group("dns-exp").exists
    assert "dns-exp" in host.user("dns-exp").groups
    assert host.user("dns-exp").shell == "/usr/sbin/nologin"


def test_service(host):
    s = host.service("dns_exporter")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u dns_exporter --since "1 hour ago"')
        print("\n==== journalctl -u dns_exporter Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_protecthome_property(host):
    s = host.service("dns_exporter")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"


def test_socket(host):
    sockets = [
        "tcp://127.0.0.1:15353"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
