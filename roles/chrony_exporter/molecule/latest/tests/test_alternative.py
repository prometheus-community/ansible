from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("files", [
    "/etc/systemd/system/chrony_exporter.service",
    "/usr/local/bin/chrony_exporter"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_service(host):
    s = host.service("chrony_exporter")
    # assert s.is_enabled
    assert s.is_running


def test_protecthome_property(host):
    s = host.service("chrony_exporter")
    p = s.systemd_properties
    assert p.get("ProtectHome") == "yes"


def test_socket(host):
    s = host.socket("tcp://0.0.0.0:9123")
    assert s.is_listening
