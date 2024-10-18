#!/usr/bin/env bash

collection_root=$(pwd | grep -oP ".+\/ansible_collections\/\w+?\/\w+")
source "$collection_root/tests/integration/molecule.sh"
