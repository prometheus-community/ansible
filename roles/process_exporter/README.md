# Ansible Role: process_exporter

## Description

Deploy [process-exporter](https://github.com/ncabatoff/process-exporter) using ansible.

Note. This repository and role uses the name process_exporter to conform with ansible galaxy constraints.

## Requirements

- Ansible >= 2.9 (It might work on previous versions, but we cannot guarantee it)

## Role Variables

All variables which can be overridden are stored in [meta/argument_specs.yml](meta/argument_specs.yml) file.
See the [prometheus.prometheus.process_exporter](https://prometheus-community.github.io/ansible/branch/main/process_exporter_role.html) docs.

## Example

### Playbook

Use it in a playbook as follows:
```yaml
- hosts: all
  roles:
    - prometheus.prometheus.process_exporter
```
