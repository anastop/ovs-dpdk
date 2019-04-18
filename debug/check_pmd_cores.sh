#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

${git_base_path}/ovs/utilities/ovs-appctl dpif-netdev/pmd-rxq-show

