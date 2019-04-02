# Intel Lab System

This repository contains the code and tools to build a student lab machine. The machine will contain:
 - DPDK 17.11.4
 - Open vSwitch 2.10.1
 - QEMU 2.12.1
 - TREX 2.53
 - And an Ubuntu 16.04 VM running VPP for routing

This repository may be found at: https://github.com/brianeiler/ovs-dpdk

---------------------
## Build Steps

0. Clone the Git repository to your machine:
```
cd /root
git clone https://github.com/brianeiler/ovs-dpdk
```
1. Update the Kernel and GRUB, then reboot:
```
cd /root/ovs-dpdk/scripts
./build-script-1.sh
init 6
```
2. Download the software packages and VM:
```
./build-script-2.sh
```
3. Install and compile the software packages:
```
./build-script-3.sh
```
4. Choose the configuration script for your environment. 
 - Single VM Router with 2 active ports `config-single-script-1.sh`
 - Two VM Routers and 4 active ports `config-dual-script-1.sh`

5. Power on the VPP Router VM(s):
 - Single VM Router with 2 active ports `config-single-script-2.sh`
 - Two VM Routers and 4 active ports `config-dual-script-2.sh`
