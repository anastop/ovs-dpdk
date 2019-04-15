#!/bin/sh

apt install -y libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev
apt install -y libattr1 libattr1-dev libcap-dev libcap-ng-dev
apt install -y linux-image-extra-virtual

cd /opt/ovs-dpdk-lab/qemu/
./configure --target-list=x86_64-softmmu --enable-virtfs
make -j10

