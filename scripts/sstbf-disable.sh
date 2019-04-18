#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

cd ${git_base_path}/debug
./clx_baseline.sh

echo
echo "SST-BF is DISABLED. Processors are back to their defaults."
echo
