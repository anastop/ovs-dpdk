touch /etc/apt/sources.list.d/grafana.list
echo "deb https://packages.grafana.com/oss/deb stable main" > /etc/apt/sources.list.d/grafana.list
curl https://packages.grafana.com/gpg.key | apt-key add -
apt-get update
apt-get install grafana
