
#?---------------------------------------------------------------------------------------------------------------------------------------- 
#?                                           ____  ____  ______   _    __
#?                                          / __ \/ __ )/ ____/  | |  / /___ ___________
#?                                         / / / / __  / /       | | / / __ `/ ___/ ___/
#?                                        / /_/ / /_/ / /___     | |/ / /_/ / /  (__  )
#?                                        \____/_____/\____/     |___/\__,_/_/  /____/
#?----------------------------------------------------------------------------------------------------------------------------------------
import os 
from datetime import datetime, timezone
#?----------------------------------------------------------------------------------------------------------------------------------------
utc_now             = datetime.now(timezone.utc)
utc_numeric         = utc_now.strftime("%Y%m%d%H%M%S")
current_directory   = os.getcwd() 
sim_idx             = 0
Traces_path         = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Traces/" 
ToFile_path         = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/CSV/"
logfile_path        = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Log/"
output_html_path    = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/html/"
model_path          = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Model/OBC.plecs" 
model_directory     = (os.path.join(current_directory, model_path)).replace("\\", "/")                        
#?----------------------------------------------------------------------------------------------------------------------------------------
Sim_param 	=  {
                  'tSim'	    	   : 1, 
                  'tsave_i'	    	: 1, 
                  'load_tflip'	   : 0.5, 
                  'maxStep'		   : 1e-3,  
                  'ZeroCross'       : 1000,
                  'rel_tol'		   : 1e-3 
               }
ToFile      =  {   
                  'ToFile_path'		: (os.path.join(current_directory, ToFile_path+f"Results_{utc_numeric}_{sim_idx}.csv")).replace("\\", "/"),                     
                  'logfile'		   : (os.path.join(current_directory, logfile_path+f"Log_{utc_numeric}_{sim_idx}.log")).replace("\\", "/"),                     
                  'output_html'     : (os.path.join(current_directory, output_html_path+f"Html_{utc_numeric}_{sim_idx}.html")).replace("\\", "/"),
                  'Traces'		      : (os.path.join(current_directory, Traces_path)).replace("\\", "/")  ,                     
                  'Ts'              : 0,
                  'tsave' 	    	   : Sim_param['tSim']-Sim_param['tsave_i']     
               }  
scopes      =  [
				      "OBC/Scopes/grid_scope",     
				      "OBC/Scopes/EMI_scope",                                
				      "OBC/Scopes/DCLink_scope",                                
				      "OBC/Scopes/load_scope",                                
				      "OBC/Scopes/PFC Input Voltage",                                
				      "OBC/Scopes/PFC Input Current",                                
				      "OBC/Scopes/PFC output voltage",                                
				      "OBC/Scopes/PFC gates signal",                                
				      "OBC/Scopes/PFC Input choke",                                
				      "OBC/Scopes/PFC sw voltage",                                
				      "OBC/Scopes/PFC sw current",                                
				      "OBC/Scopes/PFC sw junction Temp",                                
				      "OBC/Scopes/'PFC case Temp",                                
				      "OBC/Scopes/PFC switching losses",                                
				      "OBC/Scopes/PFC conduction losses",                                
				      "OBC/Scopes/PFC output capacitor",                                
				      "OBC/Scopes/PFC input busbar",                                
				      "OBC/Scopes/PFC output busbar",
                  "OBC/Scopes/PFC choke vs grid",
                  "OBC/Scopes/grid vs filter",
                  "OBC/Scopes/Load_scope"                               
                           
               ]	
PFC_glb     =  {
                  'L'               :  40e-6,
                  'Rbusin'          :  1e-2,
                  'Rbusout'         :  1e-2,
                  'Cout'            :  {
                                             'Config'		      : 1,
                                             'Cap_s'    		   : 100e-6,  
                                             'Resr_s'		      : 19e-9,  
                                             'Lesl_s'		      : 1e-12,  
                                             'Npara'		      : 1,  
                                             'Nseri'		      : 1,  
                                             'Vinit'		      : 0,  
                                             'Iinit'		      : 0             
                                       }                                                        
               }
PFC_SW      =  {
                  'Config'          : 1, 
                  'therm_mosfet'    : 'file:C3M0021120K', 
                  'Rgon'            : 2.5,
                  'Rgoff'           : 2.5, 
                  'Vdsmax'          : 1200, 
                  'Idsmax'          : 100, 
                  'Tjmax'           : 175,                    
                  'Tjmin'           : -40,                   
                  'TcDerating'      : [-55,27,45,70,95,108,120,132,145,158,170,175],           
                  'IdsMaxDerated'   : [100,100,95,86,77, 71, 65, 58, 49, 37, 20,  0],     
                  'ron_mosfet'      : 0.021, 
                  'Rds_off'         : 0,
                  'Iinit'           : 0,
                  'Coss'            : {                                                    
                                          'Config'		      : 6,  
                                          'Cap_s'    		   : 1e-12,  
                                          'Resr_s'		      : 0,  
                                          'Lesl_s'		      : 0,  
                                          'Npara'		      : 1,  
                                          'Nseri'		      : 1,  
                                          'Vinit'		      : 0,  
                                          'Iinit'		      : 0             
                                          },
                  'vblock'          : 0,
                  'Idrain'          : 0,
                  'Trise'           : 0,
                  'Tfall'           : 0,
                  'therm_body_diode': 'file:C3M0021120K_bodydiode', 
                  'ron_body_diode'  : 0.033, 
                  'Rdb_off'         : 0,
                  'vf_body_diode'   : 2.3, 
                  'BD_If'           : 0,
                  'T_reverse'       : 0,
                  'Q_reverse'       : 0,            
                  'Ldr'             : 1e-12,
                  'Ldr_Iinit'       : 0,
                  'Lso'             : 1e-12,
                  'Lso_Iinit'       : 0,
                  'nPara'           : 0,
                  'T_init'          : 25,
                  'Tamb'            : 25, 
                  't_init'          : 25, 
                  'rth_sw'          : 0.09,
                  'rth_ch'          : 0.5, 
                  'Rth'             : 0.34 					    	                           
               }
LLC_SW      =  {
                  'Config'          : 1, 
                  'therm_mosfet'    : 'file:C3M0021120K', 
                  'Rgon'            : 2.5,
                  'Rgoff'           : 2.5, 
                  'Vdsmax'          : 1200, 
                  'Idsmax'          : 100, 
                  'Tjmax'           : 175,                    
                  'Tjmin'           : -40,                   
                  'TcDerating'      : [-55,27,45,70,95,108,120,132,145,158,170,175],           
                  'IdsMaxDerated'   : [100,100,95,86,77, 71, 65, 58, 49, 37, 20,  0],     
                  'ron_mosfet'      : 0.021, 
                  'Rds_off'         : 0,
                  'Iinit'           : 0,
                  'Coss'            : {                                                    
                                          'Config'		      : 6,  
                                          'Cap_s'    		   : 1e-12,  
                                          'Resr_s'		      : 0,  
                                          'Lesl_s'		      : 0,  
                                          'Npara'		      : 1,  
                                          'Nseri'		      : 1,  
                                          'Vinit'		      : 0,  
                                          'Iinit'		      : 0             
                                          },
                  'vblock'          : 0,
                  'Idrain'          : 0,
                  'Trise'           : 0,
                  'Tfall'           : 0,
                  'therm_body_diode': 'file:C3M0021120K_bodydiode', 
                  'ron_body_diode'  : 0.033, 
                  'Rdb_off'         : 0,
                  'vf_body_diode'   : 2.3, 
                  'BD_If'           : 0,
                  'T_reverse'       : 0,
                  'Q_reverse'       : 0,            
                  'Ldr'             : 1e-12,
                  'Ldr_Iinit'       : 0,
                  'Lso'             : 1e-12,
                  'Lso_Iinit'       : 0,
                  'nPara'           : 0,
                  'T_init'          : 25,
                  'Tamb'            : 25, 
                  't_init'          : 25, 
                  'rth_sw'          : 0.09,
                  'rth_ch'          : 0.5, 
                  'Rth'             : 0.34 					    	                           
               }
LLC_SR      =  {
                  'Config'          : 1, 
                  'therm_mosfet'    : 'file:C3M0021120K', 
                  'Rgon'            : 2.5,
                  'Rgoff'           : 2.5, 
                  'Vdsmax'          : 1200, 
                  'Idsmax'          : 100, 
                  'Tjmax'           : 175,                    
                  'Tjmin'           : -40,                   
                  'TcDerating'      : [-55,27,45,70,95,108,120,132,145,158,170,175],           
                  'IdsMaxDerated'   : [100,100,95,86,77, 71, 65, 58, 49, 37, 20,  0],     
                  'ron_mosfet'      : 0.021, 
                  'Rds_off'         : 0,
                  'Iinit'           : 0,
                  'Coss'            : {                                                    
                                          'Config'		      : 6,  
                                          'Cap_s'    		   : 1e-12,  
                                          'Resr_s'		      : 0,  
                                          'Lesl_s'		      : 0,  
                                          'Npara'		      : 1,  
                                          'Nseri'		      : 1,  
                                          'Vinit'		      : 0,  
                                          'Iinit'		      : 0             
                                          },
                  'vblock'          : 0,
                  'Idrain'          : 0,
                  'Trise'           : 0,
                  'Tfall'           : 0,
                  'therm_body_diode': 'file:C3M0021120K_bodydiode', 
                  'ron_body_diode'  : 0.033, 
                  'Rdb_off'         : 0,
                  'vf_body_diode'   : 2.3, 
                  'BD_If'           : 0,
                  'T_reverse'       : 0,
                  'Q_reverse'       : 0,            
                  'Ldr'             : 1e-12,
                  'Ldr_Iinit'       : 0,
                  'Lso'             : 1e-12,
                  'Lso_Iinit'       : 0,
                  'nPara'           : 0,
                  'T_init'          : 25,
                  'Tamb'            : 25, 
                  't_init'          : 25, 
                  'rth_sw'          : 0.09,
                  'rth_ch'          : 0.5, 
                  'Rth'             : 0.34 					    	                           
               }
PFC         =  {
                  'Config'          :  1,
                  'HS1'             :  PFC_SW,   
                  'HS2'             :  PFC_SW,   
                  'LS1'             :  PFC_SW,   
                  'LS2'             :  PFC_SW
               }	
CTRL_PFC    =  {
                  'Vref'    		   :  400,  
                  'fs'    		      :  70e-3,  
                  'Ri_Kp'           :  0.1,
                  'Ri_Ki'           :  600,
                  'Rv_Kp'           :  5,
                  'Rv_Ki'           :  800
               }
DCLink      =  {
                  'Config'		      : 1,
                  'Cdc'    		   : 500e-6,  
                  'ESR'		         : 19e-9,
                  'ESL'		         : 1e-12, 
                  'nPara'		      : 6, 
                  'nSeri'		      : 1, 
                  'Vinit'		      : 0, 
                  'Iinit'		      : 0
               }
Load        =  {
                  'Config'		      : 4,  
                  'CL'    		      : 0, 
                  'RL'		         : 40,  
                  'LL'		         : 0, 
                  'Vinit'		      : 0,  
                  'Iinit'		      : 0,
                  't_switch'        : Sim_param['tSim']-Sim_param['load_tflip']
               }
LLC         =  {
                  'R1'              : 4700/4,          
                  'R2'              : 160/24,          
                  'T_dt'            : 300e-9,
                  'HS1'             :  LLC_SW,   
                  'HS2'             :  LLC_SW,   
                  'LS1'             :  LLC_SW,   
                  'LS2'             :  LLC_SW,
                  'SRHS1'           :  LLC_SR,   
                  'SRHS2'           :  LLC_SR,   
                  'SRLS1'           :  LLC_SR,   
                  'SRLS2'           :  LLC_SR                          					
               }
Grid        =  {
                  'Config'          :  2,  
                  'Vin'             :  230,  
                  'Ts'              :  0,  
                  'Fgrid'           :  50,  
                  'Rg'              :  1e-3                                                                                  
               }
Thermals    =  {
                  'T_amb'           :  25.0,  
                  'rth_Amb'         :  0.09,  
               }
HV_Filter   =  {
                  'Config'         :  2,
                  'C_o'            : {                                                    
                                          'Config'		      : 6,  
                                          'Cap_s'    		   : 1e-3,  
                                          'Resr_s'		      : 0,  
                                          'Lesl_s'		      : 0,  
                                          'Npara'		      : 1,  
                                          'Nseri'		      : 1,  
                                          'Vinit'		      : 0,  
                                          'Iinit'		      : 0             
                                          },
                  'L'              :  40e-6

            }
AC_Filter   =  {
                  'Config'          :  1 ,
                  'Cin'             :  1e-6,  
                  'L_CMC'           :  1.5e-3, 
                  'L_DMC'           :  900e-6, 
                  'Cx'              :  0.1e-6,  
                  'Cy1'             :  4.7e-12, 
                  'Cy2'             :  4.7e-12,  
                  'Ll'              :  10e-6 
               }
Battery     =  {
                  'n_series'                  : 1, # number of series-connected cells
                  'n_parallel'                : 1, # number of parallel branches
                  'SOC_init'                  : 0, # initial SOC
                  'polarizingRshift'          : 0.10, # shift polarizing R by 10%
                  'cellNominalV'              : 2.9, # voltage at end of nominal zone
                  'cellFullChargeV'           : 400, # voltage at full SOC
                  'cellExponentialV'          : 390, # voltage at end of exponential zone
                  'cellRatedCapacity'         : 400, # cell rated capacity
                  'cellMaximumCapacity'       : 400, # cell maximum capacity
                  'cellNominalCapacity'       : 350, # cell capacity at end of nominal zone
                  'cellExponentialCapacity'   : 100, # cell capacity at end of exponential zone
                  'cellNominalDischargeI'     : 200, # nominal discharge current for cell
                  'cellInternalR'             : 20, # internal cell resistance
                  'Rdis'                      : 40,
                  'I_dc'                      : 6,
                  'Rcell1'                    : 6,
                  'Rcell2'                    : 6,
                  'Ccell1'                    : 6,
                  'Ccell2'                    : 6,
                  'V_OC1'                     : 300,
                  'Cdis'                      : {                                                    
                                                'Config'		      : 1,  
                                                'Cap_s'    		   : 1e-3,  
                                                'Resr_s'		      : 0,  
                                                'Lesl_s'		      : 0,  
                                                'Npara'		      : 1,  
                                                'Nseri'		      : 1,  
                                                'Vinit'		      : 0,  
                                                'Iinit'		      : 0             
                                                },
                  'cellLPFTimeConstant'       : 30 # 30 second time constant for LPF for effect of current on voltage
               }
#?----------------------------------------------------------------------------------------------------------------------------------------
ModelVars   =  {  
                  'ToFile'          :  ToFile,
                  'scopes'          :  scopes,  
                  'Sim_param'       :  Sim_param,  
                  'Grid'            :  Grid,  
                  'AC_Filter'       :  AC_Filter,
                  'PFC_glb'         :  PFC_glb, 
                  'PFC'             :  PFC, 
                  'CTRL_PFC'        :  CTRL_PFC,
                  'DCLink'          :  DCLink,  
                  'LLC'             :  LLC, 
                  'HV_Filter'       :  HV_Filter,   
                  'Battery'         :  Battery,
                  'Load'            :  Load,
                  'Thermals'        :Thermals                                                                                   
               }	
#?----------------------------------------------------------------------------------------------------------------------------------------	
Waveforms   =  [  
                  'Grid Voltage',
                  'Grid Current',
                  #?-------------------------
                  'EMI Filter Voltage',
                  'EMI Filter Current',
                  #?-------------------------
                  'PFC Input Voltage',
                  #?-------------------------
                  'PFC Input Current',
                  #?-------------------------
                  'PFC output voltage',
                  #?-------------------------
                  'PFC gates signal HS1',
                  'PFC gates signal HS2',
                  'PFC gates signal LS1',
                  'PFC gates signal LS2',
                  #?-------------------------
                  'PFC Input choke Voltage',
                  'PFC Input choke Current',
                  #?-------------------------
                  'PFC HS1 voltage',
                  'PFC Diode HS1 voltage',
                  'PFC HS2 voltage',
                  'PFC Diode HS2 voltage',
                  'PFC LS1 voltage',
                  'PFC Diode LS1 voltage',
                  'PFC LS2 voltage',
                  'PFC Diode LS2 voltage',
                  #?-------------------------
                  'PFC HS1 Current',
                  'PFC Diode HS1 Current',
                  'PFC HS2 Current',
                  'PFC Diode HS2 Current',
                  'PFC LS1 Current',
                  'PFC Diode LS1 Current',
                  'PFC LS2 Current',
                  'PFC Diode LS2 Current',
                  #?-------------------------
                  'PFC HS1 junction Temp',
                  'PFC Diode HS1 junction Temp',
                  'PFC HS2 junction Temp',
                  'PFC Diode HS2 junction Temp',
                  'PFC LS1 junction Temp',
                  'PFC Diode LS1 junction Temp',
                  'PFC LS2 junction Temp',
                  'PFC Diode LS2 junction Temp',
                  #?-------------------------
                  'PFC case Temp HS1',
                  'PFC case Temp HS2',
                  'PFC case Temp LS1',
                  'PFC case Temp LS2',
                  #?-------------------------
                  'PFC HS1 switching losses',
                  # 'PFC Diode HS1 switching losses',
                  'PFC HS2 switching losses',
                  # 'PFC Diode HS2 switching losses',
                  'PFC LS1 switching losses',
                  # 'PFC Diode LS1 switching losses',
                  'PFC LS2 switching losses',
                  # 'PFC Diode LS2 switching losses',
                  #?-------------------------
                  'PFC HS1 conduction losses',
                  'PFC Diode HS1 conduction losses',
                  'PFC HS2 conduction losses',
                  'PFC Diode HS2 conduction losses',
                  'PFC LS1 conduction losses',
                  'PFC Diode LS1 conduction losses',
                  'PFC LS2 conduction losses',
                  'PFC Diode LS2 conduction losses',
                  #?-------------------------
                  'PFC output capacitor voltage',
                  'PFC output capacitor current',
                  'PFC output capacitor dissipation',
                  #?-------------------------                 
                  'PFC input busbar+ Resistor Voltage',
                  'PFC input busbar+ Resistor Current',
                  'PFC input busbar+ Resistor Dissipation',
                  'PFC input busbar- Resistor Voltage',
                  'PFC input busbar- Resistor Current',
                  'PFC input busbar- Resistor Dissipation',
                  #?-------------------------
                  'PFC output busbar+ Resistor Voltage',
                  'PFC output busbar+ Resistor Current',
                  'PFC output busbar+ Resistor Dissipation',
                  'PFC output busbar- Resistor Voltage',
                  'PFC output busbar- Resistor Current',
                  'PFC output busbar- Resistor Dissipation',
                  #?-------------------------
                  'DCLink Capacitor Voltage',
                  'DCLink Capacitor Current',
                  #?-------------------------
                  'Battery Pack SOC',
                  'Battery Pack depleted charge [Ah]',
                  'Battery Pack Voltage [V]',
                  'Battery Pack Current [A]',
                  #?-------------------------
                  'Load Voltage',
                  'Load Current'
               ]		
#?----------------------------------------------------------------------------------------------------------------------------------------	



