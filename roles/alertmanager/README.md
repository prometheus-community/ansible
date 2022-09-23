<p><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Human-dialog-warning.svg/2000px-Human-dialog-warning.svg.png" alt="alert logo" title="alert" align="right" height="60" /></p>

# Ansible Role: alertmanager

## Description

Deploy and manage Prometheus [alertmanager](https://github.com/prometheus/alertmanager) service using ansible.

## Requirements

- Ansible >= 2.7 (It might work on previous versions, but we cannot guarantee it)

It would be nice to have prometheus installed somewhere

## Role Variables

All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) file as well as in table below.

| Name           | Default Value | Description                        |
| -------------- | ------------- | -----------------------------------|
| `alertmanager_version` | 0.21.0 | Alertmanager package version. Also accepts `latest` as parameter. |
| `alertmanager_binary_local_dir` | "" | Allows to use local packages instead of ones distributed on github. As parameter it takes a directory where `alertmanager` AND `amtool` binaries are stored on host on which ansible is ran. This overrides `alertmanager_version` parameter |
| `alertmanager_web_listen_address` | 0.0.0.0:9093 | Address on which alertmanager will be listening |
| `alertmanager_web_external_url` | http://localhost:9093/ | External address on which alertmanager is available. Useful when behind reverse proxy. Ex. example.org/alertmanager |
| `alertmanager_config_dir` | /etc/alertmanager | Path to directory with alertmanager configuration |
| `alertmanager_db_dir` | /var/lib/alertmanager | Path to directory with alertmanager database |
| `alertmanager_config_file` | alertmanager.yml.j2 | Variable used to provide custom alertmanager configuration file in form of ansible template |
| `alertmanager_config_flags_extra` | {} | Additional configuration flags passed to prometheus binary at startup |
| `alertmanager_template_files` | ['alertmanager/templates/*.tmpl'] | List of folders where ansible will look for template files which will be copied to `{{ alertmanager_config_dir }}/templates/`. Files must have `*.tmpl` extension |
| `alertmanager_resolve_timeout` | 3m | Time after which an alert is declared resolved |
| `alertmanager_smtp` | {} | SMTP (email) configuration |
| `alertmanager_http_config` | {} | Http config for using custom webhooks |
| `alertmanager_slack_api_url` | "" | Slack webhook url |
| `alertmanager_pagerduty_url` | "" | Pagerduty webhook url |
| `alertmanager_opsgenie_api_key` | "" | Opsgenie webhook key |
| `alertmanager_opsgenie_api_url` | "" | Opsgenie webhook url |
| `alertmanager_victorops_api_key` | "" | VictorOps webhook key |
| `alertmanager_victorops_api_url` | "" | VictorOps webhook url |
| `alertmanager_hipchat_api_url` | "" | Hipchat webhook url |
| `alertmanager_hipchat_auth_token` | "" | Hipchat authentication token |
| `alertmanager_wechat_url` | "" | Enterprise WeChat webhook url |
| `alertmanager_wechat_secret` | "" | Enterprise WeChat secret token |
| `alertmanager_wechat_corp_id` | "" | Enterprise WeChat corporation id |
| `alertmanager_cluster` | {listen-address: ""} | HA cluster network configuration. Disabled by default. More information in [alertmanager readme](https://github.com/prometheus/alertmanager#high-availability) |
| `alertmanager_receivers` | [] | A list of notification receivers. Configuration same as in [official docs](https://prometheus.io/docs/alerting/configuration/#<receiver>) |
| `alertmanager_inhibit_rules` | [] | List of inhibition rules. Same as in [official docs](https://prometheus.io/docs/alerting/configuration/#inhibit_rule) |
| `alertmanager_route` | {} | Alert routing. More in [official docs](https://prometheus.io/docs/alerting/configuration/#<route>) |
| `alertmanager_amtool_config_file` | amtool.yml.j2 | Template for amtool config |
| `alertmanager_amtool_config_alertmanager_url` | `alertmanager_web_external_url` | URL of the alertmanager |
| `alertmanager_amtool_config_output` | extended | Extended output, use `""` for simple output. |

## Example

### Playbook

```yaml
---
  hosts: all
  roles:
    - ansible-alertmanager
  vars:
    alertmanager_version: latest
    alertmanager_slack_api_url: "http://example.com"
    alertmanager_receivers:
      - name: slack
        slack_configs:
          - send_resolved: true
            channel: '#alerts'
    alertmanager_route:
      group_by: ['alertname', 'cluster', 'service']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 3h
      receiver: slack
```

### Demo site

We provide demo site for full monitoring solution based on prometheus and grafana. Repository with code and links to running instances is [available on github](https://github.com/prometheus/demo-site) and site is hosted on [DigitalOcean](https://digitalocean.com).

## Local Testing

The preferred way of locally testing the role is to use Docker and [molecule](https://github.com/ansible-community/molecule) (v3.x). You will have to install Docker on your system. See "Get started" for a Docker package suitable to for your system. Running your tests is as simple as executing `molecule test`.

## Continuous Integration

Combining molecule and circle CI allows us to test how new PRs will behave when used with multiple ansible versions and multiple operating systems. This also allows use to create test scenarios for different role configurations. As a result we have a quite large test matrix which can take more time than local testing, so please be patient.

## Contributing

See [contributor guideline](CONTRIBUTING.md).

## Troubleshooting

See [troubleshooting](TROUBLESHOOTING.md).

## License

This project is licensed under MIT License. See [LICENSE](/LICENSE) for more details.
