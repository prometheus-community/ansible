===================================
Prometheus.Prometheus Release Notes
===================================

.. contents:: Topics


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
