
#?----------------------------------------------------------------------------------------------------------------------------------------
#?                                                             ____  ____  ______
#?                                                            / __ \/ __ )/ ____/
#?                                                           / / / / __  / /
#?                                                          / /_/ / /_/ / /___
#?                                                          \____/_____/\____/
#?
#?----------------------------------------------------------------------------------------------------------------------------------------
import plecs as plc
import Model_Parameters as mdl
import os
import process
#?----------------------------------------------------------------------------------------------------------------------------------------
port                = "1080"                                                               
url                 = f"http://localhost:{port}/RPC2"                                      
mdlvar              = mdl.ModelVars                                                        
model_path          = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Model/OBC.plecs" 
current_directory   = os.getcwd()                                                          
directory           = os.path.join(current_directory, model_path)                          
directory           = directory.replace("\\", "/")                                         
modelname           = "OBC"                                                                
#?----------------------------------------------------------------------------------------------------------------------------------------
plcsim              = plc.simpy(url=url , port=port , path=directory , modelvar=mdlvar)    
plcsim.rpc_connect()                                                                       
plcsim.load_model()                                                                        
#?----------------------------------------------------------------------------------------------------------------------------------------
with open(mdlvar['ToFile']['logfile'], "a") as file:
    plcsim.log_parameters(mdlvar, file)
file.close
plcsim.ClearAllTraces(mdlvar['scopes'])  
plcsim.Set_sim_param()
plcsim.launch_sim(modelname=modelname)
# plcsim.HoldAllTraces(mdlvar['scopes'])
# plcsim.saveAllTraces(mdlvar['scopes'],mdlvar['ToFile']['RES'])
process.gen_plots(resFile= mdlvar['ToFile']['ToFile_path'], html_file=mdlvar['ToFile']['output_html'],OPEN=True)
#?----------------------------------------------------------------------------------------------------------------------------------------






