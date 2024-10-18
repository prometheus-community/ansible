from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()


def test_files(host):
    files = [
        "/etc/systemd/system/influxdb_exporter.service",
        "/usr/local/bin/influxdb_exporter"
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
    assert host.group("influxdb-exp").exists
    assert "influxdb-exp" in host.user("influxdb-exp").groups
    assert host.user("influxdb-exp").shell == "/usr/sbin/nologin"
    assert host.user("influxdb-exp").home == "/etc/influxdb_exporter"


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
    sockets = [
        "tcp://127.0.0.1:9122"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
