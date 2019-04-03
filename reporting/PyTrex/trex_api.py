#!/usr/bin/python

import json
import sys
import argparse
import string
global_server = '10.239.128.51'

#def get_raw_input_values():
#   obj = {}
#   print("Indicate the number of ports that you would like to run T-Rex on.")
#   action = raw_input("Enter the action to be performed: [NDR]/PDR ") or "NDR"
#   obj['duration'] = int(raw_input("Enter the duration for the test: [25] ") or 25)
#   obj['warmup'] = int(raw_input("Enter the warmup period for the test: [5] ") or 5)
#   ip_addr_dst = []
#   ip_addr_src = []
#   ether_dst = []
#   ether_src = []
#   for ip in ports:
#       ip_addr_dst[ip] = raw_input("Enter the ip dst address: ") 
#       ip_addr_src[ip] = raw_input("Enter the ip src address: ")
#       ether_dst[ip] = raw_input("Enter the ether dst address: ")
#       ether_src[ip] = raw_input("Enter the ether src address: ")

def create_port_list(ports):
    obj = []
    for port in range(0,ports):
        obj.append(port)
    return obj

def create_peer_list(ports):
    obj = {}
    for port in range(0,ports,2):
        obj[port] = port + 1
        obj[port + 1] = port 
    return obj

def create_each_port_imix(ports):
    obj = []
    num_packet_size = int(raw_input("Enter how many packet sizes to send [3]: ") or "3")
    for port in range(0,ports):
        obj1 = {}
        obj1['port'] = port
        obj1['stream'] = []
        ip_val = 105
        print(" ")
        print("Please enter in information for port {}".format(port))
        for packet in range(0,num_packet_size):
            obj2 = {}
            obj2['ether']= {}
            obj2['ether']['dst'] = raw_input("Enter the ether dst address [00:01:02:03:04:05]: ") or "00:01:02:03:04:05"
            obj2['ether']['src'] = raw_input("Enter the ether src address [05:04:03:02:01:00]: ") or "05:04:03:02:01:00"
            obj2['ipv4'] = {}
            obj2['ipv4']['dst'] = raw_input("Enter the ip src address [192.168." + str(ip_val) + ".2]: ") or "192.168." + str(ip_val) + ".2"
            obj2['ipv4']['src'] = raw_input("Enter the ip dst address [192.168." + str(ip_val) + ".0]: ") or "192.168." + str(ip_val) + ".105.0"
            obj2['payload'] = raw_input("Enter a payload [abcdefg]: ") or "abcdefg"
            obj2['frame_size'] = int(raw_input("Enter a frame_size [64]: ") or "64")
            obj2['rate'] = {}
            obj2['rate']['type'] = raw_input("Select a rate method [pps]/percentage:") or "pps"
            obj2['rate']['value'] = int(raw_input("Input a ratio value [7]: ") or "7")
            obj2['isg'] = float(raw_input("Enter the inter space gap (isg) [0.0]: " ) or '0.0')
            obj1['stream'].append(obj2)
            ip_val = ip_val + 1
        obj.append(obj1)
    return obj

def create_each_port_stream(ports):
    obj = []
    ip_val = 105
    ip_val_array = []
    ether_dst = 0
    ether_src = 0
    ip_src = 0
    ip_dst = 0
    repeat = "true"
    port = 0
    payload = " "
    rate = " "

    while port < ports:
        print(port)
        print(ports)
        obj1 = {}
        obj1['port'] = port
        obj1['stream'] = []
        obj2 = {}
        obj2['ether']= {}
        ether_dst = raw_input("Enter the ether dst address [00:01:02:03:04:05]: ") or "00:01:02:03:04:05"
        ether_src = raw_input("Enter the ether src address [05:04:03:02:01:00]: ") or "05:04:03:02:01:00"
        obj2['ether']['dst'] = ether_dst
        obj2['ether']['src'] = ether_src
        obj2['ipv4'] = {}
        ip_src = raw_input("Enter the ip src address [192.168." + str(ip_val) + ".2]: ") or "192.168." + str(ip_val) + ".2"
        ip_dst = raw_input("Enter the ip dst address [192.168." + str(ip_val) + ".0]: ") or "192.168." + str(ip_val) + ".0"
        obj2['ipv4']['dst'] = ip_src
        obj2['ipv4']['src'] = ip_dst
        ip_val_array = ip_dst.split(".")    
        for ip in range(0,len(ip_val_array)):
            if ip == 2:
                ip_val = ip_val_array[ip]
        obj2['frame_size'] = " "
        payload = raw_input("Enter a payload [abcdefg]: ") or "abcdefg"
        obj2['payload'] = payload
        rate = raw_input("Select a rate method [pps]/percentage: ") or "pps"
        obj2['rate'] = rate
        obj1['stream'].append(obj2)
        obj.append(obj1)
        port = port + 1
        #answer = raw_input("Do you want to increment your ip dst values by 1 and skip typing values? [yes]/no: ") or "yes"
        #if answer is "yes" or answer is "Yes":
#       repeat = "false"
#       port = ports
#       if answer is "no":
#           repeat = "true"

#   while port < ports:
#       obj1 = {}
#       obj1['port'] = port
 #             obj1['stream'] = []
  #           obj2 = {}
   #             obj2['ether']= {}
#       obj2['ether']['dst'] = ether_dst
#       obj2['ether']['src'] = ether_src
 #             obj2['ipv4'] = {}
#       obj2['ipv4']['src'] = ip_src
#       ip_val = ip_val + 1
#       ip_combined = ip_val_array[0]
#       ip_val_array[2] = ip_val
#       for ip in range(1, len(ip_val_array)):
#           ip_combined = ip_combined + "." + ip_val_array[ip]
#       obj2['ipv4']['dst'] = ip_combined
#       obj2['frame_size'] = " "
             #   obj2['payload'] = payload
             #   obj2['rate'] = rate
             #   obj1['stream'].append(obj2)
             #   obj.append(obj1)
 #             port = port + 1
#       
    return obj
#print(sys.version) 

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, default="test.json", help="Output File")
    return parser.parse_args()
def main():
    args = get_args()
    output_file = args.output
    print("Please follow the steps to create your json file to run RFC2544.")
    jsonFile = {}
    jsonFile['server'] = global_server
    ports = int(raw_input("Enter the number of ports: [4] ") or '4')
    jsonFile['ports'] = create_port_list(ports)
    jsonFile['peers'] = create_peer_list(ports)
    jsonFile['action'] = (raw_input("Enter the action to be performed [NDR]/PDR: ") or 'NDR')
    type_of_test = raw_input("Enter the type of test to be performed [Single Packet]/IMIX: ")
    if type_of_test == "IMIX":
        jsonFile['streams'] = []
        jsonFile['streams'] = create_each_port_imix(ports)
    else:
        jsonFile['streams'] = []
        jsonFile['streams'] = create_each_port_stream(ports)
    jsonFile['duration'] = int(raw_input("Enter the duration for the test: [25] ") or '25')
    jsonFile['warmup'] = int(raw_input("Enter the warmup period for the test: [5] ") or '5')
    #jsonFile['streams'] = create_each_port_stream(ports)
    filename = output_file
    with open(filename, 'w') as f:
        json.dump(jsonFile, f, indent=4, sort_keys=False)       
    #get the values, create the json, change the rfc2544 code to switch out packets and in a dfiferent step, have it go through the json to the rfc to test and run the ixia test
    #make ports and peersss and warmup and duration and warmup and durationll

if __name__ == "__main__":
    main()  
