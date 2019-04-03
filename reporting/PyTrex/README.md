# PyTrex


### Purpose: 
* Run TRex using automation in a manner similar to PyIxia


### Tools Available:
trex_api.py 	     -->  builds the .json files as input to the automation script
rfc.py  	     -->  contains the RFC 2544 automation for running the TRex Traffic Generator
run_trex_traffic.py  -->  work in progress class that makes use of the RFC automation to run TRex
	- Currently it's functionality can be described in the README file. 
cfg_file_2portVersion.json
cfg_file_4portVersion.json 


### Sample Run Command:
python run_trex_traffic.py --help   -->  will provide the user with a description of each command-line argument accepted by this					 program

python run_trex_traffic.py --filename <input_json_file> --output <output_json_arbitrary_filename>

+Command above will configure TRex traffic according to the input .json file.  
+In this project folder, the two accompanying .json files can be used as input for successful traffic forwarding between the server & DUT for 2 and 4 port test cases. 
+In its current state, the run_trex_traffic.py script will start by running 64-byte traffic for 10 seconds and then stop.  Following this, it will perform a binary search on the line rate until it satisfies the loss threshold. 
