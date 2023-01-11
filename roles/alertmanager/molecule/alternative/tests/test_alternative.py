from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("dirs", [
    "/opt/am/etc",
    "/opt/am/etc/templates",
    "/opt/am/lib"
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("files", [
    "/usr/local/bin/alertmanager",
    "/usr/local/bin/amtool",
    "/opt/am/etc/alertmanager.yml",
    "/etc/systemd/system/alertmanager.service"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_service(host):
    s = host.service("alertmanager")
    # assert s.is_enabled
    assert s.is_running


@pytest.mark.parametrize("sockets", [
    "tcp://127.0.0.1:9093",
    "tcp://127.0.0.1:6783"
])
def test_socket(host, sockets):
    assert host.socket(sockets).is_listening
