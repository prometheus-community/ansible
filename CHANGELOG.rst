===================================
Prometheus.Prometheus Release Notes
===================================

.. contents:: Topics


v0.9.0
======

Minor Changes
-------------

- enhancement: allows using multiple web listen addresses (https://github.com/prometheus-community/ansible/pull/213)
- feat(blackbox_exporter): Create config directory (https://github.com/prometheus-community/ansible/pull/250)

v0.8.1
======

v0.8.0
======

Minor Changes
-------------

- feat: add smartctl_exporter role (https://github.com/prometheus-community/ansible/pull/229)

Bugfixes
--------

- fix(molecule): don't contact galaxy api since requirements come from git (https://github.com/prometheus-community/ansible/pull/241)

v0.7.1
======

Bugfixes
--------

- fix(molecule): don't contact galaxy api since requirements come from git (https://github.com/prometheus-community/ansible/pull/241)

v0.7.0
======

Minor Changes
-------------

- feat(prometheus): Add shutdown timeout variable (https://github.com/prometheus-community/ansible/pull/220)
- feat(systemd_exporter): Add TLS configuration (https://github.com/prometheus-community/ansible/pull/205)
- feat(systemd_exporter): Add logging configuration to systemd_exporter (https://github.com/prometheus-community/ansible/pull/210)

Bugfixes
--------

- fix(systemd_exporter): Fix collector flags for older versions (https://github.com/prometheus-community/ansible/pull/208)
- fix: blackbox_exporter ansible-lint risky-octal (https://github.com/prometheus-community/ansible/pull/174)

v0.6.1
======

Bugfixes
--------

- fix(systemd_exporter): Fix collector flags for older versions (https://github.com/prometheus-community/ansible/pull/208)
- fix: blackbox_exporter ansible-lint risky-octal (https://github.com/prometheus-community/ansible/pull/174)

v0.6.0
======

Minor Changes
-------------

- feat: Add chrony_exporter role (https://github.com/prometheus-community/ansible/pull/159)
- feat: Add pushgateway role (https://github.com/prometheus-community/ansible/pull/127)
- feat: Add role smokeping_prober (https://github.com/prometheus-community/ansible/pull/128)
- feature: Agent mode support (https://github.com/prometheus-community/ansible/pull/198)
- feature: Make config installation dir configurable (https://github.com/prometheus-community/ansible/pull/173)
- feature: blackbox exporter user/group configurable (https://github.com/prometheus-community/ansible/pull/172)
- minor: support fedora 38 (https://github.com/prometheus-community/ansible/pull/202)

Removed Features (previously deprecated)
----------------------------------------

- removed: Drop fedora 36 support as it is EOL (https://github.com/prometheus-community/ansible/pull/200)
- removed: Drop ubuntu 18.04 support as it is EOL (https://github.com/prometheus-community/ansible/pull/199)

Bugfixes
--------

- fix(alertmanager): add routes before match_re (https://github.com/prometheus-community/ansible/pull/194)
- fix(node_exporter): Fix ProtectHome for textfiles (https://github.com/prometheus-community/ansible/pull/184)
- fix: Add test for argument_specs matching (https://github.com/prometheus-community/ansible/pull/177)
- fix: Make binary installs consistent (https://github.com/prometheus-community/ansible/pull/204)
- fix: mysqld_exporter should actually respect the mysqld_exporter_host variable (https://github.com/prometheus-community/ansible/pull/88)

v0.5.2
======

Bugfixes
--------

- fix: mysqld_exporter should actually respect the mysqld_exporter_host variable (https://github.com/prometheus-community/ansible/pull/88)

v0.5.1
======

Bugfixes
--------

- fix: Checkout full branch for version updates (https://github.com/prometheus-community/ansible/pull/108)
- fix: Install package fact dependencies needs to be run as root (https://github.com/prometheus-community/ansible/pull/89)
- fix: always create config file (https://github.com/prometheus-community/ansible/pull/113)
- fix: don't require role name on internal vars (https://github.com/prometheus-community/ansible/pull/109)
- fix: textfile collector dir by setting recurse to false (https://github.com/prometheus-community/ansible/pull/105)

v0.5.0
======

Minor Changes
-------------

- minor: Add ansible 2.15 support (https://github.com/prometheus-community/ansible/pull/106)

Bugfixes
--------

- fix: add "become: true" to snmp_exporter handlers (https://github.com/prometheus-community/ansible/pull/99)
- fix: node_exporter - Fix Systemd ProtectHome option in service unit (https://github.com/prometheus-community/ansible/pull/94)
- fix: pass token to github api for higher ratelimit (https://github.com/prometheus-community/ansible/pull/91)
- fix: replace eol platforms with current (https://github.com/prometheus-community/ansible/pull/53)
- fix: tags support for included tasks (https://github.com/prometheus-community/ansible/pull/87)

v0.4.1
======

Bugfixes
--------

- fix: add "become: true" to snmp_exporter handlers (https://github.com/prometheus-community/ansible/pull/99)
- fix: pass token to github api for higher ratelimit (https://github.com/prometheus-community/ansible/pull/91)
- fix: replace eol platforms with current (https://github.com/prometheus-community/ansible/pull/53)
- fix: tags support for included tasks (https://github.com/prometheus-community/ansible/pull/87)

v0.4.0
======

Minor Changes
-------------

- enhancement: add `skip_install` variables to various roles (https://github.com/prometheus-community/ansible/pull/74)
- enhancement: support ansible-vaulted basic auth passwords (https://github.com/prometheus-community/ansible/pull/83)

Bugfixes
--------

- fix: meta-runtime now needs minor in version string (https://github.com/prometheus-community/ansible/pull/84)

v0.3.1
======

Bugfixes
--------

- fix: Don't log config deployments (https://github.com/prometheus-community/ansible/pull/73)
- fix: correct quotation of flags in systemd config file (https://github.com/prometheus-community/ansible/pull/71)
- fix: version bumper action (https://github.com/prometheus-community/ansible/pull/75)

v0.3.0
======

Minor Changes
-------------

- feat: Add mysqld_exporter role (https://github.com/prometheus-community/ansible/pull/45)

Bugfixes
--------

- fix: policycoreutils python package name (https://github.com/prometheus-community/ansible/pull/63)

v0.2.1
======

Bugfixes
--------

- fix: policycoreutils python package name (https://github.com/prometheus-community/ansible/pull/63)

v0.2.0
======

Minor Changes
-------------

- feat: add systemd exporter role (https://github.com/prometheus-community/ansible/pull/62)

Removed Features (previously deprecated)
----------------------------------------

- removed: community.crypto is only needed when testing (https://github.com/prometheus-community/ansible/pull/56)

Bugfixes
--------

- fix: Fix typo on Install selinux python packages for RedHat family (https://github.com/prometheus-community/ansible/pull/57)

v0.1.5
======

Bugfixes
--------

- fix: follow PEP 440 standard for supported ansible versions (https://github.com/prometheus-community/ansible/pull/46)
- fix: various role argument specs (https://github.com/prometheus-community/ansible/pull/50)

v0.1.4
======

v0.1.3
======

v0.1.2
======

v0.1.1
======

v0.1.0
======

Minor Changes
-------------

- feat: Allow grabbing binaries and checksums from a custom url/mirror (https://github.com/prometheus-community/ansible/pull/28)

Removed Features (previously deprecated)
----------------------------------------

- removed: remove lint from molecule to avoid repetition (https://github.com/prometheus-community/ansible/pull/35)

Bugfixes
--------

- fix: Force push git changelogs (https://github.com/prometheus-community/ansible/pull/36)
- fix: Remove unnecessary dependency on jmespath (https://github.com/prometheus-community/ansible/pull/22)
- fix: ansible 2.9 workaround for galaxy install from git (https://github.com/prometheus-community/ansible/pull/37)
- fix: avoid installing changelog tools when testing (https://github.com/prometheus-community/ansible/pull/34)
- fix: grab dependencies from github to avoid galaxy timeouts (https://github.com/prometheus-community/ansible/pull/33)

v0.0.3
======

v0.0.1
======

Major Changes
-------------

- Initial Release
