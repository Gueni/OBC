
#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?                                  __    __    ______
#?                                 / /   / /   / ____/
#?                                / /   / /   / /     
#?                               / /___/ /___/ /___   
#?                              /_____/_____/\____/       
#?               
#?      
#?
#? Name:        LLC.py
#? Purpose:     Run Simulation for LLC Model.
#?
#? Author:      Mohamed Gueni ( mohamedgueni@outlook.com)
#?
#? Created:     09/15/2024
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------  
#? -------------------------------------------------------------------------------
import plecs as plc
import Model_Parameters as mdl
import cleardata
import os
import time
#?----------------------------------------------------------------------------------------------------------------------------------------
mdlvar                                 = mdl.ModelVars                                                        
modelname                              = "LLC"                                 
port                                   = "1080"                                                               
url                                    = f"http://localhost:{port}/RPC2"                                      
model_path                             = "0001 Modeling and Simulation/0000 PLECS SIMULATION/Model/LLC.plecs"                  
model_directory                        = (os.path.join(os.getcwd(), model_path)).replace("\\", "/")  

mdlvar                                 = mdl.ModelVars                                                                                                                             
plcsim                                 = plc.simpy(
                                                    url             =   url                 , 
                                                    port            =   port                , 
                                                    path            =   model_directory     ,  
                                                    modelvar        =   mdlvar              ,
                                                    analysisvars    =   mdlvar              ,
                                                    analysisName    =   'LLC'               ,
                                                    parasim         =   False               ,
                                                    paranum         =   1
                                                    )                                                                                                   
#?----------------------------------------------------------------------------------------------------------------------------------------
plcsim.rpc_connect()                                                                       
plcsim.load_model()  
cleardata.clear_data_folders()                                                                  
#?----------------------------------------------------------------------------------------------------------------------------------------
utc_numeric                            = str(int(time.strftime("%Y%m%d%H%M%S",  time.gmtime() )))
sim_idx                                = 1
mdlvar['ToFile']['sim_idx']            = sim_idx
mdlvar['ToFile']['utc_numeric']        = utc_numeric
mdlvar['ToFile']['ToFile_path']        = str((os.path.join(mdl.current_directory,mdl.ToFile_path+f"Results_{utc_numeric}_{sim_idx}.csv")).replace("\\", "/"))
mdlvar['ToFile']['logfile']            = str((os.path.join(mdl.current_directory,mdl.logfile_path+f"Log_{utc_numeric}_{sim_idx}.log")).replace("\\", "/"))
mdlvar['ToFile']['output_html']        = str((os.path.join(mdl.current_directory,mdl.output_html_path+f"Html_{utc_numeric}_{sim_idx}.html")).replace("\\", "/"))
mdlvar['ToFile']['Traces']             = str((os.path.join(mdl.current_directory,mdl.Traces_path)).replace("\\", "/"))

plcsim.logParams(str(mdlvar['ToFile']['logfile']),mdlvar)
plcsim.Set_sim_param(mdlvar)
plcsim.launch_sim(modelname=modelname)
# plcsim.HoldAllTraces(mdl.scopes)
# plcsim.saveAllTraces(mdl.scopes,mdl,mdlvar['ToFile']['Traces'])
#?----------------------------------