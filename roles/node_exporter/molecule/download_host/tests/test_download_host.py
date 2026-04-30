from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import testinfra

from testinfra_helpers import get_target_hosts

testinfra_hosts = get_target_hosts()

CACHE_PATH = "/tmp/node_exporter-managed-download-host"


def test_remote_download_cache(host):
    cache_dir = host.file(CACHE_PATH)
    assert cache_dir.exists
    assert cache_dir.is_directory

    cached_binary = host.file(f"{CACHE_PATH}/node_exporter")
    assert cached_binary.exists
    assert cached_binary.is_file

    downloaded_archive = host.run(
        f"find {CACHE_PATH} -maxdepth 1 -name '*.tar.gz' -print"
    )
    assert downloaded_archive.rc == 0
    assert downloaded_archive.stdout.strip()


def test_controller_cache_was_not_created():
    controller = testinfra.get_host("local://")
    cache_dir = controller.file(CACHE_PATH)
    assert not cache_dir.exists


def test_files(host):
    files = [
        "/etc/systemd/system/node_exporter.service",
        "/usr/local/bin/node_exporter",
    ]
    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.is_file


def test_service(host):
    s = host.service("node_exporter")
    try:
        assert s.is_running
    except AssertionError:
        journal_output = host.run('journalctl -u node_exporter --since "1 hour ago"')
        print("\n==== journalctl -u node_exporter Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise


def test_socket(host):
    assert host.socket("tcp://127.0.0.1:9100").is_listening
