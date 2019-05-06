# Testing the Lab Configuration


There are two tests you can run to confirm that your network cabling is correct and that the traffic is correctly flowing in the lab.

* **[SIMPLE TEST:](#simple-test)** This is a connectivity test that shows whether packets are flowing and if TRex can use ARP to identify the VM router workload correctly.

* **[ADVANCED TESTS:](#advanced-tests)** These test are only needed if the first doesn’t work and you want to verify which ports are transmitting and receiving packets. 

&nbsp;

## Wiring Diagram
The test lab wiring should be configured per the diagram below. 

**Click the image to enlarge the diagram**

![test_doc-diagram-physical_cabling](/images/test_doc-diagram-physical_cabling.png)

**IMPORTANT!**
> These tests should be run after a clean reboot. If you don't know the last time this host was rebooted, do so before running the test. Type `init 6` after logging into the host to reboot it.

&nbsp;

## SIMPLE TEST
This test only confirms that the NICs are wired correctly. A failure typically indicates that you have network cabling flipped.

> If TRex can resolve the destination gateway address of each of its ports, you know that packets are flowing because:
> - [x] TRex sent the ARP broadcast packet for 192.1.1.1 (This IP is an example for port 0.)
> - [x] The VPP Router received the packet through the OVS (This indicates that your OVS port forwarding is working.)
> - [x] The VPP Router parsed and responded to the request (This indicates that the router is working, and you are cabled to the correct port.)
> - [x] Finally TRex correctly received and parsed the response. (This indicates that the OVS port forwarding is working both directions, and that the packet wasn't malformed in transit.)

**Follow these steps:**
1. Logon to the server as root.
```
ssh root@<hostname>
```

2. Run the script to start all services (DPDK, OVS, and TRex). This script will take about 2 minutes to complete, at which time the TRex Console will be displaying the status of its ARP resolution.
```
${git_base_path}/lab/start-all.sh
```
&nbsp;

### Reviewing the Results:

#### SUCCESSFUL TEST
![test_doc-simple-initial_screen-good](/images/test_doc-simple-initial_screen-good.png)

Above is a screenshot of a successful test. All ports resolved the destination address. This result indicates that your wiring is setup correctly, and that TRex should be able to send traffic properly. 

&nbsp;

#### FAILED TEST
![test_doc-simple-initial_screen-bad](/images/test_doc-simple-initial_screen-bad.png)

Above is a screenshot of a failed test. Note that in this case, port [0] was unable to resolve the destination gateway IP of 192.1.1.1, which is the IP address of the first network card assigned to the Virtual Machine VPP router. All ports must successfully resolve their destination addresses for the lab to function properly.

You have one or more problems with the system configuration, which could range from:
* Incorrect cabling (most likely)
* Incorrect BIOS settings
* Corrupt software installation
* Hardware failure (least likely)

Continue troubleshooting using the **[ADVANCED TESTS:](#advanced-tests)** below.

&nbsp;

&nbsp;

## ADVANCED TESTS
In these tests you will use two SSH sessions to evaluate the status of the ports while sending/receiving traffic. These tests are typically only used when TRex is unable to resolve the destination IP address of one or more of its ports. The test will show you if the ports are sending and receiving traffic properly.
* In TRex, forcibly start the traffic flows on all ports to generate traffic.
* In TRex, launch the TRex User Interface (TUI) to check the transmitted and received packets.
* Open another SSH connection to the host (you will have two windows).
* In the second window, display the OVS port flows.
* If needed, you can open a third SSH window to the host so that you can simultaneously logon to one of the VPP router VMs to view its traffic flows and errors.

### Task 1: Force TRex to send traffic
> In this task you will force TRex to send a stream of traffic out of ports 0-3. Per the traffic routing diagram below, you can see that the traffic forms two loops, whereby traffic leaving port 0 will return on port 1 (and vice-versa), and traffic leaving port 2 will return on port 3 (also vice-versa). 

**Click the image to enlarge the diagram**

![test_doc-diagram-routing_topology](/images/test_doc-diagram-routing_topology.png)

1. Launch the TRex console.
```
${git_base_path}/scripts/trex-console.sh
```
2. In the TRex Console (command line interface), load the TRex baseline traffic profiles to start the workload.
```
portattr -a --prom on
service -a
l3 -p 0 --src 192.1.1.2 --dst 192.1.1.1
l3 -p 1 --src 192.2.1.2 --dst 192.2.1.1
l3 -p 2 --src 192.3.1.2 --dst 192.3.1.1
l3 -p 3 --src 192.4.1.2 --dst 192.4.1.1
service -a --off
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-64B-base-p0.yaml --force -p0 
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-64B-base-p1.yaml --force -p1
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-64B-base-p2.yaml --force -p2
start -f /opt/ovs-dpdk-lab/configs/trex/vpp-64B-base-p3.yaml --force -p3
```
3. Again, within the TRex Console, view the traffic results using the TRex User Interface (TUI). You may need to increase the vertical size of your terminal window for the TUI to display.
```
tui
```
4. If traffic is working properly, all four ports (0-3) should be transmitting and receiving approximately the same number of packets. Due to the routing topology, a more accurate comparison is to match the Transmitted Packets of Port 0 to the Received Packets of Port 1.

**Now What?**
> If the transmitted and received packets do not match, proceed with the next task.


#### FAILURE Example: TRex transmits packets on all four ports (0-3), but no packets are received.

![test_doc-advanced-trex_tui_active-bad](/images/test_doc-advanced-trex_tui_active-bad.png)


#### SUCCESS Example: TRex transmits packets on all four ports (0-3) and a nearly equal number of packets are received.

![test_doc-advanced-trex_tui_active-good](/images/test_doc-advanced-trex_tui_active-good.png)



&nbsp;

### Task 2: Check the OVS Flows for activity

1. Start another SSH terminal window, and logon to the host. Do NOT disconnect the first terminal window.
```
ssh root@<hostname>
```
2. In the second terminal window, run the following command to dump the OVS flows to the screen. This command can be cancelled at anytime by pressing `Ctrl+C`, which will return you to the Bash shell.
```
${git_base_path}/debug/dump-flows.sh
```
The dump-flows command shows the "flows" or packet processing rules within the OVS. Unlike a traditional switch that either forwards or floods traffic based only upon a Forwarding Information Base (FIB), the OVS relies upon these flow rules to determine how to forward the traffic it receives.  If traffic matches a flow, the OVS performs the action listed in the flow; typically forwarding the packet to another port. In this configuration, the flows have only rules to push traffic from one port to another without regard for the type of packet received. For example, a packet received on port 1 will always be forwarded out of port 5. 

This command also shows how many seconds have elapses since the OVS received a packet that matched a particular flow, indicated by the "idle_age" value. 0 indicates that the flow is currently active. 
Refer to the image below for the OVS configuration and flow diagram.

**Click the image to enlarge the diagram**

![test_doc-diagram-ovs_flows](/images/test_doc-diagram-ovs_flows.png)

#### FAILURE Example: TRex packets arrive at the OVS, but VM Routers do not reply
![test_doc-advanced-ovs_dump_flows-bad](/images/test_doc-advanced-ovs_dump_flows-bad.png)

In this image, the physical NICs attached to the OVS are receiving the traffic from TRex, and the OVS has forwarded the traffic to the VMs' switch ports, but the VMs are not responding. 

You can determine this because:
* The first four lines, "in_port=1" through "in_port=4" are bound to the physical DPDK NICs in the OVS configuration.
* The next four lines, "in_port=5" through "in_port=8" are bound to the virtual NICs of the VM routers. In our configuration, VPP-VM1 is connected to ports 5 and 6, whereas VPP-VM2 is connected to ports 7 and 8.
* Also remember that the OVS only has 8 flows, and these flows strictly bind together the following ports 1:5, 2:6, 3:7, and 4:8. Traffic may flow bidirectionally between those ports, but to nowhere else. For example: traffic from port 1 will not be forwarded to any other port than port 5.
* Each of the physical DPDK NIC ports (1-4) show that traffic is coming in from TRex.
  * You see a steadily increasing value for "n_packets", indicating that the OVS has processed traffic matching this flow in the past
  * The flows also show a value of zero for "idle_age", which means the OVS is actively processing traffic that matches those flows.
* The opposite is true for the ports assigned to the VPP-VMs (5-8). The VMs are not sending any responses to the OVS (and therefore back to TRex).
  * The "n_packets=0" value is zero, indicating that no traffic has matched this flow since the OVS was last reset.
  * The "idle_age" is steadily increasing, meaning that the flow is currently inactive.
* This result is typical when the OVS is dropping the transmitted frames from the VMs, and may be caused by a shortage or lack of 2MB huge memory pages.





#### SUCCESS Example: Packets flowing properly
![test_doc-advanced-ovs_dump_flows-good](/images/test_doc-advanced-ovs_dump_flows-good.png)

In this image, all the flows are processing traffic, and the flows are nearly equal, meaning that the number of packets received by the VMs equals the number they return to TRex.


&nbsp;

### Task 3: Verify the result by checking the OVS Port counters

1. In the SSH terminal currently showing the dump-flows command, press `Ctrl+C` to abort the command and return to the Bash shell.

2. In that same terminal window, run the following command to display the individual OVS ports and their statistics counters.
```
${git_base_path}/debug/dump-ports.sh
```
Note that the dump-ports command does not display the ports in numerical order; this is normal and does *NOT* indicate a problem. 

Much like the port statistics on a physical switch, the dump-ports command shows a number of important statistics separated onto two lines: "rx" and "tx" for Receive (rx) and Transmit (tx). We will focus on the following fields:
* "**pkts**" is the total number of packets transmitted (or received)
* "**bytes**" is the total number of bytes transmitted (or received)
* "**drop**" is the total number of packets dropped while attempting to transmit (or receive)
* "**errs**" is the total number of errors encountered while attempting to transmit (or receive)

#### FAILURE Example: TRex packets arrive at the OVS, but VM Routers do not reply
![test_doc-advanced-ovs_dump_ports-bad](/images/test_doc-advanced-ovs_dump_ports-bad.png)

In this image we can see why the VM routers packets were not received by TRex. The OVS switch is dropping the frames.



#### SUCCESSFUL Example: Packets flowing properly
![test_doc-advanced-ovs_dump_ports-good](/images/test_doc-advanced-ovs_dump_ports-good.png)

This is an example of all packets flowing properly.


&nbsp;

&nbsp;

&nbsp;

# Understanding the Results

If TRex shows a port transmitting packets, the corresponding port in OVS should also show received. Thus, if TRex Port 2 is transmitting, OVS should show received packets on Port 3, which OVS will then transmit on Port 7 to the VM (VPP-VM2).

If the VPP-VM2 is functioning, packets transmitted to the VM on OVS port 7 will be received within the VM on its interface "Gig0/4/0", whereby VPP will then parse and route the packet to its interace Gig0/5/0, which is connected to OVS port 8. This will cause the OVS to show packets received on OVS port 8, and then transmitted on OVS port 4 (to TRex Port 3).

**Example: If TRex is transmitting only on Port 0, you should see the following:**
* TRex Console shows Transmitted packets on Port 0
* TRex Console shows Received packets on Port 1
* The OVS "dump-flows" command shows activity on OVS Ports 1 and 6 (attached to DPDK0 - and VPP-VM1 Gig0/6/0)
* The OVS "dump-ports" command shows finer details:
  * OVS Port 1 shows Received Packets increasing (picking packets up off the physical NIC cabled to TRex Port 0)
  * OVS Port 5 shows Transmitted Packets increasing (forwarding packets to the VPP-VM1:Gig0/5/0)
  * OVS Port 6 shows Received Packets increasing (after being routed by the VPP router to Gig0/6/0)
  * OVS Port 2 shows Transmitted packets increasing (sending the packets to the physical NIC cabled to TRex Port 1)




















