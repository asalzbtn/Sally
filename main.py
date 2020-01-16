# Author: Chu Sun

###############################################################################
# Imports
import os
#import array
#import Dispatch
import time
#import pandas as pd
#import numpy as np # linear algebra
#import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
#import matplotlib.pyplot as plt
from microgrid import Microgrid
###############################################################################

def  EMS_new(pv_power,ev_dmd,ev_dmd_1,ev_dmd_2,ev_dmd_3,avl_ESU_pwr,Gd_cons,req_ESU_pwr):
    PV2EV_enr =0
    ESU2EV_enr = 0
    Gd2EV_ENR=0
    EV_rest=0
    PV2Gd_enr=0
    PV2ESU_enr=0
    Gd2ESU_enr=0
    #iteration=0
    deltat = 1
    #ev_dmd_accept= 0
#    counter = 0   
#    t=0
#    if iteration==0 :
#        iteration=1
#        
    
 #Mode 1
    if (pv_power>=ev_dmd):
        PV2EV_enr= ev_dmd*deltat
    else:
         PV2EV_enr= pv_power*deltat                  
    # Mode 2: ESU2EV
    if (pv_power<ev_dmd):
        if ((ev_dmd-pv_power)<=avl_ESU_pwr):
                ESU2EV_enr=(ev_dmd-pv_power)*deltat
        else :
            ESU2EV_enr=avl_ESU_pwr*deltat
    else:
         if (pv_power>=ev_dmd):
                ESU2EV_enr=0        
    if (ESU2EV_enr>0):
        req_ESU_pwr=0 # we can not charge and discharge battery at the same time
   
    #Mode 3: Gd2EV
    if (pv_power<ev_dmd):
        if ((ev_dmd-pv_power)>avl_ESU_pwr):
            if ((ev_dmd-(pv_power+avl_ESU_pwr))<=Gd_cons):
                Gd2EV_ENR=(ev_dmd-(pv_power+avl_ESU_pwr))*deltat
                EV_rest=0
               # counter=1
            else:
                Gd2EV_ENR=Gd_cons*deltat
                EV_rest=(ev_dmd-(pv_power+avl_ESU_pwr+Gd_cons))*deltat
               # counter=1
        else:
            Gd2EV_ENR=0
            EV_rest=0
    else:
        Gd2EV_ENR=0
        EV_rest=0
           
    # Mode 5: PV2Gd
    if (pv_power<ev_dmd):
        PV2Gd_enr=0
    else :
        if (req_ESU_pwr>0):
            if ((pv_power-ev_dmd)<req_ESU_pwr):
                PV2Gd_enr=0
            else :
               PV2Gd_enr=(pv_power-(ev_dmd+req_ESU_pwr))*deltat
        else :
            if (req_ESU_pwr==0):
                PV2Gd_enr=(pv_power-ev_dmd)*deltat
                   
    if (req_ESU_pwr !=0):
          #Mode 4: PV2ESU
       if (pv_power<ev_dmd):
            PV2ESU_enr=0
       else:
            if(req_ESU_pwr>0):
                if ((pv_power-ev_dmd)<req_ESU_pwr):
                    PV2ESU_enr=(pv_power-ev_dmd)*deltat
                else:
                    PV2ESU_enr=req_ESU_pwr*deltat
            else:
                if (req_ESU_pwr==0):
                    PV2ESU_enr=0
                    
    # Mode 6: Gd2ESU
#                    if ((counter == 1) and ((iteration % (20e-6)) == 0)):
       if (pv_power<ev_dmd):
          if ((ev_dmd-pv_power)<Gd_cons):
              ii=(ev_dmd-pv_power)
              if ((Gd_cons-ii)<=req_ESU_pwr):
               Gd2ESU_enr=(Gd_cons-ii)*deltat
               
              else:
               Gd2ESU_enr=req_ESU_pwr*deltat;
               
          else:
              Gd2ESU_enr=0
              
    
       else:
           if (pv_power>=ev_dmd):
               if ((pv_power-ev_dmd)<req_ESU_pwr):
                   ii=(pv_power-ev_dmd)
                   if ((req_ESU_pwr-ii)<Gd_cons):
                       Gd2ESU_enr=(req_ESU_pwr-ii)*deltat
                       
                   else:
                       Gd2ESU_enr= Gd_cons*deltat
                       
               else:
                   if ((pv_power-ev_dmd)>=req_ESU_pwr): 
                       Gd2ESU_enr=0
                       
    else:
        PV2ESU_enr=0
        Gd2ESU_enr=0
#    iteration = iteration + 1
#    t = iteration
    
    Commands= [PV2EV_enr,ESU2EV_enr,Gd2EV_ENR,EV_rest,PV2Gd_enr,PV2ESU_enr,Gd2ESU_enr]#ev_dmd_accept,t
    return Commands


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
 
     PV2EV_enr=0
    
     ESU2EV_enr = 0
    
     Gd2EV_ENR=0
    
     EV_rest=0
    
     PV2Gd_enr=0
    
     PV2ESU_enr=0
    
     Gd2ESU_enr=0
    
     #t=np.zeros((288,), dtype=(int))
     pv_pow = command[0]
     net_ev_dmd = command[1]
     ev_dmd_1 = command[2]
     ev_dmd_2 = command[3]
     ev_dmd_3 = command[4]
     avl_ESU_pwr = command[5]
     Gd_con = command[6]
     req_ESU_pwr = command[7]
    
    
     Commands = EMS_new(pv_pow,net_ev_dmd,ev_dmd_1,ev_dmd_2,ev_dmd_3,avl_ESU_pwr,Gd_con,req_ESU_pwr)
     PV2EV_enr= Commands[0]
     ESU2EV_enr = Commands[1]
     Gd2EV_ENR=Commands[2]
     EV_rest=Commands[3]
     PV2Gd_enr=Commands[4]
     PV2ESU_enr=Commands[5]
     Gd2ESU_enr=Commands[6]
     
     #print(net_ev_dmd)
     print(PV2EV_enr)

     command1=tuple(Commands) # your sent data
     print(Commands)
     m.e.send(command1)    # send command
     elapsed_time = time.time() - start_time
    # time.sleep(0.1)

