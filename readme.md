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
/root/ovs-dpdk/scripts/build-script-1.sh
init 6
```
2. Download the software packages and VM:
```
/root/ovs-dpdk/scripts/build-script-2.sh
```
3. Install and compile the software packages:
```
/root/ovs-dpdk/scripts/build-script-3.sh
```

## Configuration Steps: Single VM
This configuration will produce
 - In NUMA node 0:
   - TREX configured with two active network ports
   - Grafana and the webserver
 - In NUMA node 1:
   - Open vSwitch
   - One Linux VM running the VPP router software with 2 active NICs
   
1. Configure the vSwitch by running the script: `/root/ovs-dpdk/scripts/config-single-script-1.sh`

2. Power on the VM by running the script: `/root/ovs-dpdk/scripts/config-single-script-2.sh`

3. Logon to the VPP VM:
```
ssh root@localhost -p 2023
username: root
password: root245
```

4. Inside the VPP VM, run the following commands to start the VPP router:
```
./disable_service.sh
./stop_services.sh
./setup_huge.sh

Copy the files from vpp folder. Startup config and the profile.

systemctl enable vpp.service
systemctl start vpp
telnet localhost 5002
```

5. The telnet command attaches you to the VPP router. Run the following command to configure the router:
```
exec /root/vpp-vrouter/vpp-vm1-2ports.conf
quit
```
6. Logout of the VPP-VM, and return to your test server.
```
exit
```


## Load Generator Setup:
This will launch the TRex Load Generator.

1. Start a new tmux session and launch the TRex server
```
apt-get install -y tmux
tmux new -s trex-server
```

2. In the tmux session, launch the TRex server:
```
cd /root/ovs-dpdk/scripts
./trex_server_2ports.sh
```

3. After TRex loads, disconnect from the tmux session:
```
Press <CTRL-B>, then press d
```

4.  Start another tmux session for the TRex console interface:
```
tmux new -s trex-console
```

5. In the tmux session, launch the TRex console:
```
cd /root/ovs-dpdk/trex
./trex-console -f
```

6. At the TRex command prompt, start the test:
```
start -f /root/ovs-dpdk/configs/vpp-vrouter-p0.yaml --force -p0
start -f /root/ovs-dpdk/configs/vpp-vrouter-p1.yaml --force -p1
stats -a
```


## View the results

















