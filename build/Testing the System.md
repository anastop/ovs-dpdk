# Testing the lab configuration


There are two tests you can run.
1. Simple:  This is a connectivity test that shows whether ARP works. If TRex can resolve the destination/gateway address on each of its ports, you know that packets are flowing because ARP worked.

2) Invasive: This is only needed if the first doesn’t work and you want to verify which  and a more through test that pushes traffic regardless of ARP resolution so that you can check the ports for packet flow.  If the simple test works, you do NOT need to run the invasive test.
To test a server after it has been built, follow these steps:


1. Logon to the server as root.

2. 