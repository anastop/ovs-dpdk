#!/bin/sh

#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh


cd ${git_base_path}/ovs

apt install -y autoconf automake libtool
apt install -y python-six

./boot.sh
./configure --with-dpdk=${DPDK_DIR}/x86_64-native-linuxapp-gcc CFLAGS="-Ofast" --disable-ssl
make CFLAGS="-Ofast -march=native" -j3

