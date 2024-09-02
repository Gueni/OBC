
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
plcsim.rpc_connect()                                                                       
plcsim.load_model()  
cleardata.clear_data_folders()  
utc_numeric                            = str(int(time.strftime("%Y%m%d%H%M%S",  time.gmtime() )))
sim_idx                                = 1
plcsim.set_analysis_param(analvar)
plcsim.launch_analysis(modelname=modelname)
#? -------------------------------------------------------------------------------
