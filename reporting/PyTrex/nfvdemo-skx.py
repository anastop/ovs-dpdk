from time import sleep
from influxdb import InfluxDBClient
import random
import rfc
import sys
import time
sys.path.append("/root/trex/trex/v2.53/scripts/automation/trex_control_plane/interactive/")
from trex_stl_lib.api import STLClient, STLStream, STLPktBuilder, Ether, IP, STLTXCont, STLProfile

trex_connector = {}
#Enter your TREX server IP address
trex_connector['skx'] = STLClient(username = "root", server="127.0.0.1")
trex_connector['skx'].connect()

cl = InfluxDBClient(host='localhost', port=8086)
cl.switch_database('trexdb')

nports=6

while True:

    trex_connector['skx'].clear_stats(0)

    # Collect Rx and Tx Traffic BEFORE 1 second delay

    stats = {}
    stats['skx']=[]
    for p in range(nports):
        stats['skx'].append(trex_connector['skx'].get_xstats(p))
    
    rx_before = {}
    rx_before['skx'] = 0
    for p in range(nports):    
        rx_before['skx']+=stats['skx'][p]["rx_good_packets"]
    
    time.sleep(1)


    stats = {}
    stats['skx']=[]
    for p in range(nports):
        stats['skx'].append(trex_connector['skx'].get_xstats(p))

    rx_after = {}
    rx_after['skx'] = 0
    for p in range(nports):    
        rx_after['skx']+=stats['skx'][p]["rx_good_packets"]

    rx_bandwidth = {}
    rx_bandwidth['skx'] = rx_after['skx'] - rx_before['skx']

    skx = float(rx_bandwidth['skx'])

    skx_gbps =skx*276*8/1000000000

    newdata = [{"measurement" : 'rxdata', "fields" : {"skx" : skx , "skx_gbps": skx_gbps, }}]
    cl.write_points(newdata)
    sleep(1)
    print(skx)

