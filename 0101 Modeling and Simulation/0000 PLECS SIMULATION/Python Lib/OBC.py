
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
port                = "1080"                                                                  # Port to which to connect the RPC server.    
url                 = f"http://localhost:{port}/RPC2"                                       # Replace localhost with actual ip adress if you run from remote.
mdlvar              = mdl.ModelVars                                                         # Variable model dictionary.
model_path          = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Model/OBC.plecs"  # model relative path. 
current_directory   = os.getcwd()                                                           # Get the current working directory.
directory           = os.path.join(current_directory, model_path)                           # Join both paths.
directory           = directory.replace("\\", "/")                                          # Replace backslashes (\) with forward slashes (/).
modelname           = "OBC"                                                                 # plecs model name.
save_path           = "0101 Modeling and Simulation/0000 PLECS SIMULATION/RES"
log_file            = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/parameters.log"
#?----------------------------------------------------------------------------------------------------------------------------------------
plcsim              = plc.simpy(url=url , port=port , path=directory , modelvar=mdlvar)    # set a simpy object with all the needed vars.
plcsim.rpc_connect()                                                                       # Connect to plecs through the given url and port.
plcsim.load_model()                                                                        # load the plecs model.
#?----------------------------------------------------------------------------------------------------------------------------------------

with open(os.path.join(current_directory, log_file).replace("\\", "/"), "a") as file:
    plcsim.log_parameters(mdlvar, file)
file.close
# plcsim.ClearAllTraces(mdlvar['scopes'])                                                    # clear all scopes.
plcsim.Set_sim_param()
plcsim.launch_sim(modelname=modelname)
# plcsim.HoldAllTraces(scopedict=mdlvar['scopes'])
# plcsim.saveAllTraces(mdlvar['scopes'],save_path)
#loop over csv files 
process.gen_plots(resFile= mdlvar['ToFile']['ToFile_path'], html_file=mdlvar['ToFile']['output_html'],open=True)
#?----------------------------------------------------------------------------------------------------------------------------------------






