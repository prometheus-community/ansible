from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import yaml
from testinfra_helpers import get_target_hosts
import os
import pytest

testinfra_hosts = get_target_hosts()


@pytest.fixture()
def AnsibleDefaults():
    with open("defaults/main.yml", 'r') as stream:
        return yaml.full_load(stream)


@pytest.mark.parametrize(
    "dirs",
    [
        "/etc/prometheus",
        "/etc/prometheus/console_libraries",
        "/etc/prometheus/consoles",
        "/etc/prometheus/rules",
        "/etc/prometheus/file_sd",
        "/etc/prometheus/scrape_configs",
        "/var/lib/prometheus",
    ],
)
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize(
    "files",
    [
        "/etc/prometheus/prometheus.yml",
        "/etc/prometheus/scrape_configs/empty_scrapes.yml",
        "/etc/systemd/system/prometheus.service",
        "/usr/local/bin/prometheus",
        "/usr/local/bin/promtool",
    ],
)
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


@pytest.mark.parametrize("files", [
    "/etc/prometheus/rules/ansible_managed.yml"
])
def test_absent(host, files):
    f = host.file(files)
    assert f.exists


def test_user(host):
    assert host.group("prometheus").exists
    assert host.user("prometheus").exists


def test_service(host):
    s = host.service("prometheus")
    try:
        assert s.is_running
    except AssertionError:
        # Capture service logs
        journal_output = host.run('journalctl -u prometheus --since "1 hour ago"')
        print("\n==== journalctl -u prometheus Output ====\n")
        print(journal_output)
        print("\n============================================\n")
        raise  # Re-raise the original assertion error


def test_socket(host):
    s = host.socket("tcp://0.0.0.0:9090")
    assert s.is_listening


def test_version(host, AnsibleDefaults):
    version = os.getenv('PROMETHEUS', AnsibleDefaults['prometheus_version'])
    run = host.run("/usr/local/bin/prometheus --version")
    out = run.stdout + run.stderr
    assert "prometheus, version " + version in out
