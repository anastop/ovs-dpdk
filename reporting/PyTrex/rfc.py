import sys
import json
import argparse
import logging

FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('TrexA')
logger.setLevel(logging.INFO)

#sys.path.insert(0, "/opt/trex-core-2.26/scripts/automation/"+\
        #                   "trex_control_plane/stl/")
sys.path.insert(0, "/root/trex/trex/v2.53/scripts/automation/trex_control_plane/interactive/")
#sys.path.insert(0, "/opt/trex/v2.35/automation/trex_control_plane/stl")
from trex_stl_lib.api import STLClient, STLStream, STLPktBuilder, Ether, IP, STLTXCont,STLProfile


# Input - Action 
# {
#   "server": "192.168.128.51",
#   "ports": [0,1],
#   "action": "NDR",
#   "ethernet": {"dst":"", "src":""},
#   "ipv4": {"dst":"", "src":""},
#   "payload": "",
#   "frame_size": "",
#   "duration": "",
#   "rate": ""
# }

# c = STLClient()

# try:
    # c.connect()
    # print "is_all_ports_acquired() = " + str(c.is_all_ports_acquired())
    # print "is_connected() = " + str(c.is_connected())
    # print c.get_port_count()

    # for p in c.get_all_ports():
        # print c.get_port_attr(p)

    # c.acquire(ports=[0])
    # print "is_all_ports_acquired() = " + str(c.is_all_ports_acquired())

# finally:
    # c.disconnect()

class TrexTrafficGenerator():
    def __init__(self, params):
        self._params = params
        self._conn = None
        self._ports = []

    def connect(self):
        self._conn = STLClient(username="root",server="10.2.63.64")
        #print self._params["server"]
        # self._conn = STLClient()
        self._conn.connect()
        for p in self._conn.get_all_ports():
            logger.debug(p)
            self._ports.append(self._conn.get_port_attr(p))

        logger.debug(self._ports)
        self._conn.acquire(ports=self._params["ports"])

    def disconnect(self):
        self._conn.disconnect()

    def _create_stream(self, params, pkt_size=64):
        # Create base packet and pad it to size
        streams = []
        logger.debug(params)
        for s in params:
            # HW will add 4 bytes ethernet FCS
            size = pkt_size - 4
            base_pkt = Ether()/IP(src=s["ipv4"]["src"], dst=s["ipv4"]["dst"])
            pad = max(0, size - len(base_pkt)) * 'x'
            if isinstance(s["rate"], dict):
                if s["rate"]["type"] == "percentage":
                    mode = STLTXCont(percentage=s["rate"]["value"])
                elif s["rate"]["type"] == "pps":
                    mode = STLTXCont(pps=s["rate"]["value"])
            else:
                mode = STLTXCont(percentage=s["rate"])

            isg = 0
            if "isg" in s.keys():
                isg = s["isg"]

            streams.append(STLStream(packet=STLPktBuilder(pkt=base_pkt/pad),
                mode=mode, isg=isg))
            return streams

    def start(self, mult="100%", pkt_size=64):
        ports = self._params["ports"]
        streams = self._params["streams"]
        self._conn.reset(ports=ports)
        self._conn.clear_stats()
        self._conn.set_port_attr(ports, promiscuous=True)
        traffic_ports = []
        count = 1
        core_mask_array = []
        for p in ports:
            core_mask_array.append("0x" + str(count))
            count = count + 1
            for port_stream in streams:
                if port_stream["port"] == p:
                    stream = self._create_stream(port_stream["stream"], pkt_size)
                    self._conn.add_streams(stream, ports=[p])
                    traffic_ports.append(p)

        if self._params["warmup"] > 0:
            self._conn.start(ports=traffic_ports, mult=mult, duration=self._params["warmup"], core_mask=[0x3, 0x4],force=True)
            #self._conn.start(ports=traffic_ports, mult=mult, duration=self._params["warmup"], core_mask=core_mask_array)
            self._conn.wait_on_traffic(ports=traffic_ports, timeout=self._params["warmup"]+30)

        self._conn.clear_stats()

        self._conn.start(ports=traffic_ports, mult=mult, duration=self._params["duration"], core_mask=[0x3, 0x4], force=True)
        #self._conn.start(ports=traffic_ports, mult=mult, duration=self._params["duration"], core_mask=core_mask_array)

        self._conn.wait_on_traffic(ports=traffic_ports, timeout=self._params["duration"]+30, rx_delay_ms=5000)

        if self._conn.get_warnings():
            for warning in self._conn.get_warnings():
                logger.warn(warning)
        #figure out where to insert packet size!!!!!
        stats = self._conn.get_stats()

        result = {
                "mult": mult,
                "ports": []
                }

        for p in ports:
            peers = self._params["peers"]
            logger.debug(peers)
            peer = peers[str(p)]
            logger.info("mult = {4}, port {0}: opackets = {1}, peer {2}: ipackets = {3}, lost = {5},lost_rate = {6}".format(p, stats[p]["opackets"], peer, stats[peer]["ipackets"], mult, stats[p]["opackets"] - stats[peer]["ipackets"], float(stats[p]["opackets"] - stats[peer]["ipackets"])/float(stats[p]["opackets"])))
            result["ports"].append({
                "port": p,
                "tx": stats[p]["opackets"],
                "peer_rx": stats[peer]["ipackets"],
                "lost": stats[p]["opackets"] - stats[peer]["ipackets"]
                })

            logger.debug(stats)
        logger.debug(result)
        return result

    def binary_search(self, min_rate, max_rate, pkt_sz, threshold, step=10000):
        mult = max_rate
        mult_max = max_rate
        mult_min = min_rate
        last_no_lost_mult = min_rate

        search_count = 0

        while True:
            search_count = search_count + 1
            logger.info("======Binary Search {0}======".format(search_count))
            if pkt_sz != 2078:
                logger.info("Try: mult = {0} pps (min = {1}, max = {2}) {3} Gbps".format(mult, mult_min, mult_max, mult/1e9*(pkt_sz+20)*8))
            else:
                logger.info("Try: mult = {0} pps (min = {1}, max = {2})".format(mult,mult_min, mult_max))

            result = self.start(str(mult)+"pps", pkt_sz)
            #result = self.start()
            lost = False

            for port in result["ports"]:
                if float(port["lost"])/float(port["tx"]) > threshold:
                    lost = True

            if not lost:
                last_no_lost_mult = mult
                mult_min = mult
                mult = (mult_max - mult_min)/2 + mult_min
                if mult_max - mult_min < step:
                    break
            else:
                mult_max = mult
                mult = (mult_max - mult_min)/2 + mult_min
                if mult_max - mult_min < step:
                    break

        return last_no_lost_mult


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default="out.json",
            help="Result File.")
    parser.add_argument("--filename", type=str, default="cfg_file.json", help="Configuration JSON File")
    parser.add_argument("--packet", type=str, default="64",
            help="Packet Size")
    parser.add_argument("--duration", type=str, default="25", help="Duration to run test")
    parser.add_argument("--threshold",type=str, default="0.01", help="Threshold for Packet Loss")
    return parser.parse_args()
"""
def main():
    args = get_args()
    pkt_sizes = args.packet.split(",")
    thresh = args.threshold
    filename = args.filename
    duration = args.duration
    logger.info(pkt_sizes)
    output = {} 
    for pkt_size in pkt_sizes:
        #filename = "in_{0}.json".format(pkt_size)
        with open(filename, "r") as fv:
            input_params = json.load(fv)

        logger.debug(input_params)

        logger.info("\nBinary Search for packet size {0}".format(pkt_size))

        ttg = TrexTrafficGenerator(input_params)

        try:
            ttg.connect()
            print "connected"
            line_rate = 10000000000
            line_rate_pps = 18750000
            max_rate = {
                    "64": min(line_rate/(64+20)/8, line_rate_pps),
                    "128": min(line_rate/(128+20)/8, line_rate_pps),
                    "256": min(line_rate/(256+20)/8, line_rate_pps),
                    "512": min(line_rate/(512+20)/8, line_rate_pps),
                    "1024": min(line_rate/(1024+20)/8, line_rate_pps),
                    "1420": min(line_rate/(1420+20)/8, line_rate_pps),
                    "imix": 3320000
            }

            thresh = 0.01
            if pkt_size == 'imix':
                pkt_sz=2078
                result = ttg.binary_search(min_rate=1000, max_rate=max_rate[pkt_size],pkt_sz=2078, threshold=float(thresh), step=10000)
            else:
                result = ttg.binary_search(min_rate=1000, max_rate=max_rate[pkt_size],pkt_sz=int(pkt_size), threshold=float(thresh), step=10000)
                #result = ttg.start(mult="50%")		for changing the line rate
            if pkt_size == 'imix':
                pkt_size == 2078
            logger.info("Throughput => {0} pps {1} Gbps ".format(result, result*(int(pkt_size)+20)*8/1e9))
            output[pkt_size] = "{0} pps".format(result)
        finally:
            ttg.disconnect()

    logger.info(output)
    with open(args.output, "w") as fv:
        json.dump(output, fv)



if __name__ == "__main__":
    main()
"""
