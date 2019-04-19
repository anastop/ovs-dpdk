#!/bin/bash
source /etc/0-ovs-dpdk-global-variables.sh
curl -v --upload-file $1 https://storage.googleapis.com/incoming-lab/images/$1
