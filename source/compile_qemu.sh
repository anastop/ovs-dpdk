#!/bin/sh

apt install -y libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev

cd /opt/ovs-dpdk-lab/qemu/
./configure --target-list=x86_64-softmmu --enable-virtfs
make -j10

