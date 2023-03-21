<p><img src="https://www.circonus.com/wp-content/uploads/2015/03/sol-icon-itOps.png" alt="graph logo" title="graph" align="right" height="60" /></p>

# Ansible Role: node exporter

## Description

Deploy prometheus [node exporter](https://github.com/prometheus/node_exporter) using ansible.

## Requirements

- Ansible >= 2.7 (It might work on previous versions, but we cannot guarantee it)
- gnu-tar on Mac deployer host (`brew install gnu-tar`)
- Passlib is required when using the basic authentication feature (`pip install passlib[bcrypt]`)

## Role Variables

All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) and are listed in the table below.

| Name           | Default Value | Description                        |
| -------------- | ------------- | -----------------------------------|
| `node_exporter_version` | 1.1.2 | Node exporter package version. Also accepts `latest` as parameter. |
| `node_exporter_binary_local_dir` | "" | Enables the use of local packages instead of those distributed on github. The parameter may be set to a directory where the `node_exporter` binary is stored on the host where ansible is run. This overrides the `node_exporter_version` parameter |
| `node_exporter_binary_url` | `https://github.com/prometheus/node_exporter/releases/download/v{{ node_exporter_version }}/node_exporter-{{ node_exporter_version }}.linux-{{ go_arch }}.tar.gz` | URL of the node exporter binaries .tar.gz file |
| `node_exporter_checksums_url` | `https://github.com/prometheus/node_exporter/releases/download/v{{ node_exporter_version }}/sha256sums.txt` | URL of the node exporter checksums file |
| `node_exporter_web_listen_address` | "0.0.0.0:9100" | Address on which node exporter will listen |
| `node_exporter_web_telemetry_path` | "/metrics" | Path under which to expose metrics |
| `node_exporter_enabled_collectors` | ```["systemd",{textfile: {directory: "{{node_exporter_textfile_dir}}"}}]``` | List of dicts defining additionally enabled collectors and their configuration. It adds collectors to [those enabled by default](https://github.com/prometheus/node_exporter#enabled-by-default). |
| `node_exporter_disabled_collectors` | [] | List of disabled collectors. By default node_exporter disables collectors listed [here](https://github.com/prometheus/node_exporter#disabled-by-default). |
| `node_exporter_textfile_dir` | "/var/lib/node_exporter" | Directory used by the [Textfile Collector](https://github.com/prometheus/node_exporter#textfile-collector). To get permissions to write metrics in this directory, users must be in `node-exp` system group. __Note__: More information in TROUBLESHOOTING.md guide.
| `node_exporter_tls_server_config` | {} | Configuration for TLS authentication. Keys and values are the same as in [node_exporter docs](https://github.com/prometheus/node_exporter/blob/master/https/README.md#sample-config). |
| `node_exporter_http_server_config` | {} | Config for HTTP/2 support. Keys and values are the same as in [node_exporter docs](https://github.com/prometheus/node_exporter/blob/master/https/README.md#sample-config). |
| `node_exporter_basic_auth_users` | {} | Dictionary of users and password for basic authentication. Passwords are automatically hashed with bcrypt. |

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
