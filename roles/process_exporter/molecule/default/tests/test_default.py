import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_directories(host):
    dirs = [
        "/etc/process_exporter"
    ]
    for dir in dirs:
        d = host.file(dir)
        assert d.is_directory
        assert d.exists


def test_files(host):
    files = [
        "/etc/systemd/system/process_exporter.service",
        "/usr/local/bin/process_exporter",
    ]
    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.is_file


def test_user(host):
    assert host.group("process-exp").exists
    assert "process-exp" in host.user("process-exp").groups
    assert host.user("process-exp").shell == "/usr/sbin/nologin"
    assert host.user("process-exp").home == "/"


def test_service(host):
    s = host.service("process_exporter")
#    assert s.is_enabled
    assert s.is_running


def test_socket(host):
    sockets = [
        "tcp://0.0.0.0:9256"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
