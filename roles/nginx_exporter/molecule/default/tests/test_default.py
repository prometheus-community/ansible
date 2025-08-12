from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()


def test_directories(host):
    dirs = [
        "/etc/nginx_exporter"
    ]
    for dir in dirs:
        d = host.file(dir)
        assert d.is_directory
        assert d.exists


def test_files(host):
    files = [
        "/etc/systemd/system/nginx_exporter.service",
        "/usr/local/bin/nginx-prometheus-exporter"
    ]
    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.is_file


def test_user(host):
    assert host.group("nginx-exp").exists
    assert "nginx-exp" in host.user("nginx-exp").groups
    assert host.user("nginx-exp").shell == "/usr/sbin/nologin"


def test_service(host):
    s = host.service("nginx_exporter")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u nginx_exporter --since "1 hour ago"')
        print("\n==== journalctl -u nginx_exporter Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_protecthome_property(host):
    s = host.service("nginx_exporter")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"


def test_socket(host):
    sockets = [
        "tcp://127.0.0.1:9113"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
