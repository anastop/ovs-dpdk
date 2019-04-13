apt-get install python-six autoconf automake
cd /opt/ovs-dpdk-lab/ovs
./boot.sh
./configure --with-dpdk=/opt/ovs-dpdk-lab/dpdk/x86_64-native-linuxapp-gcc CFLAGS="-Ofast" --disable-ssl
make CFLAGS="-Ofast -march=native" -j3

