# OVS-DPDK-TRex Lab System

This repository contains the code and tools to build a student lab machine. The machine will contain:
 - Ubuntu 18.04.2 ** Base OS for the host
 - DPDK 18.11.1
 - Open vSwitch 2.11.0
 - QEMU 3.1.0
 - TREX 2.56
 - And an Ubuntu 16.04 VM running VPP for routing

This repository may be cloned from: https://github.com/brianeiler/ovs-dpdk.git

---------------------


## Topology 
This configuration will produce
 - In NUMA node 0:
   - TREX configured with two active network ports

 - In NUMA node 1:
   - Open vSwitch
   - Two Linux VMs running the VPP router software with 2 active NICs each
   




## Student Lab Docs
Follow the `SST-BF Lab Guide.md` document in the `/lab` folder of this repository.




## Lab Setup and Build Docs
Follow the `Building the Lab Server.md` document in the `/build` folder of this repository.





## Caveats
The primary purpose of this lab configuration is to demonstrate the performance of specific Intel CPU features while running a synthetic network workload. Certain CPU features rely on specific CPU core IDs which may differ from host to host. The installation script attempts to identify and automatically assign the appropriate CPU cores; however you should still carefully review the configuration file as noted in the build guides.

The entire configuration of scripts relies on a global environment variable file that is copied to the lab server's /etc directory. This environment variable file contains the bit masks and CPU core assignments as well as paths to different services on the lab server. Be sure to verify the settings match your environment before running the lab.

In this lab, the TRex traffic generator is hard coded to operate on the first NUMA node (CPU 1), and the OVS and Virtual Machines are exclusively use the second NUMA node (CPU 2). This assures a separation between the load generation and the system being tested.

Currently the build script pulls one source file from a shared Dropbox location. This will be changed to a more permanent location in the future, therefore do not "fork" or copy this repository. Clone it. And then plan to periodically run `git pull` to download the most recent changes to the scripts.


No warranty is provided, but if you find bugs, let me know.
-Brian
