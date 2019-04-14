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
/opt/ovs-dpdk-lab/scripts/build-script-1.sh
init 6
```
2. Download the software packages and VM:
```
/opt/ovs-dpdk-lab/scripts/build-script-2.sh
```
3. Install and compile the software packages:
```
/opt/ovs-dpdk-lab/scripts/build-script-3.sh
```

## Configuration Steps: Single VM
This configuration will produce
 - In NUMA node 0:
   - TREX configured with two active network ports
   - Grafana and the webserver
 - In NUMA node 1:
   - Open vSwitch
   - One Linux VM running the VPP router software with 2 active NICs
   
1. Configure the vSwitch by running the script: `/opt/ovs-dpdk-lab/scripts/config-single-script-1.sh`

2. Power on the VM by running the script: `/opt/ovs-dpdk-lab/scripts/config-single-script-2.sh`

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
cd /opt/ovs-dpdk-lab/scripts
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
cd /opt/ovs-dpdk-lab/trex
./trex-console -f
```

6. At the TRex command prompt, start the test:
```
portattr
portattr -a --prom on
service -a
l3 -p 0 --src 192.1.1.2 --dst 192.1.1.1
l3 -p 1 --src 192.2.1.2 --dst 192.2.1.1
l3 -p 2 --src 192.3.1.2 --dst 192.3.1.1
l3 -p 3 --src 192.4.1.2 --dst 192.4.1.1
service -a --off
tui
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-vrouter-p0.yaml --force -p0
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-vrouter-p1.yaml --force -p1
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-vrouter-p2.yaml --force -p2
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-vrouter-p3.yaml --force -p3

stats -a
```


## View the results

















