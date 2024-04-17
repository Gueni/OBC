
#?----------------------------------------------------------------------------------------------------------------------------------------
import pyplecs as plc
import Model_Parameters as mdl
import os  
import numpy as np 
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
L_CMC               = (np.arange(0.1    ,2    +0.1    ,0.1    )*1e-3).tolist()
L_DMC               = (np.arange(100    ,900  +50     ,50     )*1e-6).tolist()
Cx                  = (np.arange(0.1    ,2    +0.1    ,0.1    )*1e-6).tolist()
Cy1                 = (np.arange(1      ,10   +0.1    ,0.1    )*1e-9).tolist()
Cy2                 = (np.arange(0.1    ,2    +0.1    ,0.1    )*1e-9).tolist()
Cd                  = (np.arange(0      ,400  +100    ,100     )*1e-3).tolist()
Rd                  = (np.arange(1      ,500  +50     ,50     )*1e3 ).tolist()
#?----------------------------------------------------------------------------------------------------------------------------------------
plcsim              = plc.simpy(url=url , port=port , path=directory , modelvar=mdlvar)    # set a simpy object with all the needed vars.
plcsim.rpc_connect()                                                                       # Connect to plecs through the given url and port.
plcsim.load_model()                                                                        # load the plecs model.
#?----------------------------------------------------------------------------------------------------------------------------------------
# Define your original lists
L_CMC               = (np.arange(0.6, 1, 0.1) * 1e-3).tolist()
L_DMC               = (np.arange(500, 900, 100) * 1e-6).tolist()
Cx                  = (np.arange(0.6, 1, 0.1) * 1e-6).tolist()
Cy1                 = (np.arange(6, 10, 1) * 1e-9).tolist()
Cy2                 = (np.arange(6, 10, 1) * 1e-9).tolist()
Cd                  = (np.arange(0, 400, 100) * 1e-3).tolist()
Rd                  = (np.arange(0, 400, 100) * 1e3).tolist()
for i in range(len(L_CMC)):
    mdlvar['Sim_param']['idx']  = i
    mdlvar['L_CMC']  = L_CMC[i]
    mdlvar['L_DMC']  = L_DMC[i]
    mdlvar['Cx']     = Cx[i]
    mdlvar['Cy1']    = Cy1[i]
    mdlvar['Cy2']    = Cy2[i]
    mdlvar['Cd']     = Cd[i]
    mdlvar['Rd']     = Rd[i]
    with open(os.path.join(current_directory, log_file).replace("\\", "/"), "a") as file:
        plcsim.log_parameters(dict({'Simulation' : i}), file)
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






