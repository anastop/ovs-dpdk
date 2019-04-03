import time
import rfc
import json

   
class PyTrex():

    def __init__(self):
        self.args = ''
        self.pkt_sizes = ''
        self.thresh = ''
        self.filename = ''
        self.duration = ''
        self.results_filename = ''
        self.rate = '1'
        self.output = {}

    def set_traffic_args(self):
        
        #Testing Parameter Args
        self.args = rfc.get_args()
        self.pkt_sizes = self.args.packet.split(",")
        self.thresh = self.args.threshold
        self.results_filename = self.args.output
        self.filename = self.args.filename 
        self.duration = self.args.duration
        rfc.logger.info(self.pkt_sizes)

    def set_packet_rate(self, rate):
        #self.rate = rate
        self.rate = str(rate) + '%'
 

    def start_traffic(self):


        with open(self.filename, "r") as fv:
            input_params = json.load(fv)
        
        number_of_ports = len(input_params['streams'])
         
            
        #Start Traffic
        for pkt_size in self.pkt_sizes:
                      
            input_params['duration'] = 10            
            ttg = rfc.TrexTrafficGenerator(input_params)
        
            #Connect to the Trex Server
            ttg.connect()
            print "connected"

            #Start Traffic
            ttg.start(mult=self.rate)
            #ttg.start()

            #Wait 10 seconds before stopping the traffic
            time.sleep(10)

            #Disconnect from the Server
            self.stop_traffic(ttg)


    #Stop the traffic

    def stop_traffic(self,ttg):
        #Disconnect from the Server
        ttg.disconnect()


    #Start Binary Search Traffic Test
    
    def run_binary_search(self, duration):

        for pkt_size in self.pkt_sizes:
            with open(self.filename, "r") as fv:
                input_params = json.load(fv)
                      
            ttg = rfc.TrexTrafficGenerator(input_params)
        
            #Connect to the Trex Server
            ttg.connect()
            print "connected"

            rfc.logger.debug(input_params)
            rfc.logger.info("\nBinary Search for packet size {0}".format(pkt_size))

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

            thresh = self.thresh

	    if pkt_size == 'imix':
	        pkt_sz=2078
		result = ttg.binary_search(min_rate=1000, max_rate=max_rate[pkt_size],pkt_sz=2078, threshold=float(thresh), step=10000)
	    else:
    	        result = ttg.binary_search(min_rate=1000, max_rate=max_rate[pkt_size],pkt_sz=int(pkt_size), threshold=float(thresh), step=10000)
                #result = ttg.start(mult="50%")		for changing the line rate
	    
            if pkt_size == 'imix':
	        pkt_size == 2078
	        rfc.logger.info("Throughput => {0} pps {1} Gbps ".format(result, result*(int(pkt_size)+20)*8/1e9))
            
            self.output[pkt_size] = "{0} pps".format(result)
  

        #Save Results to a File
        rfc.logger.info(self.output)
        with open(self.results_filename, "w") as fv:
            json.dump(self.output, fv)


        #Disconnect from the Server
        self.stop_traffic(ttg)



def main():

    trex_instance = PyTrex()
    
    trex_instance.set_traffic_args()
    trex_instance.set_packet_rate(10)
    trex_instance.start_traffic()
    
    
    trex_instance.set_packet_rate(50)
    trex_instance.start_traffic()
    
    #trex_instance.run_binary_search(duration)



if __name__ == "__main__":
    main()
