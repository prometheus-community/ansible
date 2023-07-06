#!/usr/bin/env bash
#
# Description: Discover the upstream repo from each role default vars.

result=$(
  for defaults_file in roles/*/vars/main.yml ; do
    role="$(echo "${defaults_file}" | cut -f2 -d'/')"
    yq eval "[{\"repo\": ._${role}_repo, \"role\": \"${role}\"}]" "${defaults_file}"
  done | yq -o json -I=0
)

echo "result=${result}"
