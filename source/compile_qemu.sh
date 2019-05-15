#!/bin/bash

# Wake up DNS
systemd-resolve --status > /dev/null 2>&1
sleep 2

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

apt install -y libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev
apt install -y libattr1 libattr1-dev libcap-dev libcap-ng-dev
apt install -y linux-image-extra-virtual

cd ${git_base_path}/qemu/
./configure --target-list=x86_64-softmmu --enable-virtfs
make -j10

