from time import sleep
from influxdb import InfluxDBClient
import random
import rfc
import sys
import time
sys.path.append("/opt/trex/v2.35/automation/trex_control_plane/stl")
from trex_stl_lib.api import STLClient, STLStream, STLPktBuilder, Ether, IP, STLTXCont, STLProfile

trex_connector = {}
trex_connector['clx'] = STLClient(username = "root", server="10.2.63.64")
trex_connector['clx'].connect()
trex_connector['skx'] = STLClient(username = "root", server="10.2.62.99")
trex_connector['skx'].connect()
#clx_trex_connector.get_active_pgids()
#clx_trex_connector.get_all_ports()

cl = InfluxDBClient(host='localhost', port=8086)
cl.switch_database('trexdb')

nports=4 

while True:

    trex_connector['skx'].clear_stats(0)
    trex_connector['clx'].clear_stats(0)

    # Collect Rx and Tx Traffic BEFORE 1 second delay

    stats = {}
    stats['clx']=[]
    stats['skx']=[]
    for p in range(nports):
        stats['clx'].append(trex_connector['clx'].get_xstats(p))
        stats['skx'].append(trex_connector['skx'].get_xstats(p))
    
    rx_before = {}
    rx_before['clx'] = 0
    rx_before['skx'] = 0
    for p in range(nports):    
        rx_before['clx']+=stats['clx'][p]["rx_good_packets"]
        rx_before['skx']+=stats['skx'][p]["rx_good_packets"]
    
    time.sleep(1)


    stats = {}
    stats['clx']=[]
    stats['skx']=[]
    for p in range(nports):
        stats['clx'].append(trex_connector['clx'].get_xstats(p))
        stats['skx'].append(trex_connector['skx'].get_xstats(p))

    rx_after = {}
    rx_after['clx'] = 0
    rx_after['skx'] = 0
    for p in range(nports):    
        rx_after['clx']+=stats['clx'][p]["rx_good_packets"]
        rx_after['skx']+=stats['skx'][p]["rx_good_packets"]

    rx_bandwidth = {}
    rx_bandwidth['clx'] = rx_after['clx'] - rx_before['clx']
    rx_bandwidth['skx'] = rx_after['skx'] - rx_before['skx']

    clx = float(rx_bandwidth['clx'])
    skx = float(rx_bandwidth['skx'])

    clx_gbps = clx*276*8/1000000000
    skx_gbps = skx*276*8/1000000000

    newdata = [{"measurement" : 'rxdata', "fields" : {"skx" : skx , "skx_gbps": skx_gbps, "clx" : clx, "clx_gbps" : clx_gbps}}]
    cl.write_points(newdata)
    sleep(1)
    print(skx, clx)

