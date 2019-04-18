# OVS-DPDK-TRex Lab System

This repository contains the code and tools to build a student lab machine. The machine will contain:
 - Ubuntu 18.04.2 ** Base OS for the host
 - DPDK 18.11.1
 - Open vSwitch 2.11.0
 - QEMU 3.1.0
 - TREX 2.53
 - And an Ubuntu 16.04 VM running VPP for routing

This repository may be found at: https://github.com/brianeiler/ovs-dpdk

---------------------


## Topology 
This configuration will produce
 - In NUMA node 0:
   - TREX configured with two active network ports

 - In NUMA node 1:
   - Open vSwitch
   - Two Linux VMs running the VPP router software with 2 active NICs each
   




## Student Lab Docs
Follow the numbered guide documents in the `/lab-docs` folder of this repository.




## Lab Setup and Build Docs
Follow the numbered guide documents in the `/build-docs` folder of this repository.





## Caveats
The primary purpose of this lab configuration is to demonstrate the performance of specific Intel CPU features while running a synthetic network workload. Certain CPU features rely on specific CPU core IDs which may differ from host to host. Therefore the initial configuration of this setup requires you to edit a global environment variable file and upload it to your /etc directory on the lab server. This environment variable file contains a sample bit mask for the special cores, and is meant for you to manually edit the values to match your system and the desired CPU core affinity of the services.

In this lab, the TRex traffic generator is hard coded to operate on the first NUMA node (CPU 1), and the OVS and Virtual Machines are exclusively use the second NUMA node (CPU 2). This assures a separation between the load generation and the system being tested.

Currently the scripts pull two source files from a shared Dropbox location. Soon these links will be changed to permanent public source areas, therefore do not copy this repository. Clone it. And then plan to periodically run `git pull` to get the most recent changes to the scripts.


