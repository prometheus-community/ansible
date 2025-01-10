#!/usr/bin/env bash
#
# Description: Discover the upstream repo from each role default vars.

result=$(
  for role_dir in roles/*/ ; do
    role="$(basename "${role_dir}")"
    if [[ "${role}" == "_common" ]]; then
      echo "INFO: Skipping common role" 1>&2
      continue
    fi
    echo "INFO: ${role} Scanning: ${role_dir} " 1>&2

    role_repo=$(yq eval "._${role}_repo" "${role_dir}/vars/main.yml" 2>/dev/null)
    echo "INFO: ${role} Found role repo: ${role_repo}" 1>&2
    if [[ -z "${role_repo}" ]]; then
      echo "WARN: ${role} Unable to discover repo path" 1>&2
      continue
    fi

    yq eval "[{
      \"repo\": \"${role_repo}\",
      \"role\": \"${role}\",
      \"type\": (.${role}_binary_url | split(\"/\").[2] | split(\".\").[0] // \"github\")
    }]" "${role_dir}/defaults/main.yml" 2>/dev/null
  done | yq -o json -I=0
)

echo "result=${result}"
