#!/bin/bash
source /etc/0-ovs-dpdk-global-variables.sh

source_name=${1}
target_name=`hostname`-${1}
target_path="https://storage.googleapis.com/incoming-lab"
echo
echo "source name: "${source_name}
echo "target name: "${target_name}
echo "target path: "${target_path}
echo

curl -v --upload-file ${source_name} ${target_path}/${target_name}
