from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("dirs", [
    "/etc/alertmanager",
    "/etc/alertmanager/templates",
    "/var/lib/alertmanager"
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("files", [
    "/usr/local/bin/alertmanager",
    "/usr/local/bin/amtool",
    "/etc/alertmanager/alertmanager.yml",
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


def test_socket(host):
    assert host.socket("tcp://0.0.0.0:9093").is_listening
