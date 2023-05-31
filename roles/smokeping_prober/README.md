<p><img src="https://www.circonus.com/wp-content/uploads/2015/03/sol-icon-itOps.png" alt="graph logo" title="graph" align="right" height="60" /></p>

# Ansible Role: smokeping_prober

Deploy prometheus [smokeping_prober](https://github.com/superq/smokeping_prober) using ansible.

## Requirements

- Ansible >= 2.9 (It might work on previous versions, but we cannot guarantee it)
- gnu-tar on Mac deployer host (`brew install gnu-tar`)
- Passlib is required when using the basic authentication feature (`pip install passlib[bcrypt]`)

## Role Variables
All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) file as well as in [meta/argument_specs.yml](meta/argument_specs.yml).
Please refer to the [collection docs](https://prometheus-community.github.io/ansible/branch/main/smokeping_prober_role.html) for description and default values of the variables.

## Example

### Playbook

Use it in a playbook as follows:
```yaml
- hosts: all
  collections:
    - prometheus.prometheus
  roles:
    - prometheus.prometheus.smokeping_prober
```

### TLS config

Before running smokeping_prober role, the user needs to provision their own certificate and key.
```yaml
- hosts: all
  pre_tasks:
    - name: Create smokeping_prober cert dir
      ansible.builtin.file:
        path: "/etc/smokeping_prober"
        state: directory
        owner: root
        group: root

    - name: Create cert and key
      community.crypto.x509_certificate:
        path: /etc/smokeping_prober/tls.cert
        csr_path: /etc/smokeping_prober/tls.csr
        privatekey_path: /etc/smokeping_prober/tls.key
        provider: selfsigned
  collections:
    - prometheus.prometheus
  roles:
    - prometheus.prometheus.smokeping_prober
  vars:
    smokeping_prober_tls_server_config:
      cert_file: /etc/smokeping_prober/tls.cert
      key_file: /etc/smokeping_prober/tls.key
    smokeping_prober_basic_auth_users:
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
