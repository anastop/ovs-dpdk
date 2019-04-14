# Lab Runtime
The steps in this section should be followed by the student to run the lab.

Current state assumption:
* The server has been updated to Ubuntu 18.04.2 (Kernel 4.20)
* The root account is permitted to logon via SSH
* The following software is installed: OVS, 2 VM routers, and TRex.
* The OVS, VMs, nor TRex are configured to run at boot.

## Start the OVS and VMs

1. Logon to the host as root via SSH:
```
ssh root@<hostname>
```
2. Locate the lab directory
```
cd /opt/ovs-dpdk-lab/scripts
```
3. Start the Open vSwitch
```
./step-3-start-ovs.sh
```
4. Start the Virtual Machine routers
```
./step-4-start-vms.sh
```
5. Start the TRex Server
```
./step-5-start-trex.sh
```

## Experiment with SST-BF
In this task you will open a new SSH terminal window where you will run the script to enable and disable SST-BF on your CPUs. In your TRex console window, you will see the number of packets per second increase when you activate SST-BF.

**Note:**
> Do **not** terminate your current SSH terminal.

1. In a new SSH terminal window, logon to the host as root via SSH:
```
ssh root@<hostname>
```
2. Locate the lab directory
```
cd /opt/ovs-dpdk-lab/scripts
```
3. In your TRex console window, take note of the current number of received packets per second (pps). The number should be approximately 7 Mpps (7 million packets per second).

4. Run the SST-BF python script.
```
./pbf.py
```
5. In the SST-BF utility, press the `s` key to increase the base frequency of the CPU cores assigned to the virtual network switch (OVS).

6. In your TRex console window, take note of the increased number of received packets per second (pps). The number should now be approximately 8.5 Mpps (8.5 million packets per second).

7. In the SST-BF utility, press the `t` key to return the base frequency of all the CPU cores to their original values.

8. In your TRex console window, take note of how quickly the number of received packets per second (pps) falls back to its original value.

9. You can experiment with these settings by toggling SST-BF on and off to see the change in performance.

## Cleanup

When you are finished experimenting with SST-BF, follow these steps to reset the server and close the terminal windows.

1. In the SST-BF console, press `q` to exit the script interface.

2. In the SST-BF console, type `init 6` to reboot the server. This will terminate your SSH sessions.

3. You may close both SSH windows.


# You have completed the lab exercise.
