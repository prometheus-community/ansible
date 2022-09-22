import pytest
import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("files", [
    "/etc/systemd/system/alertmanager.service",
    "/usr/local/bin/alertmanager",
    "/usr/local/bin/amtool"
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
    s = host.socket("tcp://0.0.0.0:9093")
    assert s.is_listening
