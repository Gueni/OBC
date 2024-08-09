
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
import post_process
import cleardata
#?----------------------------------------------------------------------------------------------------------------------------------------
port                = "1080"                                                               
url                 = f"http://localhost:{port}/RPC2"                                      
mdlvar              = mdl.ModelVars                                                        
modelname           = "OBC"                                                                
#?----------------------------------------------------------------------------------------------------------------------------------------
plcsim              = plc.simpy(url=url , port=port , path=mdl.model_directory , modelvar=mdlvar)    
plcsim.rpc_connect()                                                                       
plcsim.load_model()  
cleardata.clear_data_folders()                                                                  
#?----------------------------------------------------------------------------------------------------------------------------------------
plcsim.logParams(str(mdlvar['ToFile']['logfile']),mdlvar)
plcsim.ClearAllTraces(mdlvar['scopes'])  
plcsim.Set_sim_param()
plcsim.launch_sim(modelname=modelname)
# plcsim.HoldAllTraces(mdlvar['scopes'])
# plcsim.saveAllTraces(mdlvar['scopes'],mdl,mdlvar['ToFile']['Traces'])
post_process.gen_plots(resFile= mdlvar['ToFile']['ToFile_path'], html_file=mdlvar['ToFile']['output_html'],OPEN=True)
#?----------------------------------------------------------------------------------------------------------------------------------------
