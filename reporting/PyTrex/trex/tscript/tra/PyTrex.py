#!/usr/bin/python3
import sys
import json
import argparse
import logging

FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('TrexA')
logger.setLevel(logging.INFO)

sys.path.insert(0, "/root/trex/tscript/trex-core-master/scripts/automation/trex_control_plane/stl/")
from trex_stl_lib.api import STLClient, STLStream, STLPktBuilder, Ether, IP, STLTXCont, STLProfile

class PyTrex(object):
	def __init__(self, filename):
		self.thresh = 0.01
		self.TrafficItem = TrafficItem(filename)
		self.TrafficItem.ttg
	#	try:
		self.TrafficItem.ttg.connect()
		print "hello"
		#insert whether you choose binary search or quicktest
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
	#include imix option??
		self.TrafficItem.start(duration, rate)
		self.qt = Quicktest(self.TrafficItem)
		self.qt.create_test(self.TrafficItem, packet_sizes)
		self.qt.error_check()
		self.qt.write_test()
#	finally:
		self.TrafficItem.ttg.disconnect()
		logger.info(output)
	#with open(args.output, "w") as fv:
	#	json.dump(output, fv)

class TrexTrafficGenerator(object):
	def __init__(self, input_params):
		self._conn = None
		self._ports = []
		self.input_params = input_params
	def connect(self):
		self._conn = STLClient()
		self._conn.connect()
		print "Connecting with ports"
		for p in self._conn.get_all_ports():
			logger.debug(p)
			self._ports.append(self._conn.get_port_attr(p))
		logger.debug(self._ports)
		self._conn.acquire(ports=self.input_params["ports"])
	def disconnect(self):
		self._conn.disconnect()

	def create_stream(self, params):
		streams = []
		logger.debug(params) 
		for s in params:  #create streams in Trex, I need a packet size.....
			size = s["frame_size"] - 4 #(need to pick the packet sizes before)
			base_pkt = Ether()/IP(src=s["ipv4"]["src"], dst=s["ipv4"]["dst"])
			pad = max(0, size - len(base_pkt)) * 'x'
			if isinstance(s["rate"], dict):
				if s["rate"]["type"] == "percentage":
					mode = STLTXCont(percenrage=s["rate"]["value"])
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
	def start(self, duration=30, rate=100):
        	ports = self.input_params["ports"]
	        streams = self.input_params["streams"]
        	self._conn.reset(ports=ports)
	        print " reset over"
        	self._conn.clear_stats()

	        self._conn.set_port_attr(ports, promiscuous=True)
		#self.rate (global variable)
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
            		self._conn.start(ports=traffic_ports, mult=mult, duration=duration, core_mask=[0x1, 0x2, 0x3, 0x4])
            		#self._conn.start(ports=traffic_ports, mult=mult, duration=self._params["warmup"], core_mask=core_mask_array)
            		self._conn.wait_on_traffic(ports=traffic_ports, timeout=self._params["warmup"]+30)

			self._conn.clear_stats()

			self._conn.start(ports=traffic_ports, mult=mult, duration=duration, core_mask=[0x1, 0x2, 0x3, 0x4])
        #self._conn.start(ports=traffic_ports, mult=mult, duration=self._params["duration"], core_mask=core_mask_array)

			self._conn.wait_on_traffic(ports=traffic_ports, timeout=duration+30, rx_delay_ms=5000)

		if self._conn.get_warnings():
		    for warning in self._conn.get_warnings():
   	            	logger.warn(warning)
   
	        stats = self._conn.get_stats()
	
	#def rate(%)
	#def rate_mpps():
	#	re
	#def rate_mbps()

class QuickTest(object):
	def __init__(self, tItem):
		self.TrafficItem = tItem
	output = [] 
	def create_test(self, packet_sizes):
	#packet sizes vaiable becomes member of class self.packetsizes, create test just passes packet sizes to the test
		for pkt_sz in len(packet_sizes):
			output[index] = run_test(min_Rate, max_rate, pkt_sz, threshold, step)

	def run_test(min_rate, max_rate, pkt_sz, threshold, step=10000):
		mult = max_rate
       		mult_max = max_rate,
        	mult_min = min_rate
	        last_no_lost_mult = min_rate

        	search_count = 0

	        while True:
            		search_count = search_count + 1
			logger.info("======Binary Search {0}======".format(search_count))
			if pkt_sz != 2078:
				logger.info("Try: mult = {0} pps (min = {1}, max = {2}) {3} gbps".format(mult, mult_min, mult_max, mult/1e9*(pkt_sz+20)*8))
			else:
				logger.info("Try: mult = {0} pps (min = {1}, max = {2})".format(mult,mult_min, mult_max))

			result = self.TrafficItem.start(str(mult)+"pps")
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

		#def error_check
			#did the binary search actually work? return a boolean otherwise
		#def write_result(filename.csv)
		#use output dictionary to reformat


	
