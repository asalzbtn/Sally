# Author: Chu Sun

###############################################################################
# Imports
import os
#import array
#import Dispatch
import time
from microgrid import Microgrid
###############################################################################
# OS checks and setup 
try:
    machine_name = os.uname()[1]
except AttributeError:
    print('Not running on controller!')
    pi = False
else:
    if machine_name == 'raspberrypi':
        print('Running on correct machine!')
        pi = True
    else:
        print('Not running on controller!')
        pi = False
        
###############################################################################
# Main Code

m  = Microgrid()
#command = array.array('d',[])
#for i in range(1):
#    command.append(1.0)
init_time=time.time()
#this is comment
last_error1=0
SoC1=0.9   ###0.9
flag2=1
StDS=1  ### 0 is SoC1>0.9, otherwise 11
while 1:
     start_time = time.time()
     command=list(m.e.status()) # read your received data
 # ####################put your script here#######################
 

     command[0],command[1]
	 command[0]=command[0]+command[1]+1;
	 
	  ########################################
     command1=tuple(command) # your sent data
     m.e.send(command1)    # send command
     elapsed_time = time.time() - start_time

