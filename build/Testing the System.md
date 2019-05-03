# Testing the Lab Configuration


There are two tests you can run to confirm that your network cabling is correct and that the traffic is correctly flowing in the lab.

1. **SIMPLE**:  This is a connectivity test that shows whether ARP works. If TRex can resolve the destination/gateway address on each of its ports, you know that packets are flowing because:
	1. TRex sent the ARP broadcast packet for 192.1.1.1
	2. The VPP Router received the packet through the OVS (your OVS port forwarding is working)
	3. The VPP Router parsed and responded to the request (the router is working, and you are cabled to the correct port.
	4. Finally TRex correctly received and parsed the response. (the OVS port forwarding is working both directions, and the packet wasn't malformed)
	
2. **INVASIVE**: This is only needed if the first doesn’t work and you want to verify which ports are transmitting and receiving packets.

&nbsp;

**IMPORTANT!**
> These tests should be run after a clean reboot. If you don't know the last time this host was rebooted, do so before running the test. Type `init 6` after logging into the host to reboot it.

&nbsp;

## Simple Test
As noted above, this test only confirms that the NICs are wired correctly and relies upon TRex to send an ARP for a specific IP down each of the ports. If the cables are wired correctly, the OVS will forward that ARP packet to exactly one NIC of one of the VMs. If that VM replies, and the address is resolved, your cabling is correct.  This test can help you also if you have flipped your cables around. See the note below these steps for more information.

1. Logon to the server as root.
```
ssh root@<hostname>
```

2. Run the script to start all services (DPDK, OVS, and TRex). This script will take about 2 minutes to complete, at which time the TRex Console will be displaying the status of its ARP resolution.
```
${git_base_path}/lab/start-all.sh
```

### Reviewing the Results

#### SUCCESSFUL TEST
Below is a screenshot of a successful test. All ports resolved the destination address.
![test-doc_test-simple_initial-screen_good](/images/test-doc_test-simple_initial-screen_good.png)
Your wiring is correctly setup.

#### FAILED TEST
Below is a screenshot of a failed test. Note that in this case, port [0] was unable to resolve the destination gateway IP of 192.1.1.1, which is the IP address of the first network card assigned to the Virtual Machine VPP router. All ports must successfully resolve their destination addresses for the lab to function properly.
![test-doc_test-simple_initial-screen_bad](/images/test-doc_test-simple_initial-screen_bad.png)
You have one or more problems with the system configuration, which could range from:
* Incorrect cabling (most likely)
* Incorrect BIOS settings
* Corrupt software installation
* Hardware failure (least likely)
Continue troubleshooting using the invasive test below.

&nbsp;

&nbsp;

## Invasive Test
This test you will use two SSH sessions to evaluate the status of the ports while sending/receiving traffic. This test is typically only used when TRex is unable to resolve the destination IP address on one or more of its ports. The test will show you if the ports are sending and receiving traffic properly.
* Open another SSH connection to the host (you will have two windows).
* In the second window, display the OVS port flows.
* In TRex, forcibly start the traffic flows on all ports to generate traffic.
* In TRex, launch the TRex User Interface (TUI) to check the transmitted and received packets.
* If needed, you can open a third SSH window to the host so that you can simultaneously logon to one of the VPP router VMs to view its traffic flows and errors.

1. Start another SSH terminal window, and logon to the host. Do NOT disconnect the first terminal window.
```
ssh root@<hostname>
```
2. In the second terminal window, run the following command to dump the OVS flows to the screen. This command can be cancelled at anytime by pressing `Ctrl+C`, which will return you to the Bash shell.
```
${git_base_path}/debug/dump-flows.sh
```
