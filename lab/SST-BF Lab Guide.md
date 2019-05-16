# Lab Guide
This guide provides instructions that allow you to demonstrate the functionality of Intel® Speed Select Technology - Base Frequency, hereafter referred to as "Intel® SST-BF", or "SST-BF".

&nbsp;

## Lab Overview
In this lab you will use a network traffic generator and two Virtual Network Function (VNF) workloads to demonstrate the performance enhancing ability of Intel® SST-BF.

This lab must be conducted on a Cascade Lake server that has been configured per the hardware requirements section of the lab guide. If you are conducting this lab within the Intel test environment, your hardware has already been configured to meet these requirements.
The lab utilizes open source software to provide a testing platform that is extensible and generally available to the world. The software includes:
 - Ubuntu 18.04.2 ** Base OS for the host
 - DPDK 18.11.1
 - Open vSwitch 2.11.0
 - QEMU 3.1.0
 - TRex 2.56
 - Two Linux VMs running Ubuntu 16.04 and the opens source VPP router software.
 
The TRex software creates the traffic load by routing packets through the two Linux VMs. The Linux VMs are connected to the Open VSwitch (OVS) and each have dedicated 25 Gbps network cards. The dataplane of the OVS has been pinned to specific CPU cores that can be accellerated on Cascade Lake servers using Intel® SST-BF.

In this lab you will first run a workload that drives the OVS dataplane to maximum capacity without dropping packets. You will then increase the workload beyond the capabilities of the dataplane, resulting in dropped packets. At this point you will enable Intel® SST-BF on the cores assigned to the OVS data plane, which allows the virtual switch to process the increased traffic flows. You will observe the packet loss drop while the packet throughput remains unchanged.
Finally, time permitting, you may repeat this lab using different packet payload sizes. The initial test is run with a 64 byte packet to maximize the number of packets sent through the OVS dataplane. As you increase the packet payload size be sure to also decrease the rate of packets per second that are passed through the switch or you may saturate your infrastructure and invalidate your test result. Typically as packet size doubles, the rate of packets per second must be reduced by 25-50% to account for the increased volume of data flowing through the network and switch.

&nbsp;

## Lab Learning Objectives
Upon completion of this lab you should be able to:
- Explain the purpose and benefits of Intel® SST-BF
- Enable and activate Intel® SST-BF on a Linux server
- Compare the before and after performance of an OVS when using Intel® SST-BF
- Identify and evaluate workloads best suited for use with Intel® SST-BF

&nbsp;

## Duration
This exercise should take no more than 60 minutes.

&nbsp;

## Participant Prerequisites
To complete this lab successfully, you must have the proper equipment and technical experience to perform the steps. This section describes the equipment that a participant must provide in addition to the lab server hardware (defined elsewhere in this guide). 
- A laptop computer running Windows, MacOS, or Linux.
- Administrative rights to the laptop to configure an SSH tunnel to the lab datacenter.
- Wifi Network connectivity
- An SSH client. This could be the SSH client built-in to the OS, or a third party package such as PuTTY or MobaXterm.
Additionally participants should have the following technical skills:
- Familiarity with the Linux OS.
- Familiarity with networking concepts such as IP addressing and basic routing, and packet loss.
- A basic working knowledge of the Linux Bash shell to review certain script files and launch processes as directed in the lab steps.

&nbsp;

## Caveats for this Lab Exercise
- The traffic generator (TRex) will send a generic layer three packet with out any additional layer headers or overhead. The traffic is routed through the VM using the opensource VPP Router software. The packets do not contain any additional traffic layers so that we can provide a test result that can be easily reproduced on nearly any hardware without regard for special software or proprietary packet configuration.
- This lab does not rely upon the Operating System or any 3rd party software to determine the high performance cores. This determination process is done manually at the start of the lab, again to make certain that the instructions do not rely upon any proprietary software configuration or unpublished algorithms. In this lab you will have the ability to set the CPU core affinity of every process manually should you choose. In the Intel sever lab environment the high P1 cores have already been identified and flagged using environment variables that you will review at the start of the lab exercise.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

# Start of the Lab Exercise

## Exercise Tasks
- [ ] **Task 1:** Review the server configuration
- [ ] **Task 2:** Verify the impact of Intel® SST-BF on the CPU cores
- [ ] **Task 3:** Prepare the lab server for the workload test
- [ ] **Task 4:** Perform the workload test and observe the impact of Intel® SST-BF
- [ ] **Task 5:** Reset the lab server configuration
- [ ] **Task 6:** (OPTIONAL) Perform additional workload testing.

&nbsp;

&nbsp;

## Task 1: Review the server configuration
> In this task you will review the server configuration, and learn how to adjust the core speeds manually
> You will also learn how the core mappings are unique to each CPU chip
1. Check the Linux kernel version. It should be 4.20.
```
	uname -r
```
2. Check the base frequency of CPU 0 in the file System
```
	cat /sys/devices/system/cpu/cpu0/cpufreq/base_freq
```
3. Compare that to the current running frequency of CPU 0
```
	cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
```

##### That was the hard way. Let's try an easier approach!
4. Run a python script to show the core configuration
```
	cd ${git_base_path}/scripts/
	./sstbf.py
```
5. Run a command line arguments -b and -c at the CLI
```
	./sstbf.py -b
	
	./sstbf.py -c
```

6. Examine the shell script used for environment variables
```
	cat /etc/0-ovs-dpdk-global-variables.sh
```

&nbsp;

## Task 2: Verify the impact of Intel® SST-BF on the CPU cores
> In this task you will confirm the CPU affinity of the processes and verify that Intel® SST-BF increases the frequency of the correct CPU cores. 
> In our lab, all but first core on each CPU are isolated from the Linux CPU scheduler to avoid interference in our tests.
> We have also pinned the processes used in the lab to specific cores to better show the impact of Intel® SST-BF in the lab.
>  - The TRex traffic generator runs on CPU 1, and only on the low P1 cores.
>  - The VM VPP routers run on CPU 2, and also only on the low P1 cores.
>  - The OVS dataplane processes run on CPU 2 and are pinned to the High P1 cores.
> Therefore when Intel® SST-BF is activated, only the OVS dataplane is increased in performance, all other system and workload services remain on the Low P1 cores.
1. Run a shell script to show the CPU affinity and core speeds of the processes. Note that all cores show 2300MHz and are therefore equal.
```
	cd ${git_base_path}/scripts/
	./show-cores.sh
```
2. Activate Intel® SST-BF to increase the speed of the CPU cores assigned to the OVS data plane.
```
	./sstbf.py -a
```
3. Run the shell script again to show the change in the CPU core speeds of the processes. Take special note of the OVS dataplane processes running at 2700MHz.
```
	./show-cores.sh
```
4. Deactivate Intel® SST-BF so that we can perform addional comparisons.
```
	./sstbf.py -d
```

&nbsp;

## Task 3: Prepare the lab server for the workload test
> In this task you will start the services for OVS, the VMs, and the TRex traffic generator.
1. Start the OVS virtual switch process.
```
	cd ${git_base_path}/lab/
	./start-ovs.sh
```
2. Start the QEMU virtual machines.
```
	./start-qemu.sh
```
3. Start the TRex traffic generator service and set its network configuration parameters.
```
	./start-trex.sh
```

&nbsp;

## Task 4: Perform the workload test and observe the impact of Intel® SST-BF
> In this task you will launch a predefined TRex traffic generation script that streams a constant flow of 64 byte packets through the OVS to and from the VPP router VMs. You will start with a baseline configuration that maximizes the throughput of the OVS, but does not result in dropped packets. You will then load a higher demand workload that streams more traffic than the OVS can handle, resulting in packet loss. While this new workload is running, you will activate Intel® SST-BF on your server to increase the base frequency of the CPU cores assigned to the OVS dataplane. The increased CPU power allows the dataplane to handle the increase in traffic, which results in greater network throughput.
1. In the TRex Console (command line interface), load the TRex baseline traffic profiles to start the workload.
```
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-64B-base-p0.yaml --force -p0 
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-64B-base-p1.yaml --force -p1
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-64B-base-p2.yaml --force -p2
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-64B-base-p3.yaml --force -p3
```
2. Again, within the TRex Console, view the traffic results using the TRex User Interface (TUI). You may need to increase the vertical size of your terminal window for the TUI to display.
```
tui
```
3. Compare the number of transmitted packets to the number of received packets. They should be almost equal. This indicates very low or no packet loss. Record the total amount of transmitted and received packets. You will use this value in a comparison at the end of the lab.
4. Now increase the traffic load by stopping the workload and loading the high demand traffic profile. 
```
stop
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-64B-high-p0.yaml --force -p0 
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-64B-high-p1.yaml --force -p1
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-64B-high-p2.yaml --force -p2
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-64B-high-p3.yaml --force -p3
```
5. You should noticed the number of transmitted packets increasing, but the values no longer match the number of received packets. This indicates a percentage of packet loss because the OVS dataplane is running at full capacity and for this test we have configured it to drop packets that is unable to forward immediately.
6. Start another SSH terminal window, and logon to your lab server. Do NOT disconnect the first terminal window.
7. In the 2nd terminal window use the Python script to activate Intel® SST-BF on the CPUs.
```
${git_base_path}/scripts/sstbf.py -a
```
8. Return to your first terminal window (the one showing TRex). Note that the number of transmitted packets has remained the same, but we are now also receiving an equal amount of packets, which indicates that there is again low or no packet loss. Record the total amount of transmitted and received packets. 
9. Compare the values that you recorded for the total received packets (from Step 2 and Step 8). You should see approximately a 10% increase in the throughput. This increase in throughput is a result of increasing the CPU frequency of the cores assigned to the OVS dataplane, which is allowing it to process a greater volume of traffic per second.

&nbsp;

## Task 5: Reset the lab server configuration
> In this task you will stop the TRex traffic generation and then reset the Intel® SST-BF settings.
1. In the TRex User Interface (TUI), stop the current workload test, and quit the TUI. This will return you to the main TRex Console interface.
```
stop
quit
```
2. Quit the TRex Console. This will return you to the Linux shell.
```
quit
```
3. In your 2nd terminal window use the Python script to activate Intel® SST-BF on the CPUs. Then exit and close that terminal window.
```
${git_base_path}/scripts/sstbf.py -d
exit
```
4. Return to your first terminal window and run the following shell script to confirm that all the cores are operating at the base frequency, for example: 2300MHz.
```
${git_base_path}/scripts/show-cores.sh
```

&nbsp;

## Task 6: (OPTIONAL) Perform additional workload testing
> This task is optional and should only be performed if you have time remaining in the lab window.
> In this task you will use the TRex GUI to customize the traffic profiles to change the packets per second and the packet payload size, and then compare the performance with Intel® SST-BF active and inactive.

> **IMPORTANT**: At this time you must use the TRex GUI using a Linux desktop to perform the additional tests because the traffic profiles have not yet been created for the CLI-based TRex TUI.
1. In the TRex GUI, edit the profile attached to each port.
2. You may then alter the stream configuration, adjusting the packets per second and/or the packet payload size.
3. When you have configured each port as desired, start the traffic generation process and review the results in the dashboard charts.
4. You may adjust the TRex stream configuration while the test is running to achieve as close to zero packet loss as possible.
5. When you have reached the point where very few packets are being dropped, document the packets per second rate you achieved for the packet size that you selected.
6. Now in the Server CLI, activate Intel® SST-BF by running the script "/scripts/sstbf.py -a".
7. In the TRex GUI you can now begin to **SLOWLY** increase the number of packets per second. A sudden increase may cause queueing due to the burst activity and could lead to inaccurate results. Try increasing the rate by no more than 10% at a time, then wait for 5-10 seconds for the traffic to normalize before increasing or decreasing the value again.
8. Once you achieve a value that is just below the point where packet loss begins, document the current number of packets per second.
9. Compare this increased rate to your starting rate to determine how much of an impact Intel® SST-BF had on your test.
10. Finally, when you are finished, run the lab reset steps in Task 5 to prepare your lab server for future lab activities.

&nbsp;

&nbsp;

# You have completed the lab.
