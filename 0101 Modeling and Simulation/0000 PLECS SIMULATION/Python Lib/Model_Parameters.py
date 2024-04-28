
#?---------------------------------------------------------------------------------------------------------------------------------------- 
#?                                           ____  ____  ______   _    __
#?                                          / __ \/ __ )/ ____/  | |  / /___ ___________
#?                                         / / / / __  / /       | | / / __ `/ ___/ ___/
#?                                        / /_/ / /_/ / /___     | |/ / /_/ / /  (__  )
#?                                        \____/_____/\____/     |___/\__,_/_/  /____/
#?----------------------------------------------------------------------------------------------------------------------------------------
import os  
#?----------------------------------------------------------------------------------------------------------------------------------------
Sim_param 	=  {
                  'tSim'	    	   : 1.0, 
                  'maxStep'		   : 1e-3,  
                  'ZeroCross'       : 1000,
                  'idx'             : 0,
                  'rel_tol'		   : 1e-3 
               }
ToFile      =  {   #! change dir to generic later
                  'RES'		         : 'D:/4 WORKSPACE/24-OBC/OBC/0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Traces',                     
                  'ToFile_path'		: f'D:/4 WORKSPACE/24-OBC/OBC/0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/CSV/Results_{Sim_param['idx']}.csv',                     
                  'logfile'		   : f'D:/4 WORKSPACE/24-OBC/OBC/0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Log/log_{Sim_param['idx']}.log',                     
                  'Ts'              : 0,
                  'output_html'     : f'D:/4 WORKSPACE/24-OBC/OBC/0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/html/output_html{Sim_param['idx']}.html',
                           
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
				      "OBC/Scopes/PFC output busbar"                               
                           
               ]	
PFC_glb     =  {
                  'L'               :  300e-6,
                  'Rbusin'          :  1e-2,
                  'Rbusout'         :  1e-2,
                  'Cout'            :  {
                                             'Config'		      : 4,
                                             'Cap_s'    		   : 100e-6,  
                                             'Resr_s'		      : 19e-9,  
                                             'Lesl_s'		      : 1e-12,  
                                             'Npara'		      : 1,  
                                             'Nseri'		      : 1,  
                                             'Vinit'		      : 0,  
                                             'Iinit'		      : 0             
                                       },  
                  'VF'              :  500                                                         
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
                  'Lso'             : 0,
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
                  'Config'		      : 4,
                  'Cdc'    		   : 500e-6,  
                  'ESR'		         : 19e-9,
                  'ESL'		         : 1e-12, 
                  'nPara'		      : 6, 
                  'nSeri'		      : 1, 
                  'Vinit'		      : 0, 
                  'Iinit'		      : 0
               }
Load        =  {
                  'Config'		      : 2,  
                  'CL'    		      : 1e-6, 
                  'RL'		         : 40,  
                  'LL'		         : 0, 
                  'Vinit'		      : 0,  
                  'Iinit'		      : 0
               }
LLC         =  {
                  'R1'              : 4700/4,          
                  'R2'              : 160/24,          
                  'T_dt'            : 300e-9                          					
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
                  'Config'          :  4 ,
                  'Cin'             :  1e-9,  
                  'Lin'             :  1e-9,  
                  'Ro'              :  1e-9, 
                  'L_CMC'           :  1.5e-3, 
                  'L_DMC'           :  900e-6, 
                  'Cx'              :  0.1e-6,  
                  'Cy1'             :  4.7e-12, 
                  'Cy2'             :  4.7e-12,  
                  'Cd'              :  0,  
                  'Rd'              :  470e3
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
                  'Load'            :  Load,
                  'Thermals'        :Thermals                                                                                   
               }	
#?----------------------------------------------------------------------------------------------------------------------------------------	
Waveforms   =  [  
                  'Grid Voltage',
                  'Grid Current',

                  'EMI Filter Voltage',
                  'EMI Filter Current',

                  'PFC Input Voltage',

                  'PFC Input Current',

                  'PFC output voltage',

                  'PFC gates signal HS1',
                  'PFC gates signal HS2',
                  'PFC gates signal LS1',
                  'PFC gates signal LS2',

                  'PFC Input choke Voltage',
                  'PFC Input choke Current',

                  'PFC HS1 voltage',
                  'PFC Diode HS1 voltage',
                  'PFC HS2 voltage',
                  'PFC Diode HS2 voltage',
                  'PFC LS1 voltage',
                  'PFC Diode LS1 voltage',
                  'PFC LS2 voltage',
                  'PFC Diode LS2 voltage',

                  'PFC HS1 Current',
                  'PFC Diode HS1 Current',
                  'PFC HS2 Current',
                  'PFC Diode HS2 Current',
                  'PFC LS1 Current',
                  'PFC Diode LS1 Current',
                  'PFC LS2 Current',
                  'PFC Diode LS2 Current',

                  'PFC HS1 junction Temp',
                  'PFC Diode HS1 junction Temp',
                  'PFC HS2 junction Temp',
                  'PFC Diode HS2 junction Temp',
                  'PFC LS1 junction Temp',
                  'PFC Diode LS1 junction Temp',
                  'PFC LS2 junction Temp',
                  'PFC Diode LS2 junction Temp',

                  'PFC case Temp HS1',
                  'PFC case Temp HS2',
                  'PFC case Temp LS1',
                  'PFC case Temp LS2',

                  'PFC HS1 switching losses',
                  # 'PFC Diode HS1 switching losses',
                  'PFC HS2 switching losses',
                  # 'PFC Diode HS2 switching losses',
                  'PFC LS1 switching losses',
                  # 'PFC Diode LS1 switching losses',
                  'PFC LS2 switching losses',
                  # 'PFC Diode LS2 switching losses',

                  'PFC HS1 conduction losses',
                  'PFC Diode HS1 conduction losses',
                  'PFC HS2 conduction losses',
                  'PFC Diode HS2 conduction losses',
                  'PFC LS1 conduction losses',
                  'PFC Diode LS1 conduction losses',
                  'PFC LS2 conduction losses',
                  'PFC Diode LS2 conduction losses',

                  'PFC output capacitor voltage',
                  'PFC output capacitor current',
                  'PFC output capacitor dissipation',
                 
                  'PFC input busbar+ Resistor Voltage',
                  'PFC input busbar+ Resistor Current',
                  'PFC input busbar+ Resistor Dissipation',
                  'PFC input busbar- Resistor Voltage',
                  'PFC input busbar- Resistor Current',
                  'PFC input busbar- Resistor Dissipation',

                  'PFC output busbar+ Resistor Voltage',
                  'PFC output busbar+ Resistor Current',
                  'PFC output busbar+ Resistor Dissipation',
                  'PFC output busbar- Resistor Voltage',
                  'PFC output busbar- Resistor Current',
                  'PFC output busbar- Resistor Dissipation',

                  'DCLink Capacitor Voltage',
                  'DCLink Capacitor Current'
               ]		
#?----------------------------------------------------------------------------------------------------------------------------------------	

