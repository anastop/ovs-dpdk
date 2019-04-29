#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh

export vhost_socket_path=/usr/local/var/run/openvswitch/vhost-client


#modprobe uio > /dev/null
#insmod $DPDK_BUILD/kmod/igb_uio.ko > /dev/null

# Bind OVS to the second NUMA node. All device IDs are 80 or higher.
python $DPDK_DIR/usertools/dpdk-devbind.py --bind=igb_uio ${PCI_ADDR_NIC4}
python $DPDK_DIR/usertools/dpdk-devbind.py --bind=igb_uio ${PCI_ADDR_NIC5}
python $DPDK_DIR/usertools/dpdk-devbind.py --bind=igb_uio ${PCI_ADDR_NIC6}
python $DPDK_DIR/usertools/dpdk-devbind.py --bind=igb_uio ${PCI_ADDR_NIC7}

# terminate OVS
pkill -9 ovs
rm -rf /usr/local/var/run/openvswitch
rm -rf /usr/local/etc/openvswitch/
rm -rf /usr/local/var/log/openvswitch
rm -f /tmp/conf.db

mkdir -p /usr/local/etc/openvswitch
mkdir -p /usr/local/var/run/openvswitch
mkdir -p /usr/local/var/log/openvswitch

# initialize new OVS database
cd $OVS_DIR
$OVS_DIR/ovsdb/ovsdb-tool create /usr/local/etc/openvswitch/conf.db $OVS_DIR/vswitchd/vswitch.ovsschema

#start database server
$OVS_DIR/ovsdb/ovsdb-server --remote=punix:$DB_SOCK \
	--remote=db:Open_vSwitch,Open_vSwitch,manager_options \
	--pidfile --detach

#As both TRex and OvS-DPDK create hugepages via DPDK, they need to change from the default hugepage-backed filenames
$OVS_DIR/utilities/ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-extra=”--file-prefix=ovs”

#initialize OVS database
$OVS_DIR/utilities/ovs-vsctl --no-wait init

# Configure OVS with the CPU cores and RAM for the SECOND NUMA node
$OVS_DIR/utilities/ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-init=true 
$OVS_DIR/utilities/ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-lcore-mask=${cpu_ovs_lcpu_mask} 
$OVS_DIR/utilities/ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-socket-mem="0,2048" 	# This assigns 2GB of RAM to the second NUMA node, and none to the first
$OVS_DIR/vswitchd/ovs-vswitchd unix:$DB_SOCK \
	--pidfile \
	--detach  \
	--log-file=/usr/local/var/log/openvswitch/ovs-vswitchd.log
$OVS_DIR/utilities/ovs-vsctl set Open_vSwitch . other_config:pmd-cpu-mask=${cpu_ovs_pmd_mask}
$OVS_DIR/utilities/ovs-vsctl set Open_vSwitch . other_config:max-idle=30000
# $OVS_DIR/utilities/ovs-vsctl set Open_vSwitch . other_config:vhost-iommu-support=true

#create OVS DPDK Bridge and add the four physical NICs
$OVS_DIR/utilities/ovs-vsctl add-br br0 -- set bridge br0 datapath_type=netdev
ifconfig br0 0 up
$OVS_DIR/utilities/ovs-vsctl add-port br0 dpdk0 -- set Interface dpdk0 type=dpdk options:dpdk-devargs=0000:${PCI_ADDR_NIC4} other_config:pmd-rxq-affinity="0:${cpu_ovs_dpdk0}"
$OVS_DIR/utilities/ovs-vsctl add-port br0 dpdk1 -- set Interface dpdk1 type=dpdk options:dpdk-devargs=0000:${PCI_ADDR_NIC5} other_config:pmd-rxq-affinity="0:${cpu_ovs_dpdk1}"
$OVS_DIR/utilities/ovs-vsctl add-port br0 dpdk2 -- set Interface dpdk2 type=dpdk options:dpdk-devargs=0000:${PCI_ADDR_NIC6} other_config:pmd-rxq-affinity="0:${cpu_ovs_dpdk2}"
$OVS_DIR/utilities/ovs-vsctl add-port br0 dpdk3 -- set Interface dpdk3 type=dpdk options:dpdk-devargs=0000:${PCI_ADDR_NIC7} other_config:pmd-rxq-affinity="0:${cpu_ovs_dpdk3}"

$OVS_DIR/utilities/ovs-vsctl add-port br0 vhost-client-0 -- set Interface vhost-client-0 type=dpdkvhostuserclient \
	options:vhost-server-path=${vhost_socket_path}-0 \
	other_config:pmd-rxq-affinity="0:${cpu_ovs_vhost0}"
	
$OVS_DIR/utilities/ovs-vsctl add-port br0 vhost-client-1 -- set Interface vhost-client-1 type=dpdkvhostuserclient \
	options:vhost-server-path=${vhost_socket_path}-1 \
	other_config:pmd-rxq-affinity="0:${cpu_ovs_vhost1}"
	
$OVS_DIR/utilities/ovs-vsctl add-port br0 vhost-client-2 -- set Interface vhost-client-2 type=dpdkvhostuserclient \
	options:vhost-server-path=${vhost_socket_path}-2 \
	other_config:pmd-rxq-affinity="0:${cpu_ovs_vhost2}"
	
$OVS_DIR/utilities/ovs-vsctl add-port br0 vhost-client-3 -- set Interface vhost-client-3 type=dpdkvhostuserclient \
	options:vhost-server-path=${vhost_socket_path}-3 \
	other_config:pmd-rxq-affinity="0:${cpu_ovs_vhost3}"

# $OVS_DIR/utilities/ovs-vsctl add-port br0 vhost-user0 -- set Interface vhost-user0 type=dpdkvhostuser other_config:pmd-rxq-affinity="0:${cpu_ovs_vhost0}"
# $OVS_DIR/utilities/ovs-vsctl add-port br0 vhost-user1 -- set Interface vhost-user1 type=dpdkvhostuser other_config:pmd-rxq-affinity="0:${cpu_ovs_vhost1}"
# $OVS_DIR/utilities/ovs-vsctl add-port br0 vhost-user2 -- set Interface vhost-user2 type=dpdkvhostuser other_config:pmd-rxq-affinity="0:${cpu_ovs_vhost2}"
# $OVS_DIR/utilities/ovs-vsctl add-port br0 vhost-user3 -- set Interface vhost-user3 type=dpdkvhostuser other_config:pmd-rxq-affinity="0:${cpu_ovs_vhost3}"

# $OVS_DIR/utilities/ovs-vsctl show
# $OVS_DIR/utilities/ovs-appctl dpif-netdev/pmd-rxq-show

$OVS_DIR/utilities/ovs-ofctl add-flow br0 in_port=1,idle_timeout=0,action=output:5
$OVS_DIR/utilities/ovs-ofctl add-flow br0 in_port=2,idle_timeout=0,action=output:6
$OVS_DIR/utilities/ovs-ofctl add-flow br0 in_port=3,idle_timeout=0,action=output:7
$OVS_DIR/utilities/ovs-ofctl add-flow br0 in_port=4,idle_timeout=0,action=output:8

$OVS_DIR/utilities/ovs-ofctl add-flow br0 in_port=5,idle_timeout=0,action=output:1
$OVS_DIR/utilities/ovs-ofctl add-flow br0 in_port=6,idle_timeout=0,action=output:2
$OVS_DIR/utilities/ovs-ofctl add-flow br0 in_port=7,idle_timeout=0,action=output:3
$OVS_DIR/utilities/ovs-ofctl add-flow br0 in_port=8,idle_timeout=0,action=output:4

# $OVS_DIR/utilities/ovs-ofctl dump-flows br0


echo
echo "OVS Started"
echo

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
fi

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
fi
echo
echo
echo "VMs Started"
echo



yaml_source="${git_base_path}/configs/trex/trex_cfg.yaml"
yaml_file="/etc/trex_cfg.yaml"


# Copy in the source yaml with variable placeholders for the CPU core numbers
cp ${yaml_source} ${yaml_file}

# Replace the variables in the YAML file for CPU cores
sed -i -e 's/PCI_ADDR_NIC0/'"${PCI_ADDR_NIC0}"'/g' \
     -e 's/PCI_ADDR_NIC1/'"${PCI_ADDR_NIC1}"'/g' \
     -e 's/PCI_ADDR_NIC2/'"${PCI_ADDR_NIC2}"'/g' \
     -e 's/PCI_ADDR_NIC3/'"${PCI_ADDR_NIC3}"'/g' \
     -e 's/cpu_trex_port0/'"${cpu_trex_port0}"'/g' \
     -e 's/cpu_trex_port1/'"${cpu_trex_port1}"'/g' \
     -e 's/cpu_trex_port2/'"${cpu_trex_port2}"'/g' \
     -e 's/cpu_trex_port3/'"${cpu_trex_port3}"'/g' \
     -e 's/cpu_trex_port4/'"${cpu_trex_port4}"'/g' \
     -e 's/cpu_trex_port5/'"${cpu_trex_port5}"'/g' \
     -e 's/cpu_trex_port6/'"${cpu_trex_port6}"'/g' \
     -e 's/cpu_trex_port7/'"${cpu_trex_port7}"'/g' \
     -e 's/cpu_trex_master/'"${cpu_trex_master}"'/g' \
     -e 's/cpu_trex_latency/'"${cpu_trex_latency}"'/g' ${yaml_file}


echo "Starting the TRex server"

num_ports=`netstat -tln | grep -E :4500\|:4501 | wc -l`

if [ ! ${num_ports} -lt 2 ]; then
	echo
	echo "TRex server is already running."
	echo
else
	if [ -d ${trex_dir} -a -d ${tmp_dir} ]; then
		pushd ${trex_dir} 2>/dev/null
		trex_server_cmd="./t-rex-64 -i --cfg ${yaml_file} --iom 0 -v 4"
		rm -fv /tmp/trex.server.out
		screen -dmS trex -t server ${trex_server_cmd}
		screen -x trex -X chdir /tmp
		screen -x trex -p server -X logfile trex.server.out
		screen -x trex -p server -X logtstamp on
		screen -x trex -p server -X log on

		echo
		echo "Waiting for the TRex server to be ready..."
		echo
		echo "Please be patient, this may take up to 2 minutes."
		echo
		count=120
		num_ports=0
		while [ ${count} -gt 0 -a ${num_ports} -lt 2 ]; do
			sleep 1
			num_ports=`netstat -tln | grep -E :4500\|:4501 | wc -l`
			((count--))
		done
		if [ ${num_ports} -eq 2 ]; then
			echo "Session: screen -x trex"
			echo "Logs:    cat /tmp/trex.server.out"
			echo
			echo "Done. The TRex server is online"
			echo
		else
			echo "ERROR: The TRex server did not start properly.  Check 'screen -x trex' and/or 'cat /tmp/trex.server.out'"
			exit 1
		fi
	else
		echo "ERROR: ${trex_dir} and/or ${tmp_dir} does not exist"
	fi
	echo
fi
cd ${trex_dir}
#./trex_daemon_server start
echo "run ./trex-console --batch ${git_base_path}/configs/trex/trex-init-script.conf"
# echo
# read -r -p "Press the ENTER key to launch the TRex console." key
# echo
# echo "Starting the TRex console"
# cd ${git_base_path}/scripts
echo
echo "To start a TRex workload, type: ./trex-load-64byte-base.sh"
echo
echo "To launch the TRex Console, type: ${trex_dir}/trex-console -f"
echo 
