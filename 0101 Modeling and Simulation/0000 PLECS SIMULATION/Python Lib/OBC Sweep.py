
#?----------------------------------------------------------------------------------------------------------------------------------------
#?                                         ____  ____  ______   ______       __________________ 
#?                                        / __ \/ __ )/ ____/  / ___/ |     / / ____/ ____/ __ \
#?                                       / / / / __  / /       \__ \| | /| / / __/ / __/ / /_/ /
#?                                      / /_/ / /_/ / /___    ___/ /| |/ |/ / /___/ /___/ ____/ 
#?                                      \____/_____/\____/   /____/ |__/|__/_____/_____/_/   
#?
#?----------------------------------------------------------------------------------------------------------------------------------------
import plecs as plc
import Model_Parameters as mdl
import numpy as np 
import post_process
#?----------------------------------------------------------------------------------------------------------------------------------------
port                = "1080"                                                               
url                 = f"http://localhost:{port}/RPC2"                                      
mdlvar              = mdl.ModelVars                                                        
modelname           = "OBC" 
L_CMC               = (np.arange(0.1    ,2    +0.1    ,0.1    )*1e-3).tolist()
plcsim              = plc.simpy(url=url , port=port , path=mdl.model_directory , modelvar=mdlvar)   
#?----------------------------------------------------------------------------------------------------------------------------------------
plcsim.rpc_connect()                                                                    
plcsim.load_model()
for i in range(len(L_CMC)):
    mdlvar['Sim_param']['idx']      = i
    mdlvar['AC_Filter']['L_CMC']    = L_CMC[i]
    plcsim.logParams(mdlvar['ToFile']['logfile'],mdlvar)
    # plcsim.ClearAllTraces(mdlvar['scopes'])     
    plcsim.Set_sim_param()
    plcsim.launch_sim(modelname=modelname)
    plcsim.HoldAllTraces(mdlvar['scopes'])
    plcsim.saveAllTraces(mdlvar['scopes'],mdl,mdlvar['ToFile']['Traces'])
post_process.gen_plots(resFile= mdlvar['ToFile']['ToFile_path'], html_file=mdlvar['ToFile']['output_html'],OPEN=True)
#?----------------------------------------------------------------------------------------------------------------------------------------






