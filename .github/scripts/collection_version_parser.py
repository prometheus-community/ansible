#!/usr/bin/env python3

"""
This module provides functions for parsing PEP 440 compliant
version ranges in Ansible collections.
"""

import yaml
from packaging.version import Version
from packaging.specifiers import SpecifierSet


def increment_version(version):
    """
    Increment the minor version of the provided version and return the result.

    :param version: The version to increment
    :type version: packaging.version.Version
    :return: The incremented version
    :rtype: packaging.version.Version
    """
    major, minor, _ = version.release
    return Version(f"{major}.{minor+1}.0")


def parse_pep440_range(range_str):
    """
    Parse the range_str into individual versions and return a list of versions
    in the range formatted with "stable-" prefix.

    :param range_str: The version range string
    :type range_str: str
    :return: List of formatted version strings
    :rtype: list
    """
    specifier_set = SpecifierSet(range_str)

    start_str, end_str = [s.strip() for s in range_str.split(",")]
    start_version = Version(start_str.strip(">= >"))
    end_version = Version(end_str.strip("<= <"))

    if ">=" in start_str:
        current_version = start_version
    else:
        current_version = increment_version(start_version)

    versions = []

    while (current_version < end_version or
           (current_version == end_version and "<=" in end_str)):
        if current_version in specifier_set:
            if (current_version < end_version or
               ("<=" in end_str and current_version == end_version)):
                version_string = (
                    f"stable-{current_version.major}.{current_version.minor}"
                )
                versions.append(version_string)
        current_version = increment_version(current_version)

    return versions


def get_requires_ansible(yaml_file_path):
    """
    Get the 'requires_ansible' property from a YAML file.

    :param yaml_file_path: The path to the YAML file
    :type yaml_file_path: str
    :return: The value of the 'requires_ansible' property
    :rtype: str
    """
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)
        return yaml_data.get('requires_ansible')


if __name__ == "__main__":
    requires_ansible = get_requires_ansible("meta/runtime.yml")
    if requires_ansible:
        stable_versions = parse_pep440_range(requires_ansible)
        print(stable_versions)
    else:
        print("Requires_ansible not found in the YAML file.")
