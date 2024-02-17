from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_directories(host):
    dirs = [
        "/etc/mongodb_exporter"
    ]
    for dir in dirs:
        d = host.file(dir)
        assert d.is_directory
        assert d.exists


def test_files(host):
    files = [
        "/etc/systemd/system/mongodb_exporter.service",
        "/usr/local/bin/mongodb_exporter"
    ]
    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.is_file


def test_user(host):
    assert host.group("mongodb-exp").exists
    assert "mongodb-exp" in host.user("mongodb-exp").groups
    assert host.user("mongodb-exp").shell == "/usr/sbin/nologin"
    assert host.user("mongodb-exp").home == "/"


def test_service(host):
    s = host.service("mongodb_exporter")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u mongodb_exporter --since "1 hour ago"')
        print("\n==== journalctl -u mongodb_exporter Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_protecthome_property(host):
    s = host.service("mongodb_exporter")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"


def test_socket(host):
    sockets = [
        "tcp://127.0.0.1:9216"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
