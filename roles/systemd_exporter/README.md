<p><img src="https://brand.systemd.io/assets/png/systemd-logomark.png" alt="systemd logo" title="systemd" align="right" height="60" /></p>

# Ansible Role: systemd exporter

## Description

Deploy prometheus [systemd exporter](https://github.com/prometheus-community/systemd_exporter) using ansible.

## Requirements

- Ansible >= 2.9 (It might work on previous versions, but we cannot guarantee it)
- gnu-tar on Mac deployer host (`brew install gnu-tar`)

## Role Variables

All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) file as well as in table below.

| Name           | Default Value | Description                        |
| -------------- | ------------- | -----------------------------------|
| `systemd_exporter_version` | 0.4.0 | SystemD exporter package version. Also accepts latest as parameter. |
| `systemd_exporter_skip_install` | false | SystemD exporter installation tasks gets skipped when set to true. |
| `systemd_exporter_binary_local_dir` | "" | Allows to use local packages instead of ones distributed on github. As parameter it takes a directory where `systemd_exporter` binary is stored on host on which ansible is ran. This overrides `systemd_exporter_version` parameter |
| `systemd_exporter_binary_url` | `https://github.com/prometheus-community/systemd_exporter/releases/download/v{{ systemd_exporter_version }}/systemd_exporter-{{ systemd_exporter_version }}.linux-{{ go_arch }}.tar.gz` | URL of the systemd exporter binaries .tar.gz file |
| `systemd_exporter_checksums_url` | `https://github.com/prometheus-community/systemd_exporter/releases/download/v{{ systemd_exporter_version }}/sha256sums.txt` | URL of the systemd exporter checksums file |
| `systemd_exporter_web_listen_address` | "0.0.0.0:9558" | Address on which systemd exporter will listen |
| `systemd_exporter_enable_restart_count` | false | Enables service restart count metrics. This feature only works with systemd 235 and above |
| `systemd_exporter_enable_ip_accounting` | false | Enables service ip accounting metrics. This feature only works with systemd 235 and above |
| `systemd_exporter_enable_file_descriptor_size` | false | Enables file descriptor size metrics. This feature will cause exporter to run as root as it needs access to /proc/X/fd |
| `systemd_exporter_unit_allowlist` | "" | Include some systemd units. Expects a regex. More in https://github.com/prometheus-community/systemd_exporter#configuration |
| `systemd_exporter_unit_denylist` | "" | Exclude some systemd units. Expects a regex. More in https://github.com/prometheus-community/systemd_exporter#configuration |

## Example

### Playbook

Use it in a playbook as follows:
```yaml
- hosts: all
  roles:
    - prometheus.prometheus.systemd_exporter
```

## Local Testing

The preferred way of locally testing the role is to use Docker and [molecule](https://github.com/ansible-community/molecule) (v3.x). You will have to install Docker on your system. See "Get started" for a Docker package suitable to for your system. Running your tests is as simple as executing `molecule test`.

## Continuous Intergation

Combining molecule and circle CI allows us to test how new PRs will behave when used with multiple ansible versions and multiple operating systems. This also allows use to create test scenarios for different role configurations. As a result we have a quite large test matrix which can take more time than local testing, so please be patient.

## Contributing

See [contributor guideline](CONTRIBUTING.md).

## Troubleshooting

See [troubleshooting](TROUBLESHOOTING.md).

## License

This project is licensed under MIT License. See [LICENSE](/LICENSE) for more details.
