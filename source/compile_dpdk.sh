#!/bin/sh

apt install -y libnuma-dev

cd /opt/ovs-dpdk-lab/dpdk
make install T=x86_64-native-linuxapp-gcc DESTDIR=install

sleep 2
cd x86_64-native-linuxapp-gcc 
make EXTRA_CFLAGS="-Ofast" -j3

