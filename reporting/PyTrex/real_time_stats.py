import rfc
import sys
import time
#sys.path.append("/mnt/DEV_system/root/trex/tscript/trex-core-master/scripts/automation/trex_control_plane/stl")
sys.path.append("/root/trex/trex/v2.53/scripts/automation/trex_control_plane/interactive/")
from trex_stl_lib.api import STLClient, STLStream, STLPktBuilder, Ether, IP, STLTXCont, STLProfile

trex_connector = STLClient(username = "root", server="10.240.108.207")
trex_connector.connect()
trex_connector.get_active_pgids()
trex_connector.get_all_ports()


while True:

    trex_connector.clear_stats(0)

    # Collect Rx and Tx Traffic BEFORE 1 second delay
    traffic_stats_before_port0 = trex_connector.get_xstats(0)
    traffic_stats_before_port1 = trex_connector.get_xstats(1)
    traffic_stats_before_port2 = trex_connector.get_xstats(2)
    traffic_stats_before_port3 = trex_connector.get_xstats(3)

    total_rx_packets_before = traffic_stats_before_port0["rx_good_packets"] + traffic_stats_before_port1["rx_good_packets"] + traffic_stats_before_port2["rx_good_packets"] + traffic_stats_before_port3["rx_good_packets"]

    total_tx_packets_before = traffic_stats_before_port0["tx_good_packets"] + traffic_stats_before_port1["tx_good_packets"] + traffic_stats_before_port2["tx_good_packets"] + traffic_stats_before_port3["tx_good_packets"]



    time.sleep(1)



    # Collect Rx and Tx Traffic AFTER 1 second delay
    traffic_stats_after_port0 = trex_connector.get_xstats(0)
    traffic_stats_after_port1 = trex_connector.get_xstats(1)
    traffic_stats_after_port2 = trex_connector.get_xstats(2)
    traffic_stats_after_port3 = trex_connector.get_xstats(3)


    total_rx_packets_after = traffic_stats_after_port0["rx_good_packets"] + traffic_stats_after_port1["rx_good_packets"] + traffic_stats_after_port2["rx_good_packets"] + traffic_stats_after_port3["rx_good_packets"]

    total_tx_packets_after = traffic_stats_after_port0["tx_good_packets"] + traffic_stats_after_port1["tx_good_packets"] + traffic_stats_after_port2["tx_good_packets"] + traffic_stats_after_port3["tx_good_packets"]



    rx_bandwidth = total_rx_packets_after - total_rx_packets_before

    tx_bandwidth = total_tx_packets_after - total_tx_packets_before



    print("\nRx Bandwidth (in pps): " + str(rx_bandwidth))

    #print "Tx Bandwidth (in pps): " + str(tx_bandwidth)
