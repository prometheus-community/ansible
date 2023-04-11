<p><img src="https://brand.systemd.io/assets/png/systemd-logomark.png" alt="systemd logo" title="systemd" align="right" height="60" /></p>

# Ansible Role: systemd exporter

## Description

Deploy prometheus [systemd exporter](https://github.com/prometheus-community/systemd_exporter) using ansible.

## Requirements

- Ansible >= 2.9 (It might work on previous versions, but we cannot guarantee it)
- gnu-tar on Mac deployer host (`brew install gnu-tar`)

## Role Variables

All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) file as well as in [meta/argument_specs.yml](meta/argument_specs.yml).
Please refer to the [collection docs](https://prometheus-community.github.io/ansible/branch/main/systemd_exporter_role.html) for description and default values of the variables.

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
