# OPAL-RT Technologies Inc.
#This script is provided 'as is', without warranty of any kind.

##Import Libraries
import array
from ServerRP import Ethernet
import socket
import time

##Initiate Communications with the simulator
## CHANGE THE IP ADDRESS ACCORDINGLY
## (The IP address is the one from the raspberry PI)
comm = Ethernet(45000,'132.206.62.241')

time.sleep(1)
counter = 0

# This script will run indefinitely
while True:
    
    ##Obtain measurements from simulator
    Meas = comm.status()
    print (Meas)
    time.sleep(1)
    counter = counter + 1
    
    ##Send commands to the simulator
    comm.send([12, 24, 45, counter])
    print('commands:')
    print(str([12, 24, 45, counter]))
		
    time.sleep(1)
		
