#!/usr/bin/env bash
#
# Description: Lint the defaults/main.yml against the meta/arguments_spec.yml

lint_diff() {
  diff -u \
    <(yq 'keys | .[]' "${role}/defaults/main.yml" | sort -u) \
    <(yq '.argument_specs.main.options | keys | .[] ' "${role}/meta/argument_specs.yml" | sort -u)
  return $?
}

error=0

for role in roles/* ; do
  echo "Checking ${role}"
  if ! lint_diff ; then
    echo "ERROR: ${role}: meta/argument_specs.yml doesn't match defaults/main.yml"
    error=1
  fi
done

exit "${error}"
