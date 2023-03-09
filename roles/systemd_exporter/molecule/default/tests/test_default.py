from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_files(host):
    files = [
        "/etc/systemd/system/systemd_exporter.service",
        "/usr/local/bin/systemd_exporter"
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
    assert host.group("systemd-exporter").exists
    assert "systemd-exporter" in host.user("systemd-exporter").groups
    assert host.user("systemd-exporter").shell == "/usr/sbin/nologin"
    assert host.user("systemd-exporter").home == "/"


# def test_service(host):
#     s = host.service("systemd_exporter")
# #    assert s.is_enabled
#     assert s.is_running


def test_socket(host):
    sockets = [
        "tcp://127.0.0.1:9558"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
