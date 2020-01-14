# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:47:28 2020

@author: HP
"""
import pandas as pd
import numpy as np # linear algebra
#import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

#pv_power=120e3
#ev_dmd=150e3
#ev_dmd_1=50e3
#ev_dmd_2=50e3
#ev_dmd_3=50e3
#deltat=1
#avl_ESU_pwr=50e3
#Gd_cons=25e3
#req_ESU_pwr=50e3
#iteration=0
#counter=0

#Initialization
#PV2EV_enr = 0
#ESU2EV_enr = 0
#Gd2EV_ENR=0
#EV_rest=0;
#PV2Gd_enr=0;
#PV2ESU_enr=0;
#Gd2ESU_enr=0;
#counter = 0;
def  EMS_new(pv_power,ev_dmd, deltat,avl_ESU_pwr,Gd_cons,req_ESU_pwr):
    PV2EV_enr =0
    ESU2EV_enr = 0
    Gd2EV_ENR=0
    EV_rest=0
    PV2Gd_enr=0
    PV2ESU_enr=0
    Gd2ESU_enr=0
    iteration=0
    #ev_dmd_accept= 0
    counter = 0   
    t=0
    if iteration==0 :
        iteration=1
        
    
 #Mode 1
    if (pv_power>=ev_dmd):
        PV2EV_enr= ev_dmd*deltat
    else:
         PV2EV_enr= pv_power*deltat                  
    # Mode 2: ESU2EV
    if (pv_power<ev_dmd):
        if ((np.subtract(ev_dmd,pv_power))<=avl_ESU_pwr):
                ESU2EV_enr=(np.subtract(ev_dmd,pv_power))*deltat
        else :
            ESU2EV_enr=avl_ESU_pwr*deltat
    else:
         if (pv_power>=ev_dmd):
                ESU2EV_enr=0;        
    if (ESU2EV_enr>0):
        req_ESU_pwr=0 # we can not charge and discharge battery at the same time
    ...
    #Mode 3: Gd2EV
    if (pv_power<ev_dmd):
        if ((np.subtract(ev_dmd,pv_power))>avl_ESU_pwr):
            if ((np.subtract(ev_dmd,np.sum((pv_power,avl_ESU_pwr))))<=Gd_cons):
                Gd2EV_ENR=(np.subtract(ev_dmd,np.sum((pv_power,avl_ESU_pwr))))*deltat
                EV_rest=0
                counter=1
            else:
                Gd2EV_ENR=Gd_cons*deltat
                EV_rest=(np.subtract(ev_dmd,np.sum((pv_power,avl_ESU_pwr,Gd_cons))))*deltat
                counter=1
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
            if ((np.subtract(pv_power,ev_dmd))<req_ESU_pwr):
                PV2Gd_enr=0
            else :
               PV2Gd_enr=np.subtract((pv_power,np.sum(ev_dmd,req_ESU_pwr)))*deltat
        else :
            if (req_ESU_pwr==0):
                PV2Gd_enr=np.subtract(pv_power,ev_dmd)*deltat
                   
    if (req_ESU_pwr !=0):
          #Mode 4: PV2ESU
       if (pv_power<ev_dmd):
            PV2ESU_enr=0
       else:
            if(req_ESU_pwr>0):
                if (np.subtract(pv_power,ev_dmd)<req_ESU_pwr):
                    PV2ESU_enr=np.subtract(pv_power,ev_dmd)*deltat
                else:
                    PV2ESU_enr=req_ESU_pwr*deltat
            else:
                if (req_ESU_pwr==0):
                    PV2ESU_enr=0
                    ...
    # Mode 6: Gd2ESU
                    if ((counter == 1) and ((iteration % (20e-6)) == 0)):
                        if (pv_power<ev_dmd):
                            if (np.subtract(ev_dmd,pv_power)<Gd_cons):
                                if (np.subtract(Gd_cons,np.subtract((ev_dmd,pv_power)))<=req_ESU_pwr):
                                    Gd2ESU_enr=np.subtract(Gd_cons,np.sub((ev_dmd,pv_power)))*deltat
                                else:
                                    Gd2ESU_enr=req_ESU_pwr*deltat;
                            else:
                                Gd2ESU_enr=0
    
                        else:
                            if (np.subtract(pv_power,ev_dmd)<req_ESU_pwr):
                                if (np.subtract(req_ESU_pwr,np.subtract((pv_power,ev_dmd)))<Gd_cons):
                                    Gd2ESU_enr=np.subtract(req_ESU_pwr,np.subtract((pv_power,ev_dmd)))*deltat
                                else:
                                    Gd2ESU_enr= Gd_cons*deltat
                            else:
                                Gd2ESU_enr= 0
    else:
        PV2ESU_enr=0
        Gd2ESU_enr=0
    iteration = iteration + 1
    t = iteration
    
    Commands= [PV2EV_enr,ESU2EV_enr,Gd2EV_ENR,EV_rest,PV2Gd_enr,PV2ESU_enr,Gd2ESU_enr,t]#ev_dmd_accept,t
    return Commands

ev_dmd_1=pd.read_csv('ev_dmd_1.csv')
ev_dmd_1=ev_dmd_1.drop(columns=['Time'])
ev_dmd_1=ev_dmd_1.to_numpy()
#

#
ev_dmd_2=pd.read_csv('ev_dmd_2.csv')
ev_dmd_2=ev_dmd_2.drop(columns=['Time'])
ev_dmd_2=ev_dmd_2.to_numpy()
#

#
ev_dmd_3=pd.read_csv('ev_dmd_3.csv')
ev_dmd_3=ev_dmd_3.drop(columns=['Time'])
ev_dmd_3=ev_dmd_3.to_numpy()

#

#

#
pv_pow=pd.read_csv('PV_pow.csv')
pv_pow=pv_pow.drop(columns=['Time'])
pv_pow=pv_pow.to_numpy()

#
#
avl_ESU_pwr=pd.read_csv('avl_ESU_pwr.csv')
avl_ESU_pwr=avl_ESU_pwr.to_numpy()
#
#
req_ESU_pwr=pd.read_csv('req_ESU_pwr.csv')
req_ESU_pwr=req_ESU_pwr.to_numpy()

net_ev_dmd = np.zeros(len(ev_dmd_1))

for i in range (len(ev_dmd_1)):
    net_ev_dmd[i]=sum([ev_dmd_1[i],ev_dmd_2[i],ev_dmd_3[i]])
  
        

#ev_dmd=net_ev_dmd
#ev_dmd=ev_dmd.to_numpy()
t=0
soc_min=  20
soc_max=90
ESU_ENG_Max=50e3*60
ESU_Max_pwr=50e3
ESU_inj_pwr=50e3
ESU_ini=0

Gd_con= np.ones((288,), dtype=(int))
Gd_con=Gd_con*25e3

PV2EV_enr=np.zeros((288,), dtype=(int))

ESU2EV_enr = np.zeros((288,), dtype=(int))

Gd2EV_ENR=np.zeros((288,), dtype=(int))

EV_rest=np.zeros((288,), dtype=(int))

PV2Gd_enr=np.zeros((288,), dtype=(int))

PV2ESU_enr=np.zeros((288,), dtype=(int))

Gd2ESU_enr=np.zeros((288,), dtype=(int))

t=np.zeros((288,), dtype=(int))

for j in range (len(ev_dmd_1)):
    Commands = EMS_new(pv_pow[j],net_ev_dmd[j] , 1,avl_ESU_pwr[j],Gd_con[j],req_ESU_pwr[j])
    PV2EV_enr[j]= Commands[0]
    ESU2EV_enr[j] = Commands[1]
    Gd2EV_ENR[j]=Commands[2]
    EV_rest[j]=Commands[3]
    PV2Gd_enr[j]=Commands[4]
    PV2ESU_enr[j]=Commands[5]
    Gd2ESU_enr[j]=Commands[6]
    t[j]=Commands[7]
#    PV2EV_enr[j]= float(Commands[0])
#    ESU2EV_enr[j] = float(Commands[1])
#    Gd2EV_ENR[j]=float(Commands[2])
#    EV_rest[j]=float(Commands[3])
#    PV2Gd_enr[j]=float(Commands[4])
#    PV2ESU_enr[j]=float(Commands[5])
#    Gd2ESU_enr[j]=float(Commands[6])
#    t[j]=float(Commands[7])
    
    
#
    #(PV2EV_enr[j],ESU2EV_enr[j],Gd2EV_ENR[j],EV_rest[j],PV2Gd_enr[j],PV2ESU_enr[j],Gd2ESU_enr[j],t[j])