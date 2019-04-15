#!/bin/bash

# This script is intended to optimally configure TRex and launch it in
# a screen session for the user.

tmp_dir="/tmp"
trex_dir="/opt/ovs-dpdk-lab/trex"
yaml_file="/etc/trex_cfg.yaml"
yaml_source="/opt/ovs-dpdk-lab/configs/trex/trex_cfg.yaml"

cp ${yaml_source} ${yaml_file}

echo "Starting the TRex server"

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
	count=60
	num_ports=0
	while [ ${count} -gt 0 -a ${num_ports} -lt 2 ]; do
		sleep 1
		num_ports=`netstat -tln | grep -E :4500\|:4501 | wc -l`
		((count--))
	done
	if [ ${num_ports} -eq 2 ]; then
		echo "Session: \'screen -x trex\'"
		echo "Logs:    \'cat /tmp/trex.server.out\'"
		echo
		echo "Done. The TRex server is online"
		echo
	else
		echo "ERROR: The TRex server did not start properly.  Check \'screen -x trex\' and/or \'cat /tmp/trex.server.out\'"
		exit 1
	fi
else
	echo "ERROR: ${trex_dir} and/or ${tmp_dir} does not exist"
fi
echo
read -r -p "Press the ENTER key to launch the TRex console." key
echo
echo "Starting the TRex console"
cd {trex_dir}
./trex-console -f
