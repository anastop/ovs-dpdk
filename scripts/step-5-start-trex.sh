#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh


# This script is intended to optimally configure TRex and launch it in
# a screen session for the user.


yaml_source="${git_base_path}/configs/trex/trex_cfg.yaml"
yaml_file="/etc/trex_cfg.yaml"


# Copy in the source yaml with variable placeholders for the CPU core numbers
cp ${yaml_source} ${yaml_file}

# Replace the variables in the YAML file for CPU cores
sed -e "s/PCI_ADDR_NIC0/${PCI_ADDR_NIC0}/g" ${yaml_file}
sed -e "s/PCI_ADDR_NIC1/${PCI_ADDR_NIC1}/g" ${yaml_file}
sed -e "s/PCI_ADDR_NIC2/${PCI_ADDR_NIC2}/g" ${yaml_file}
sed -e "s/PCI_ADDR_NIC3/${PCI_ADDR_NIC3}/g" ${yaml_file}
sed -e "s/cpu_trex_port0/${cpu_trex_port0}/g" ${yaml_file}
sed -e "s/cpu_trex_port1/${cpu_trex_port1}/g" ${yaml_file}
sed -e "s/cpu_trex_port2/${cpu_trex_port2}/g" ${yaml_file}
sed -e "s/cpu_trex_port3/${cpu_trex_port3}/g" ${yaml_file}
sed -e "s/cpu_trex_port4/${cpu_trex_port4}/g" ${yaml_file}
sed -e "s/cpu_trex_port5/${cpu_trex_port5}/g" ${yaml_file}
sed -e "s/cpu_trex_port6/${cpu_trex_port6}/g" ${yaml_file}
sed -e "s/cpu_trex_port7/${cpu_trex_port7}/g" ${yaml_file}
sed -e "s/cpu_trex_master/${cpu_trex_master}/g" ${yaml_file}
sed -e "s/cpu_trex_latency/${cpu_trex_latency}/g" ${yaml_file}


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
./trex_daemon_server start
echo
read -r -p "Press the ENTER key to launch the TRex console." key
echo
echo "Starting the TRex console"
cd ${trex_dir}
./trex-console --batch ${git_base_path}/configs/trex/trex-script.conf
./trex-console -f
