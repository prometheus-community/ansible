<p><img src="https://www.circonus.com/wp-content/uploads/2015/03/sol-icon-itOps.png" alt="graph logo" title="graph" align="right" height="60" /></p>

# Ansible Role: node exporter

## Description

Deploy prometheus [node exporter](https://github.com/prometheus/node_exporter) using ansible.

## Requirements

- Ansible >= 2.9 (It might work on previous versions, but we cannot guarantee it)
- gnu-tar on Mac deployer host (`brew install gnu-tar`)
- Passlib is required when using the basic authentication feature (`pip install passlib[bcrypt]`)

## Role Variables

All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) file as well as in [meta/argument_specs.yml](meta/argument_specs.yml).
Please refer to the [collection docs](https://prometheus-community.github.io/ansible/branch/main/node_exporter_role.html) for description and default values of the variables.

## Example

### Playbook

Use it in a playbook as follows:
```yaml
- hosts: all
  roles:
    - prometheus.prometheus.node_exporter
```

### TLS config

Before running node_exporter role, the user needs to provision their own certificate and key.
```yaml
- hosts: all
  pre_tasks:
    - name: Create node_exporter cert dir
      file:
        path: "/etc/node_exporter"
        state: directory
        owner: root
        group: root

    - name: Create cert and key
      openssl_certificate:
        path: /etc/node_exporter/tls.cert
        csr_path: /etc/node_exporter/tls.csr
        privatekey_path: /etc/node_exporter/tls.key
        provider: selfsigned
  roles:
    - prometheus.prometheus.node_exporter
  vars:
    node_exporter_tls_server_config:
      cert_file: /etc/node_exporter/tls.cert
      key_file: /etc/node_exporter/tls.key
    node_exporter_basic_auth_users:
      randomuser: examplepassword
```


### Demo site

We provide an example site that demonstrates a full monitoring solution based on prometheus and grafana. The repository with code and links to running instances is [available on github](https://github.com/prometheus/demo-site) and the site is hosted on [DigitalOcean](https://digitalocean.com).

## Local Testing

The preferred way of locally testing the role is to use Docker and [molecule](https://github.com/ansible-community/molecule) (v3.x). You will have to install Docker on your system. See "Get started" for a Docker package suitable for your system. Running your tests is as simple as executing `molecule test`.

## Continuous Integration

Combining molecule and circle CI allows us to test how new PRs will behave when used with multiple ansible versions and multiple operating systems. This also allows use to create test scenarios for different role configurations. As a result we have quite a large test matrix which can take more time than local testing, so please be patient.

## Contributing

See [contributor guideline](CONTRIBUTING.md).

## Troubleshooting

See [troubleshooting](TROUBLESHOOTING.md).

## License

This project is licensed under MIT License. See [LICENSE](/LICENSE) for more details.
