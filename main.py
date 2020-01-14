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
comm = Ethernet(50000,'192.168.22.143')

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
    print('commands:', end="")
    print(str([12, 24, 45, counter]))
		
    time.sleep(1)
		
