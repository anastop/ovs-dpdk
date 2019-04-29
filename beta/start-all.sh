#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh


${git_base_path}/scripts/step-3-start-ovs.sh
${git_base_path}/scripts/step-4-start-vms.sh
${git_base_path}/beta/step-5-start-trex.sh

