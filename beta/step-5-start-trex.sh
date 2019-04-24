#!/bin/bash

# Load the custom global environment variables
source /etc/0-ovs-dpdk-global-variables.sh


yaml_source="${git_base_path}/configs/trex/trex_cfg.yaml"
yaml_file="/etc/trex_cfg.yaml"

cd ${trex_dir}
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
echo "netstat -tln | grep -E :4500\|:4501"

echo "Session: screen -x trex"
echo "Logs:    cat /tmp/trex.server.out"
echo
echo "Done. The TRex server is online"
echo



echo "To launch config: " cd ${trex_dir}; ${trex_dir}/trex-console --batch ${git_base_path}/beta/trex-init-script.conf
echo "To launch load: " ${git_base_path}/beta/trex-load-64byte-base.sh
echo
echo "To launch the TRex Console, type: ${trex_dir}/trex-console -f"
echo 
