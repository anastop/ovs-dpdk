#!/bin/bash

# Wake up DNS
systemd-resolve --status > /dev/null 2>&1
sleep 2

source /etc/0-ovs-dpdk-global-variables.sh

source_name=${1}
target_bucketname=${2}

target_filename=`hostname`-${1}
target_path="https://storage.googleapis.com/${target_bucketname}"

curl -v --upload-file ${source_name} ${target_path}/${target_filename}
