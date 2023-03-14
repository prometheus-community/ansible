<p><img src="https://www.circonus.com/wp-content/uploads/2015/03/sol-icon-itOps.png" alt="graph logo" title="graph" align="right" height="60" /></p>

# Ansible Role: mysqld exporter


Deploy prometheus [mysql exporter](https://github.com/prometheus/mysqld_exporter) using ansible.

## Requirements

- Ansible >= 2.7 (It might work on previous versions, but we cannot guarantee it)
- gnu-tar on Mac deployer host (`brew install gnu-tar`)
- Passlib is required when using the basic authentication feature (`pip install passlib[bcrypt]`)

## Role Variables

All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) and are listed in the table below.

| Name           | Default Value | Description                        |
| -------------- | ------------- | -----------------------------------|
| `mysqld_exporter_version` | 0.14.0 | mysqld exporter package version. Also accepts latest as parameter. |
| `mysqld_exporter_binary_local_dir` | "" | Enables the use of local packages instead of those distributed on github. The parameter may be set to a directory where the `mysqld_exporter` binary is stored on the host where ansible is run. This overrides the `mysqld_exporter_version` parameter |
| `mysqld_exporter_binary_url` | `https://github.com/prometheus/mysqld_exporter/releases/download/v{{ mysqld_exporter_version }}/mysqld_exporter-{{ mysqld_exporter_version }}.linux-{{ go_arch }}.tar.gz` | URL of the mysqld\_exporter binaries .tar.gz file |
| `mysqld_exporter_checksums_url` | `https://github.com/prometheus/mysqld_exporter/releases/download/v{{ mysqld_exporter_version }}/sha256sums.txt` | URL of the mysqld\_exporter checksums file |
| `mysqld_exporter_web_listen_address` | "0.0.0.0:9104" | Address on which mysqld\_exporter will listen |
| `mysqld_exporter_web_telemetry_path` | "/metrics" | Path under which to expose metrics |
| `mysqld_exporter_enabled_collectors` | `[]` | List of dicts defining additionally enabled collectors and their configuration. It adds collectors to [those enabled by default](https://github.com/prometheus/mysqld_exporter#collector-flags). |
| `mysqld_exporter_disabled_collectors` | [] | List of disabled collectors. By default mysqld_exporter disables collectors listed [here](https://github.com/prometheus/mysqld_exporter#collector-flags). |
| `mysqld_exporter_tls_server_config` | {} | Configuration for TLS authentication. Keys and values are the same as in [mysqld_exporter docs](https://github.com/prometheus/mysqld_exporter/blob/master/https/README.md#sample-config). |
| `mysqld_exporter_http_server_config` | {} | Config for HTTP/2 support. Keys and values are the same as in [mysqld_exporter docs](https://github.com/prometheus/mysqld_exporter/blob/master/https/README.md#sample-config). |
| `mysqld_exporter_basic_auth_users` | {} | Dictionary of users and password for basic authentication. Passwords are automatically hashed with bcrypt. |

## Example

### Playbook

Use it in a playbook as follows:
```yaml
- hosts: all
  collections:
    - prometheus.prometheus
  roles:
    - prometheus.prometheus.mysqld_exporter
```

### TLS config

Before running mysqld_exporter role, the user needs to provision their own certificate and key.
```yaml
- hosts: all
  pre_tasks:
    - name: Create mysqld_exporter cert dir
      ansible.builtin.file:
        path: "/etc/mysqld_exporter"
        state: directory
        owner: root
        group: root

    - name: Create cert and key
      community.crypto.x509_certificate:
        path: /etc/mysqld_exporter/tls.cert
        csr_path: /etc/mysqld_exporter/tls.csr
        privatekey_path: /etc/mysqld_exporter/tls.key
        provider: selfsigned
  collections:
    - prometheus.prometheus
  roles:
    - prometheus.prometheus.mysqld_exporter
  vars:
    mysqld_exporter_tls_server_config:
      cert_file: /etc/mysqld_exporter/tls.cert
      key_file: /etc/mysqld_exporter/tls.key
    mysqld_exporter_basic_auth_users:
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
