#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

${git_base_path}/debug/pbf.py -s

echo
echo "SST-BF is ACTIVE."
echo
