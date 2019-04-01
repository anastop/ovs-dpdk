Steps to run VPP vRouter over OVS-DPDK:


1. Upgrade the kernel to 4.20+
	/root/ovs-dpdk/kernel-upgrade.sh

2. Unpack the VM Image file
	cd /root/ovs-dpdk/vm-images
	tar -xzf ubuntu-16.04-testpmd.img.tgz ubuntu-16.04-testpmd.img

3. Update GRUB Boot Loader
	cp -f /root/ovs-dpdk/grub /etc/default/grub
	update-grub

4. Reboot the machine, then logon again as root
	init 6
	
5. Compile and install DPDK, OVS, and QEMU KVM
	cd /root/ovs-dpdk
	./setup_ovs.sh
	
6. Shutdown extraneous services
	cd /root/ovs-dpdk
	./disable_service.sh
	./stop_services.sh

7. Run the configuration scripts
	cd /root/ovs-dpdk/scripts
	./start-ovs-dpdk.sh
	./set_pmd_thread.sh
	./createports_pvp-4P-4c.sh
	./addroutes_pvp-4P.sh

8. Power on the VM
	./power_on_vm_vhost-user-4P.sh

9. SSH into the VM via your host machine with this command:
	ssh -l root localhost -p 2023
	username: root
	password: passme123

10. Inside of the VM, Check the following:	
	a. Check the cat /proc/cmdline to ensure the isolcpus on the isolated cores is correct.
		For 4 vCPU, isolate core 1 - 3
		For 6 vCPU, isolate core 1 - 5
		For 8 vCPU, isolate core 1 - 7
		For 10 vCPU, isolate core 1 - 9

	b. Make changes to the grub command line to isolate the correct cores. The reboot the VM.

	c. In the VM, run the following tuning scripts:
		./disable_service.sh
		./stop_services.sh

	d. Edit and save /etc/vpp/startup.conf to include the correct PCI ID devices to configure in the VPP, the number of worker threads, core list and main core.

main-core 1
corelist-workers 2-3  (for 2 worker threads)
workers 2
## Whitelist specific interface by specifying PCI address
dev 0000:00:04.0
dev 0000:00:05.0


Go to the /root/vpp-vrouter folder in the VM to create your port configuration in VPP.
cd /root/vpp-vrouter
vpp-2p.conf is the 2 port configuration for VPP Router setup.
You can refer to vpp-2p.conf to create 4-port, 6-port, and 8-port configuration.

Once all has been edited, start vpp:
systemctl start vpp

systemctl status vpp  (to check status of VPP)

from the host, access to VPP:
telnet localhost 5002

Trying ::1...
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
    _______    _        _   _____  ___ 
 __/ __/ _ \  (_)__    | | / / _ \/ _ \
 _/ _// // / / / _ \   | |/ / ___/ ___/
 /_/ /____(_)_/\___/   |___/_/  /_/    

vpp# show interface 
vpp# exec /root/vpp-vrouter/vpp-2p.conf    (to configure router with 2 interfaces)
vpp# show interface		            (you should see all the interfaces are up)
vpp# show ip arp     (IXIA would learn the IP and this would output the IP address of the IXIA ports)
vpp# show thread     (show the number of worker thread)
vpp# show interface rx-placement       (show whether each port is on separate worker thread)

VPP is ready.

Back on the host, do the CPU pinning on the VPP VM. Follow the steps documented in ovs-dpdk VM CPU pinning.

On the IXIA, there will be protocol interface and static to be enabled. You will learn the ARP on the porotocl interface.

Use the attached IXIA config as your reference.

