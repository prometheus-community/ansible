# Ansible Role: dns exporter

## Description

Deploy prometheus [dns exporter](https://github.com/tykling/dns_exporter), written in python, using ansible.

Possible Grafana dashboard: https://grafana.com/grafana/dashboards/20617-dns-exporter/

## Requirements

- Ansible >= 2.9 (It might work on previous versions, but we cannot guarantee it)
- gnu-tar on Mac deployer host (`brew install gnu-tar`)
- Passlib is required when using the basic authentication feature (`pip install passlib[bcrypt]`)

## Role Variables

All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) file as well as in [meta/argument_specs.yml](meta/argument_specs.yml).
Please refer to the [collection docs](https://prometheus-community.github.io/ansible/branch/main/dns_exporter_role.html) for description and default values of the variables.

## Example

### Playbook

Use it in a playbook as follows:
```yaml
- hosts: all
  roles:
    - prometheus.prometheus.dns_exporter
```

## Local Testing

The preferred way of locally testing the role is to use Docker and [molecule](https://github.com/ansible-community/molecule) (v3.x). You will have to install Docker on your system. See "Get started" for a Docker package suitable for your system. Running your tests is as simple as executing `molecule test`.

## Continuous Integration

Combining molecule and circle CI allows us to test how new PRs will behave when used with multiple ansible versions and multiple operating systems. This also allows use to create test scenarios for different role configurations. As a result we have quite a large test matrix which can take more time than local testing, so please be patient.

## Contributing

See [contributor guideline](CONTRIBUTING.md).

## Troubleshooting

See [troubleshooting](TROUBLESHOOTING.md).

Manual test
```
curl -v "http://127.0.0.1:15353/query?query_name=gmail.com&server=127.0.0.2:53"
curl -v "http://127.0.0.1:15353/query?module=internal_a_v4&module=internalbind_a_v4&module=internaldnscrypt_a_v4&query_name=youtube.com"
```

## License

This project is licensed under MIT License. See [LICENSE](/LICENSE) for more details.
