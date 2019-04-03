#!/usr/bin/python3
import sys
import json
import argparse
import logging

FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('TrexA')
logger.setLevel(logging.INFO)

min_rate = 0
max_rate = 0
thresh = 0.01
#sys.path.insert(0, "/root/trex/tscript/trex-core-master/scripts/automation/trex_control_plane/stl/")
sys.path.insert(0, "/root/trex-core/automation/trex_control_plane/stl")
from trex_stl_lib.api import STLClient, STLStream, STLPktBuilder, Ether, IP, STLTXCont, STLProfile
class PyTrex(object):
    def __init__(self, filename):
        #self.thresh = 0.01
        self.rate_value = 100
        self.TrafficItem = TrafficItem(filename)
        self.TrafficItem.ttg
    #	try:
        #insert whether you choose binary search or quicktest
    #include imix option??
    #	if 'mpps' in rate_value:
    #		rate_percent = self.TrafficItem.rate_mpps(rate_value)
    #	if 'mbps' in rate_value:
    #		rate_percent = self.TrafficItem.ratembps(rate_value)
    #	#self.TrafficItem.start(duration, rate)
        packet_sizes = [64,128,256]
        self.qt = QuickTest(self.TrafficItem)
        output = self.qt.create_test(packet_sizes)
        #correct = self.qt.error_check(output)
        #if correct is True:
        #	self.qt.write_test(output, name)
#	finally:
            #self.TrafficItem.ttg.disconnect()
        logger.info(output)
    #with open(args.output, "w") as fv:
    #	json.dump(output, fv)

class TrexTrafficGenerator(object):
    def __init__(self, input_params):
        self._conn = None
        self._ports = []
        self.input_params = input_params
    def connect(self):
        self._conn = STLClient(server="localhost")
        self._conn.connect()
        for p in self._conn.get_all_ports():
            logger.debug(p)
            self._ports.append(self._conn.get_port_attr(p))
        logger.debug(self._ports)
        self._conn.acquire(ports=self.input_params["ports"])
    def disconnect(self):
        self._conn.disconnect()

    def create_stream(self, params, pkt_size):
        streams = []
        logger.debug(params) 
        for s in params:  #create streams in Trex, I need a packet size.....
            size = pkt_size - 4 #(need to pick the packet sizes before)
            base_pkt = Ether(dst=s["ether"]["dst"])/IP(src=s["ipv4"]["src"], dst=s["ipv4"]["dst"])
            pad = max(0, size - len(base_pkt)) * 'x'
            if isinstance(s["rate"], dict):
                if s["rate"]["type"] == "percentage":
                    mode = STLTXCont(percentage=s["rate"]["value"])
                elif s["rate"]["type"] == "pps":
                    mode = STLTX(pps=s["rate"]["value"])
            else:
                mode = STLTXCont(percentage=s["rate"])
            isg = 0
            if "isg" in s.keys():
                isg = s["isg"]
            streams.append(STLStream(packet=STLPktBuilder(pkt=base_pkt/pad),mode=mode, isg=isg))
        return streams

class TrafficItem(object):
    def __init__(self, filename):
        fd = open(filename, 'r')
        self.input_params = json.load(fd)
        logger.debug(self.input_params)
        self.ttg = TrexTrafficGenerator(self.input_params)
        self.pkt_size = 64
                #ports = self.input_params["ports"]

    def pktSize(self, new_size=None):
        self.pkt_size = new_size

    #fixed start to match PyIxia
    def start(self, duration=-1, rate_given='10mbps'):
        self.ttg.connect()
        if 'mpps' in rate_given:
            rate = self.rate_mpps(rate_given)
        if 'mbps' in rate_given:
            rate = self.rate_mbps(rate_given)

        ports = self.input_params["ports"]
        streams = self.input_params["streams"]
        self.ttg._conn.reset(ports=ports)
        self.ttg._conn.clear_stats()

        self.ttg._conn.set_port_attr(ports, promiscuous=True)
    #self.rate (global variable)
        self.traffic_ports = []

        count = 1
        core_mask_array = []
        for p in ports:
            core_mask_array.append("0x" + str(count))
            count = count + 1
            for port_stream in streams:
                if port_stream["port"] == p:
                    stream = self.ttg.create_stream(port_stream["stream"], self.pkt_size)
                    self.ttg._conn.add_streams(stream, ports=[p])
                    self.traffic_ports.append(p)

        if duration != -1:
            if self.ttg.input_params["warmup"] > 0:
                self.ttg._conn.start(ports=self.traffic_ports, mult=rate_given, duration=duration, core_mask=[0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8])
        #self._conn.start(ports=traffic_ports, mult=mult, duration=self._params["warmup"], core_mask=core_mask_array)
        if duration!= -1:
            self.ttg._conn.wait_on_traffic(ports=self.traffic_ports, timeout=self.ttg.input_params["warmup"]+30)
            self.ttg._conn.stop(self.traffic_ports)
        self.ttg._conn.clear_stats()

        self.ttg._conn.start(ports=self.traffic_ports, mult=rate_given, duration=duration, core_mask=[0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8])
#self._conn.start(ports=traffic_ports, mult=mult, duration=self._params["duration"], core_mask=core_mask_array)
        if duration != -1:
            self.ttg._conn.wait_on_traffic(ports=self.traffic_ports, timeout=duration+30, rx_delay_ms=5000)
            self.ttg._conn.stop(self.traffic_ports)

        if self.ttg._conn.get_warnings():
            for warning in self.ttg._conn.get_warnings():
                logger.warn(warning)

        stats = self.ttg._conn.get_stats()
        logger.debug(stats)
        result = {
                "mult": rate_given,
                "ports": []
                }

        for p in ports:
            peers = self.ttg.input_params["peers"]
            logger.debug(peers)
            peer = peers[str(p)]
            #logger.info("mult = {4}, port {0}: opackets = {1}, peer {2}: ipackets = {3}, lost = {5},lost_rate = {6}".format(p, stats[p]["opackets"], peer, stats[peer]["ipackets"], rate_given, stats[p]["opackets"] - stats[peer]["ipackets"], float(stats[p]["opackets"] - stats[peer]["ipackets"])/float(stats[p]["opackets"])))
            result["ports"].append({
                "port": p,
                "tx": stats[p]["opackets"],
                "peer_rx": stats[peer]["ipackets"],
                "lost": stats[p]["opackets"] - stats[peer]["ipackets"]
                })

            logger.debug(stats)
        logger.debug(result)
        #self.ttg.disconnect()
        return result

    #stop matches PyIxia
    def stop(self):
        self.ttg._conn.stop(self.traffic_ports)

    def rate_mpps(self, mpps):
        return (mpps / line_rate_pps) * 100
    def rate_mbps(self, mbps):
        return (int(mbps.strip('mbps')) / 10 / 1000000000) * 100

class QuickTest(object):
    def __init__(self, tItem):
        self.TrafficItem = tItem
        self.packet_sizes = []
        self.threshold = 0.01
        self.duration = 20
        output = [] 

    def run_test(self, test_id=0,step=10000): 
        #self.TrafficItem.ttg.connect()
        ret = []
        for  pkt_sz in self.packet_sizes:
            max_rate = int(self.max_rate[str(pkt_sz)])
            min_rate = self.min_rate
            self.TrafficItem.pktSize(pkt_sz)
            mult = max_rate
            mult_max = max_rate
            mult_min = min_rate
            last_no_lost_mult = min_rate

            search_count = 0

            while True:
                search_count = search_count + 1
                logger.info("-----Packet Size {}--------".format(pkt_sz))
                logger.info("======Binary Search {0}======".format(search_count))
                if pkt_sz != 2078:
                    logger.info("Try: mult = {0} pps (min = {1}, max = {2}) {3} gbps".format(mult, mult_min, mult_max, mult/1e9*(pkt_sz+20)*8))
                else:
                    logger.info("Try: mult = {0} pps (min = {1}, max = {2})".format(mult,mult_min, mult_max))

                result = self.TrafficItem.start(self.duration, str(mult)+"pps")
                lost = False

                for port in result["ports"]:
                    if float(port["lost"])/float(port["tx"]) > self.threshold:
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
        ret.append(mult)	
        return ret

#		self.TrafficItem.ttg.disconnect()

    def create_test(self, trafficItem=None, packet_sizes=[64], threshold=0.01, init_rate=100, duration=20):
        #packet sizes vaiable becomes member of class self.packetsizes, create test just passes packet sizes to the test
            line_rate = 10000000000
            line_rate_pps = 18750000

            self.max_rate = {
                    "64": min(line_rate/(64+20)/8, line_rate_pps),
                    "72": min(line_rate/(72+20)/8, line_rate_pps),
                    "128": min(line_rate/(128+20)/8, line_rate_pps),
                    "256": min(line_rate/(256+20)/8, line_rate_pps),
                    "512": min(line_rate/(512+20)/8, line_rate_pps),
                    "768": min(line_rate/(768+20)/8, line_rate_pps),
                    "1024": min(line_rate/(1024+20)/8, line_rate_pps),
                    "1280": min(line_rate/(1280+20)/8, line_rate_pps),
                    "1420": min(line_rate/(1420+20)/8, line_rate_pps),
                    "1518": min(line_rate/(1518+20)/8, line_rate_pps),
                    "imix": 3320000
                    }
            self.min_rate = 1000
            self.packet_sizes=packet_sizes
            self.threshold = threshold
            self.duration = duration
            #for pkt_sz in range(len(packet_sizes)):
            #		
            #		output[pkt_sz] = self.run_test(min_rate, max_rate, packet_sizes[pkt_sz], thresh, step=10000)


    #def error_check(self, output):
        # DO SOME CHECKING HERE and return a boolean

    def get_results(self, csv_name):
        print("pass")

        #def write_result(fileniddame.csv)
        #use output dictionary to reformat



