# Troubleshooting

## Bad requests (HTTP 400)

This role downloads checksums from the Github project to verify the integrity of artifacts installed on your servers. When downloading the checksums, a "bad request" error might occur.

This happens in environments which (knowningly or unknowling) use the [netrc mechanism](https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html) to auto-login into servers.

Unless netrc is needed by your playbook and ansible roles, please unset the var like so:

```
$ NETRC= ansible-playbook ...
```

Or:

```
$ export NETRC=
$ ansible-playbook ...
```

## node_exporter doesn't report data from textfile collector

There are 3 potential issues why node_exporter doesn't pick up data:

1. Duplicated metrics across multiple files.
2. File is not readable by node_exporter process.
3. Textfile collector is not enabled.

Solving first possibility is out of scope of the role as data is created somewhere else. When creating that data ensure
files are readable by `node-exp` user. To get access to the directory with files your process needs to be in `node-exp`
group.

Lastly ansible role misconfiguration can also lead to data not being picked up. Check if `node_exporter` textfile
collector is enabled in `node_exporter_enabled_collectors` as follows:

```yaml
node_exporter_enabled_collectors:
  - textfile:
      directory: "{{ node_exporter_textfile_dir }}"
```

__note___: `node_exporter_textfile_dir` variable is only responsible for creating a directory not enabling a collector.
