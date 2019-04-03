from time import sleep
from influxdb import InfluxDBClient
import random
import rfc
import sys
import time
sys.path.append("/root/trex/trex/v2.53/scripts/automation/trex_control_plane/interactive/")
from trex_stl_lib.api import STLClient, STLStream, STLPktBuilder, Ether, IP, STLTXCont, STLProfile
#cl = InfluxDBClient(host='localhost', port=8086)
#cl.switch_database('trexdb')

trex_connector = {}
#Enter your TREX server IP machine
trex_connector['clx'] = STLClient(username = "root", server="10.240.108.207")
trex_connector['clx'].connect()
#clx_trex_connector.get_active_pgids()
#clx_trex_connector.get_all_ports()

cl = InfluxDBClient(host='10.240.108.162', port=8086)
cl.switch_database('trexdb')


nports=6

while True:

    trex_connector['clx'].clear_stats(0)

    # Collect Rx and Tx Traffic BEFORE 1 second delay

    stats = {}
    stats['clx']=[]
    for p in range(nports):
        stats['clx'].append(trex_connector['clx'].get_xstats(p))
    
    rx_before = {}
    rx_before['clx'] = 0
    for p in range(nports):    
        rx_before['clx']+=stats['clx'][p]["rx_good_packets"]
    
    time.sleep(1)


    stats = {}
    stats['clx']=[]
    for p in range(nports):
        stats['clx'].append(trex_connector['clx'].get_xstats(p))

    rx_after = {}
    rx_after['clx'] = 0
    for p in range(nports):    
        rx_after['clx']+=stats['clx'][p]["rx_good_packets"]

    rx_bandwidth = {}
    rx_bandwidth['clx'] = rx_after['clx'] - rx_before['clx']

    clx = float(rx_bandwidth['clx'])

    clx_gbps = clx*276*8/1000000000

    newdata = [{"measurement" : 'rxdata', "fields" : {"clx" : clx, "clx_gbps" : clx_gbps}}]
    cl.write_points(newdata)
    sleep(1)
    print(clx)

