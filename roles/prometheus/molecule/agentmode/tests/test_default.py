from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import yaml
import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def AnsibleDefaults():
    with open("defaults/main.yml", 'r') as stream:
        return yaml.full_load(stream)


@pytest.mark.parametrize('file, content', [
    ("/etc/systemd/system/prometheus.service",
     "storage.agent.path=/var/lib/prometheus"),
    ("/etc/systemd/system/prometheus.service",
     "enable-feature=agent"),
])
def test_file_contents(host, file, content):
    f = host.file(file)
    assert f.exists
    assert f.is_file
    assert f.contains(content)


def test_service(host):
    s = host.service("prometheus")
    assert s.is_running


# # "/agent" page is available (http 200) when agent mode is enabled
def test_agent_enabled(host):
    output = host.check_output('curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:9090/agent')
    assert '200' in output


def test_socket(host):
    s = host.socket("tcp://0.0.0.0:9090")
    assert s.is_listening
