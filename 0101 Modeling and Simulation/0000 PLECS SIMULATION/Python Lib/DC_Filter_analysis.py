
#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?                   ____  ______   _______ ____
#?                  / __ \/ ____/  / ____(_) / /____  _____
#?                 / / / / /      / /_  / / / __/ _ \/ ___/
#?                / /_/ / /___   / __/ / / / /_/  __/ /    
#?               /_____/\____/  /_/   /_/_/\__/\___/_/     
#?               
#?      
#?
#? Name:        DC_Filter_analysis.py
#? Purpose:     Run AC sweep Analysis for the HV DC Filter.
#?
#? Author:      Mohamed Gueni ( mohamedgueni@outlook.com)
#?
#? Created:     09/02/2024
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------  
#? -------------------------------------------------------------------------------

import os
import time
import plecs as plc
import cleardata
import Model_Parameters as mdl
import post_process
import numpy as np
from itertools import product

port                                   = "1080"                                                               
url                                    = f"http://localhost:{port}/RPC2"                                      
analvar                                = mdl.AnalysisOpts                                                        
modelname                              = "DC HV Filter Analysis"   
model_path                             = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Model/DC HV Filter Analysis.plecs"                  
model_directory                        = (os.path.join(os.getcwd(), model_path)).replace("\\", "/")  
mdlvar                                 = mdl.ModelVars                                                                                                                             
plcsim                                 = plc.simpy(
                                                    url             =   url                 , 
                                                    port            =   port                , 
                                                    path            =   model_directory     ,  
                                                    modelvar        =   mdlvar              ,
                                                    analysisvars    =   analvar             ,
                                                    analysisName    =   'DC Filter AC Sweep'
                                                    )  

Cx                                     = np.arange(10e-6     , 10e-6 +1e-6  , 10e-6).tolist()       
Cy                                     = np.linspace(50e-6   , 50e-6 +50e-6  , num=len(Cx)).tolist()    
L                                      = np.linspace(50e-6   , 50e-6 +50e-6 , num=len(Cx)).tolist()    
chokeL1                                = np.linspace(50e-3 , 50e-3+50e-3, num=len(Cx)).tolist()  
chokeL2                                = np.linspace(50e-3 , 50e-3+50e-3, num=len(Cx)).tolist() 

plcsim.rpc_connect()                                                                       
plcsim.load_model()  
cleardata.clear_data_folders()  
utc_numeric                            = str(int(time.strftime("%Y%m%d%H%M%S",  time.gmtime() )))
sim_idx                                = 1
mdlvar['ToFile']['sim_idx']            = sim_idx
mdlvar['ToFile']['utc_numeric']        = utc_numeric
mdlvar['ToFile']['logfile']            = str((os.path.join(mdl.current_directory,mdl.logfile_path+f"Log_{utc_numeric}_{sim_idx}.log")).replace("\\", "/"))
analvar['DC_Filter']                   = mdlvar['HV_Filter']
mdlvar['ToFile']['output_html']        = str((os.path.join(mdl.current_directory,mdl.output_html_path+f"Html_{utc_numeric}_{sim_idx}.html")).replace("\\", "/"))

combinations    = product(Cx, Cy, L, chokeL1, chokeL2)
result_list     = []

for i, (item1, item2, item3, item4, item5) in enumerate(combinations):
    print(f'iteration =  {i} | Cx = {item1} F | Cy = {item2} F | L = {item3} H | chokeL1 = {item4} H | ChokeL2 = {item5} H ')
    analvar['DC_Filter']['Cy']['Cap_s']                   = item1 #Cx[i]
    analvar['DC_Filter']['Cx']['Cap_s']                   = item2 #Cy[i]
    analvar['DC_Filter']['L']                             = item3 #L[i]
    analvar['DC_Filter']['Choke']['L1']                   = item4 #chokeL1[i]
    analvar['DC_Filter']['Choke']['L2']                   = item5 #chokeL2[i]

    plcsim.logParams(str(mdlvar['ToFile']['logfile']),analvar)
    plcsim.set_analysis_param(analvar)
    results                                = plcsim.launch_analysis(modelname=modelname)
    result_list.append(results)
    plcsim.logParams(str(mdlvar['ToFile']['logfile']),result_list[0])
post_process.plot_ac_analysis_sweep(result_list, html_file=mdlvar['ToFile']['output_html'],OPEN=True)
#? -------------------------------------------------------------------------------

