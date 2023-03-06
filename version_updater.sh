#!/usr/bin/env bash

set -uo pipefail

GIT_MAIL="prometheus-team@googlegroups.com"
GIT_USER="prombot"
GIT_REPO="prometheus-community/ansible"

if [[ $# -ne 2 ]]; then
  echo "usage: $(basename "$0") <source repo> <role>"
  exit 1
fi

source_repo="$1"
role="$2"

color_red='\e[31m'
color_green='\e[32m'
color_yellow='\e[33m'
color_none='\e[0m'

echo_red() {
  echo -e "${color_red}$*${color_none}" 1>&2
}

echo_green() {
  echo -e "${color_green}$*${color_none}" 1>&2
}

echo_yellow() {
  echo -e "${color_yellow}$*${color_none}" 1>&2
}

github_api() {
  local url
  url="https://api.github.com/${1}"
  shift 1
  curl --retry 5 --silent --fail -u "${GIT_USER}:${GITHUB_TOKEN}" "${url}" "$@"
}

post_pull_request() {
  local pr_title="$1"
  local default_branch="$2"
  local branch="$3"
  local pr_msg="$4"
  local post_json
  post_json="$(printf '{"title":"%s","base":"%s","head":"%s","body":"%s"}' "${pr_title}" "${default_branch}" "${branch}" "${pr_msg}")"
  echo "Posting PR to ${default_branch}"
  github_api "repos/${GIT_REPO}/pulls" --data "${post_json}" --show-error |
    jq -r '"PR URL " + .html_url'
}

GITHUB_TOKEN="${GITHUB_TOKEN:-}"
if [[ -z "${GITHUB_TOKEN}" ]]; then
  echo_red 'GitHub token (GITHUB_TOKEN) not set. Terminating.'
  exit 128
fi

if [[ -z "${source_repo}" ]]; then
  echo_red 'No source repository set. Terminating.'
  exit 128
fi

if [[ -z "${role}" ]]; then
    echo_red 'No destination repository set. Terminating.'
    exit 128
fi

# Get latest version.
version="$(github_api "repos/${source_repo}/releases/latest" | jq '.tag_name' | tr -d '"v')"
echo_green "New ${source_repo} version is: ${version}"

# Download destination repository
if grep "_version: ${version}" "roles/${role}/defaults/main.yml"; then
    echo_green "Newest version is used."
    exit 0
fi
sed -i "s/_version:.*$/_version: ${version}/" "roles/${role}/defaults/main.yml"
sed -i -r "s/_version.*[0-9]+\.[0-9]+\.[0-9]+/_version\` | ${version}/" "roles/${role}/README.md"
yq eval -i ".argument_specs.main.options.${role}_version.default = \"${version}\"" "roles/${role}/meta/argument_specs.yml"

update_branch="autoupdate/${role}/${version}"

# Push new version
git config user.email "${GIT_MAIL}"
git config user.name "${GIT_USER}"
git checkout -b "${update_branch}"
git add \
  "roles/${role}/defaults/main.yml" \
  "roles/${role}/meta/argument_specs.yml" \
  "roles/${role}/README.md"
git commit -m 'patch: :tada: automated upstream release update'
echo_green "Pushing to ${update_branch} branch in ${role}"
if ! git push "https://${GITHUB_TOKEN}:@github.com/${GIT_REPO}" --set-upstream "${update_branch}"; then
    echo_yellow "Branch is already on remote."
    exit 0
fi

if ! post_pull_request \
  "patch: New ${source_repo} upstream release!" \
  "main" \
  "${update_branch}" \
  "The upstream [${source_repo}](https://github.com/${source_repo}/releases) released new software version - **${version}**!\n\nThis automated PR updates code to bring new version into repository." ; then
  echo_red "Pull request failed"
  exit 1
fi
echo_green "Pull Request with new version is ready"
