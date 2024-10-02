#!/usr/bin/env bash
#
# Description: Discover the upstream repo from each role default vars.

result=$(
  for role_dir in roles/*/ ; do
    role="$(basename "${role_dir}")"

    role_repo=$(yq eval "._${role}_repo" "${role_dir}/vars/main.yml" 2>/dev/null)

    yq eval "[{
      \"repo\": \"${role_repo}\",
      \"role\": \"${role}\",
      \"type\": (.${role}_binary_url | split(\"/\")[2] | split(\".\")[0] // \"github\")
    }]" "${role_dir}/defaults/main.yml" 2>/dev/null
  done | yq -o json -I=0
)

echo "result=${result}"
