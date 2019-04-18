#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh


cd ${git_base_path}/dpdk

apt install -y libnuma-dev

make install T=x86_64-native-linuxapp-gcc DESTDIR=install

sleep 2
cd x86_64-native-linuxapp-gcc 
make EXTRA_CFLAGS="-Ofast" -j3

