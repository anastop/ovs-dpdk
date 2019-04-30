#!/bin/bash
source /etc/0-ovs-dpdk-global-variables.sh

cd $git_base_path
git pull
cd /etc
$git_base_path/debug/send.sh 0-ovs-dpdk-global-variables.sh incoming-lab
