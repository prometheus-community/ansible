from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from testinfra_helpers import get_target_hosts
import pytest

testinfra_hosts = get_target_hosts()


@pytest.mark.parametrize("files", [
    "/etc/systemd/system/smokeping_prober.service",
    "/usr/local/bin/smokeping_prober"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_service(host):
    s = host.service("smokeping_prober")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u smokeping_prober --since "1 hour ago"')
        print("\n==== journalctl -u smokeping_prober Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_socket(host):
    s = host.socket("tcp://0.0.0.0:9374")
    assert s.is_listening
