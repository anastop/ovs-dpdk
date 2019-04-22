#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh
#
# WARNING!!!
# Each VM that will run VPP must have a unique "vm_uuid" value.
# The VM queries this value to determine which configuration script to execute at boot.
# The VMs are otherwise unable to uniquely identify themselves.
#

fs_path=${git_base_path}/configs/vpp
fs_mount_tag=hostfs
vm_disk=${git_base_path}/vm-images/ubuntu-16.04-vpp-1.img
vm_name=VPP-VM1
vm_uuid=00000000-0000-0000-0000-000000000001
vm_ssh=2023
vm_vnc=1

vm_nic_1_id=char1
vm_nic_1_hostpath=/usr/local/var/run/openvswitch/vhost-client-0
vm_nic_1_net=net1
vm_nic_1_mac=00:01:00:00:00:01

vm_nic_2_id=char2
vm_nic_2_hostpath=/usr/local/var/run/openvswitch/vhost-client-1
vm_nic_2_net=net2
vm_nic_2_mac=00:02:00:00:00:02

echo
echo "Powering on ${vm_name}..."
if [ ! -f ${vm_disk} ];
then
	echo
	echo "File: ${vm_disk} not found."
	echo "You must first run the build script to download the VM disk files."
else
#	-virtfs local,path=${fs_path},mount_tag=${fs_mount_tag},security_model=none,readonly \

taskset -c ${cpu_vm1_core0},${cpu_vm1_core1},${cpu_vm1_core2},${cpu_vm1_core3} ${git_base_path}/qemu/x86_64-softmmu/qemu-system-x86_64 \
	-m 8G -smp 4,cores=4,threads=1,sockets=1 -cpu host \
	-drive format=raw,file=${vm_disk} \
	-boot c \
	-enable-kvm \
	-name ${vm_name},debug-threads=on \
	-uuid ${vm_uuid} \
	-object memory-backend-file,id=mem,size=8G,mem-path=/dev/hugepages,share=on \
	-numa node,memdev=mem -mem-prealloc \
	-netdev user,id=nttsip,hostfwd=tcp::${vm_ssh}-:22 \
	-device e1000,netdev=nttsip \
	-chardev socket,id=${vm_nic_1_id},path=${vm_nic_1_hostpath},server \
	-netdev type=vhost-user,id=${vm_nic_1_net},chardev=${vm_nic_1_id},vhostforce \
	-device virtio-net-pci,netdev=${vm_nic_1_net},mac=${vm_nic_1_mac},csum=off,gso=off,guest_tso4=off,guest_tso6=off,guest_ecn=off,mrg_rxbuf=off \
	-chardev socket,id=${vm_nic_2_id},path=${vm_nic_2_hostpath},server \
	-netdev type=vhost-user,id=${vm_nic_2_net},chardev=${vm_nic_2_id},vhostforce \
	-device virtio-net-pci,netdev=${vm_nic_2_net},mac=${vm_nic_2_mac},csum=off,gso=off,guest_tso4=off,guest_tso6=off,guest_ecn=off,mrg_rxbuf=off \
	-vnc :${vm_vnc} &
echo
echo "${vm_name} started!"
echo "VNC: ${vm_vnc}"
echo "ssh root@localhost -p ${vm_ssh}"
echo "username: root"
echo "password: root245"
fi

echo
echo
echo
echo
echo
echo
echo

fs_path=${git_base_path}/configs/vpp
fs_mount_tag=hostfs
vm_disk=${git_base_path}/vm-images/ubuntu-16.04-vpp-2.img
vm_name=VPP-VM2
vm_uuid=00000000-0000-0000-0000-000000000002
vm_ssh=2024
vm_vnc=2

vm_nic_1_id=char3
vm_nic_1_hostpath=/usr/local/var/run/openvswitch/vhost-client-2
vm_nic_1_net=net3
vm_nic_1_mac=00:03:00:00:00:03

vm_nic_2_id=char4
vm_nic_2_hostpath=/usr/local/var/run/openvswitch/vhost-client-3
vm_nic_2_net=net4
vm_nic_2_mac=00:04:00:00:00:04

echo
echo "Powering on $vm_name..."
if [ ! -f $vm_disk ];
then
	echo
	echo "File: $vm_disk not found."
	echo "You must first run the build script to download the VM disk files."
else

#	-virtfs local,path=${fs_path},mount_tag=${fs_mount_tag},security_model=none,readonly \

taskset -c ${cpu_vm2_core0},${cpu_vm2_core1},${cpu_vm2_core2},${cpu_vm2_core3} ${git_base_path}/qemu/x86_64-softmmu/qemu-system-x86_64 \
	-m 8G -smp 4,cores=4,threads=1,sockets=1 -cpu host \
	-drive format=raw,file=${vm_disk} \
	-boot c \
	-enable-kvm \
	-name ${vm_name},debug-threads=on \
	-uuid ${vm_uuid} \
	-object memory-backend-file,id=mem,size=8G,mem-path=/dev/hugepages,share=on \
	-numa node,memdev=mem -mem-prealloc \
	-netdev user,id=nttsip,hostfwd=tcp::${vm_ssh}-:22 \
	-device e1000,netdev=nttsip \
	-chardev socket,id=${vm_nic_1_id},path=${vm_nic_1_hostpath},server \
	-netdev type=vhost-user,id=${vm_nic_1_net},chardev=${vm_nic_1_id},vhostforce \
	-device virtio-net-pci,netdev=${vm_nic_1_net},mac=${vm_nic_1_mac},csum=off,gso=off,guest_tso4=off,guest_tso6=off,guest_ecn=off,mrg_rxbuf=off \
	-chardev socket,id=${vm_nic_2_id},path=${vm_nic_2_hostpath},server \
	-netdev type=vhost-user,id=${vm_nic_2_net},chardev=${vm_nic_2_id},vhostforce \
	-device virtio-net-pci,netdev=${vm_nic_2_net},mac=${vm_nic_2_mac},csum=off,gso=off,guest_tso4=off,guest_tso6=off,guest_ecn=off,mrg_rxbuf=off \
	-vnc :${vm_vnc} &
echo
echo "${vm_name} started!"
echo "VNC: ${vm_vnc}"
echo "ssh root@localhost -p ${vm_ssh}"
echo "username: root"
echo "password: root245"
fi
echo
echo
echo "Done"
echo
