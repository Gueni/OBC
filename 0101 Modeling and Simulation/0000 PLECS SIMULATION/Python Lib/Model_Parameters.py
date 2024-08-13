
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
utc_now             = datetime.now(timezone.utc)                                                            # []  - 
utc_numeric         = utc_now.strftime("%H%M%S")                                                            # []  - 
current_directory   = os.getcwd()                                                                           # []  - 
sim_idx             = 0                                                                                     # []  - 
Traces_path         = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Traces/"           # []  - 
ToFile_path         = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/CSV/"              # []  - 
logfile_path        = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Log/"              # []  - 
output_html_path    = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/html/"             # []  - 
model_path          = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Model/OBC.plecs"                  # []  - 
model_directory     = (os.path.join(current_directory, model_path)).replace("\\", "/")                      # []  -                   
#?----------------------------------------------------------------------------------------------------------------------------------------
Sim_param 	=  {                                                                                            #![]  - 
                  'tSim'	    	   : 0.4,                                                                  # []  - 
                  'tsave_i'	    	: 0.1,                                                                    # []  - 
                  'load_tflip'	   : 0.4 * 0.5,                                                            # []  -  
                  'maxStep'		   : 1e-3,                                                                 # []  - 
                  'ZeroCross'       : 1000,                                                                 # []  - 
                  'rel_tol'		   : 1e-7                                                                  # []  - 
               }
ToFile      =  {                                                                                            #![]  - 
                  'ToFile_path'		: (os.path.join(current_directory,                                      # []  - 
                   ToFile_path+f"Results_{utc_numeric}_{sim_idx}.csv")).replace("\\", "/"),                 # []  -                 
                  'logfile'		   : (os.path.join(current_directory,                                      # []  - 
                   logfile_path+f"Log_{utc_numeric}_{sim_idx}.log")).replace("\\", "/"),                    # []  -               
                  'output_html'     : (os.path.join(current_directory,                                      # []  - 
                   output_html_path+f"Html_{utc_numeric}_{sim_idx}.html")).replace("\\", "/"),              # []  - 
                  'Traces'		      : (os.path.join(current_directory,                                      # []  - 
                   Traces_path)).replace("\\", "/")  ,                                                      # []  - 
                  'Ts'              : 0,                                                                    # []  - 
                  'tsave' 	    	   : Sim_param['tSim']-Sim_param['tsave_i']                                # []  - 
               }  
scopes      =  [                                                                                            #![]  - 
				      "OBC/Scope",                                                                              # []  - 
				      "OBC/Scopes/grid_scope",                                                                  # []  - 
				      "OBC/Scopes/EMI_scope",                                                                   # []  -                          
				      "OBC/Scopes/DCLink_scope",                                                                # []  -                             
				      "OBC/Scopes/load_scope",                                                                  # []  -                          
				      "OBC/Scopes/PFC Input Voltage",                                                           # []  -                                 
				      "OBC/Scopes/PFC Input Current",                                                           # []  -                               
				      "OBC/Scopes/PFC output voltage",                                                          # []  -                              
				      "OBC/Scopes/PFC gates signal",                                                            # []  -                            
				      "OBC/Scopes/PFC Input choke",                                                             # []  -                           
				      "OBC/Scopes/PFC sw voltage",                                                              # []  -                        
				      "OBC/Scopes/PFC sw current",                                                              # []  -                        
				      "OBC/Scopes/PFC sw junction Temp",                                                        # []  -                            
				      "OBC/Scopes/'PFC case Temp",                                                              # []  -                      
				      "OBC/Scopes/PFC switching losses",                                                        # []  -                             
				      "OBC/Scopes/PFC conduction losses",                                                       # []  -                             
				      "OBC/Scopes/PFC output capacitor",                                                        # []  -                           
				      "OBC/Scopes/PFC input busbar",                                                            # []  -                         
				      "OBC/Scopes/PFC output busbar",                                                           # []  - 
                  "OBC/Scopes/PFC choke vs grid",                                                           # []  - 
                  "OBC/Scopes/grid vs filter",                                                              # []  - 
                  "OBC/Scopes/load_scope",                                                                  # []  -                
                  "OBC/Scopes/relays",                                                                      # []  -                
                  "OBC/Scopes/battery"                                                                      # []  -                

               ]	
PFC_glb     =  {                                                                                            #![]  - 
                  'L'               :  1.5e-3,                                                              # []  - 
                  'Rbusin'          :  0.001,                                                               # []  - 
                  'Rbusout'         :  0.001,                                                               # []  - 
                  'Cout'            :  {                                                                    # []  - 
                                             'Config'		      : 6,                                         # []  - 
                                             'Cap_s'    		   : 400e-6,                                    # []  - 
                                             'Resr_s'		      : 19e-9,                                     # []  - 
                                             'Lesl_s'		      : 1e-12,                                     # []  - 
                                             'Npara'		      : 1,                                         # []  - 
                                             'Nseri'		      : 1,                                         # []  - 
                                             'Vinit'		      : 0,                                         # []  - 
                                             'Iinit'		      : 0                                          # []  -        
                                       }                                                        
               }
PFC_SW      =  {                                                                                            #![]  - 
                  'Config'          : 1,                                                                    # []  - 
                  'therm_mosfet'    : 'file:C3M0021120K',                                                   # []  - 
                  'Rgon'            : 2.5,                                                                  # []  - 
                  'Rgoff'           : 2.5,                                                                  # []  - 
                  'Vdsmax'          : 1200,                                                                 # []  - 
                  'Idsmax'          : 100,                                                                  # []  - 
                  'Tjmax'           : 175,                                                                  # []  -                   
                  'Tjmin'           : -40,                                                                  # []  -                  
                  'TcDerating'      : [-55,27,45,70,95,108,120,132,145,158,170,175],                        # []  -         
                  'IdsMaxDerated'   : [100,100,95,86,77, 71, 65, 58, 49, 37, 20,  0],                       # []  -   
                  'ron_mosfet'      : 0.021,                                                                # []  - 
                  'Rds_off'         : 0,                                                                    # []  - 
                  'Iinit'           : 0,                                                                    # []  - 
                  'Coss'            : {                                                                     # []  -                        
                                          'Config'		      : 5,                                            # []  - 
                                          'Cap_s'    		   : 1e-12,                                        # []  - 
                                          'Resr_s'		      : 0,                                            # []  - 
                                          'Lesl_s'		      : 0,                                            # []  - 
                                          'Npara'		      : 1,                                            # []  - 
                                          'Nseri'		      : 1,                                            # []  - 
                                          'Vinit'		      : 0,                                            # []  - 
                                          'Iinit'		      : 0                                             # []  -       
                                          },                                                                # []  - 
                  'vblock'          : 0,                                                                    # []  - 
                  'Idrain'          : 0,                                                                    # []  - 
                  'Trise'           : 0,                                                                    # []  - 
                  'Tfall'           : 0,                                                                    # []  - 
                  'therm_body_diode': 'file:C3M0021120K_bodydiode',                                         # []  - 
                  'ron_body_diode'  : 0.033,                                                                # []  - 
                  'Rdb_off'         : 0,                                                                    # []  - 
                  'vf_body_diode'   : 2.3,                                                                  # []  - 
                  'BD_If'           : 0,                                                                    # []  - 
                  'T_reverse'       : 0,                                                                    # []  - 
                  'Q_reverse'       : 0,                                                                    # []  -      
                  'Ldr'             : 1e-12,                                                                # []  - 
                  'Ldr_Iinit'       : 0,                                                                    # []  - 
                  'Lso'             : 1e-12,                                                                # []  - 
                  'Lso_Iinit'       : 0,                                                                    # []  - 
                  'nPara'           : 0,                                                                    # []  - 
                  'T_init'          : 25,                                                                   # []  - 
                  'Tamb'            : 25,                                                                   # []  - 
                  't_init'          : 25,                                                                   # []  - 
                  'rth_sw'          : 0.09,                                                                 # []  - 
                  'rth_ch'          : 0.5,                                                                  # []  - 
                  'Rth'             : 0.34 	                                                               # []  - 				    	                           
               }
LLC_SW      =  {                                                                                            #![]  - 
                  'Config'          : 1,                                                                    # []  - 
                  'therm_mosfet'    : 'file:C3M0021120K',                                                   # []  - 
                  'Rgon'            : 2.5,                                                                  # []  - 
                  'Rgoff'           : 2.5,                                                                  # []  - 
                  'Vdsmax'          : 1200,                                                                 # []  - 
                  'Idsmax'          : 100,                                                                  # []  - 
                  'Tjmax'           : 175,                                                                  # []  -         
                  'Tjmin'           : -40,                                                                  # []  -               
                  'TcDerating'      : [-55,27,45,70,95,108,120,132,145,158,170,175],                        # []  -         
                  'IdsMaxDerated'   : [100,100,95,86,77, 71, 65, 58, 49, 37, 20,  0],                       # []  -  
                  'ron_mosfet'      : 0.021,                                                                # []  - 
                  'Rds_off'         : 0,                                                                    # []  - 
                  'Iinit'           : 0,                                                                    # []  - 
                  'Coss'            : {                                                                     # []  -                        
                                          'Config'		      : 1,                                            # []  - 
                                          'Cap_s'    		   : 1e-12,                                        # []  - 
                                          'Resr_s'		      : 0,                                            # []  - 
                                          'Lesl_s'		      : 0,                                            # []  - 
                                          'Npara'		      : 1,                                            # []  - 
                                          'Nseri'		      : 1,                                            # []  - 
                                          'Vinit'		      : 0,                                            # []  - 
                                          'Iinit'		      : 0                                             # []  -        
                                          },
                  'vblock'          : 0,                                                                    # []  - 
                  'Idrain'          : 0,                                                                    # []  - 
                  'Trise'           : 0,                                                                    # []  - 
                  'Tfall'           : 0,                                                                    # []  - 
                  'therm_body_diode': 'file:C3M0021120K_bodydiode',                                         # []  -  
                  'ron_body_diode'  : 0.033,                                                                # []  - 
                  'Rdb_off'         : 0,                                                                    # []  - 
                  'vf_body_diode'   : 2.3,                                                                  # []  - 
                  'BD_If'           : 0,                                                                    # []  - 
                  'T_reverse'       : 0,                                                                    # []  - 
                  'Q_reverse'       : 0,                                                                    # []  -             
                  'Ldr'             : 1e-12,                                                                # []  - 
                  'Ldr_Iinit'       : 0,                                                                    # []  - 
                  'Lso'             : 1e-12,                                                                # []  - 
                  'Lso_Iinit'       : 0,                                                                    # []  - 
                  'nPara'           : 0,                                                                    # []  - 
                  'T_init'          : 25,                                                                   # []  - 
                  'Tamb'            : 25,                                                                   # []  - 
                  't_init'          : 25,                                                                   # []  - 
                  'rth_sw'          : 0.09,                                                                 # []  - 
                  'rth_ch'          : 0.5,                                                                  # []  - 
                  'Rth'             : 0.34 			                                                         # []  - 		    	                           
               }
LLC_SR      =  {                                                                                            #![]  - 
                  'Config'          : 1,                                                                    # []  - 
                  'therm_mosfet'    : 'file:C3M0021120K',                                                   # []  -  
                  'Rgon'            : 2.5,                                                                  # []  - 
                  'Rgoff'           : 2.5,                                                                  # []  - 
                  'Vdsmax'          : 1200,                                                                 # []  - 
                  'Idsmax'          : 100,                                                                  # []  - 
                  'Tjmax'           : 175,                                                                  # []  -            
                  'Tjmin'           : -40,                                                                  # []  -   
                  'TcDerating'      : [-55,27,45,70,95,108,120,132,145,158,170,175],                        # []  -            
                  'IdsMaxDerated'   : [100,100,95,86,77, 71, 65, 58, 49, 37, 20,  0],                       # []  - 
                  'ron_mosfet'      : 0.021,                                                                # []  - 
                  'Rds_off'         : 0,                                                                    # []  - 
                  'Iinit'           : 0,                                                                    # []  - 
                  'Coss'            : {                                                                     # []  -                                            
                                          'Config'		      : 1,                                            # []  -   
                                          'Cap_s'    		   : 1e-12,                                        # []  - 
                                          'Resr_s'		      : 0,                                            # []  - 
                                          'Lesl_s'		      : 0,                                            # []  - 
                                          'Npara'		      : 1,                                            # []  - 
                                          'Nseri'		      : 1,                                            # []  - 
                                          'Vinit'		      : 0,                                            # []  - 
                                          'Iinit'		      : 0                                             # []  -           
                                          },                                                                # []  - 
                  'vblock'          : 0,                                                                    # []  - 
                  'Idrain'          : 0,                                                                    # []  - 
                  'Trise'           : 0,                                                                    # []  - 
                  'Tfall'           : 0,                                                                    # []  - 
                  'therm_body_diode': 'file:C3M0021120K_bodydiode',                                         # []  - 
                  'ron_body_diode'  : 0.033,                                                                # []  - 
                  'Rdb_off'         : 0,                                                                    # []  - 
                  'vf_body_diode'   : 2.3,                                                                  # []  - 
                  'BD_If'           : 0,                                                                    # []  - 
                  'T_reverse'       : 0,                                                                    # []  - 
                  'Q_reverse'       : 0,                                                                    # []  -     
                  'Ldr'             : 1e-12,                                                                # []  - 
                  'Ldr_Iinit'       : 0,                                                                    # []  - 
                  'Lso'             : 1e-12,                                                                # []  - 
                  'Lso_Iinit'       : 0,                                                                    # []  - 
                  'nPara'           : 0,                                                                    # []  - 
                  'T_init'          : 25,                                                                   # []  - 
                  'Tamb'            : 25,                                                                   # []  - 
                  't_init'          : 25,                                                                   # []  - 
                  'rth_sw'          : 0.09,                                                                 # []  - 
                  'rth_ch'          : 0.5,                                                                  # []  - 
                  'Rth'             : 0.34 			                                                         # []  - 		    	                           
               }
PFC         =  {                                                                                            #![]  - 
                  'Config'          :  1,                                                                   # []  - 
                  'HS1'             :  PFC_SW,                                                              # []  - 
                  'HS2'             :  PFC_SW,                                                              # []  -  
                  'LS1'             :  PFC_SW,                                                              # []  - 
                  'LS2'             :  PFC_SW                                                               # []  - 
               }	
CTRL_PFC    =  {                                                                                            #![]  - 
                  'Vref'    		   :  400,                                                                 # []  - 
                  'fs'    		      :  70e-3,                                                               # []  -  
                  'Ri_Kp'           :  0.1,                                                                 # []  - 
                  'Ri_Ki'           :  600,                                                                 # []  - 
                  'Rv_Kp'           :  5,                                                                   # []  - 
                  'Rv_Ki'           :  800                                                                  # []  - 
               }
DCLink      =  {                                                                                            #![]  - 
                  'Config'		      : 1,                                                                    # []  - 
                  'Cdc'    		   : 9*100e-6,                                                             # []  -  
                  'ESR'		         : 19e-9,                                                                # []  - 
                  'ESL'		         : 1e-19,                                                                # []  - 
                  'nPara'		      : 1,                                                                    # []  - 
                  'nSeri'		      : 1,                                                                    # []  - 
                  'Vinit'		      : 0,                                                                    # []  - 
                  'Iinit'		      : 1e-3                                                                     # []  - 
               }
Load        =  {                                                                                            #![]  - 
                  'Config'		      : 1,                                                                    # []  - 
                  'CL'    		      : 0,                                                                    # []  - 
                  'RL'		         : 40,                                                                   # []  - 
                  'LL'		         : 0,                                                                    # []  - 
                  'Vinit'		      : 0,                                                                    # []  - 
                  'Iinit'		      : 0,                                                                    # []  - 
                  't_switch'        : Sim_param['tSim']-Sim_param['load_tflip'],                            # []  - 
                  't_dead'          : (Sim_param['tSim']-Sim_param['load_tflip'])/2                         # []  - 
               }
RCSnub      =  {                                                                                            #![]  - 
                  'Config'		      : 1,                                                                    # []  - 
                  'Rsnub'           : 1e-3,                                                               # []  - 
                  'Csnub'           : {                                                                     # []  -               
                                          'Config'		      : 1,                                            # []  - 
                                          'Cap_s'    		   :  1e-3,                                      # []  - 
                                          'Resr_s'		      : 0,                                            # []  -           
                                          'Lesl_s'		      : 0,                                            # []  -       
                                          'Npara'		      : 1,                                            # []  -          
                                          'Nseri'		      : 1,                                            # []  -       
                                          'Vinit'		      : 0,                                            # []  -          
                                          'Iinit'		      : 0                                             # []  -                 
                                          }
               }
Diode       =  {
               
                  'diode'		         : 'file:C4D40120D',                                            # []     - diode thermal description       
                  'ron_diode'		      : 1,                                                           # [V]    - diode forward voltage    
                  'vf_diode'		      : 1.4,                                                         # [V]    - diode forward voltage
                  'rth_ch_diode'		   : 0.5,                                                         # [K/W]  - thermal resistance case-heatsink (grease)       
                  'num_par_diode'		: 4,                                                           # []     - Number of parallel diodes      
                  'Rth'		            : 0.1,                                                         # [K/W]  - Heatsink to ambient thermal resistance    
                  't_init'		         : 25                                                           # [C]    - initial temperature   
               }
LLC         =  {                                                                                            #![]  - 
                  'R1'              : 4700/4,                                                               # []  -         
                  'R2'              : 160/24,                                                               # []  - 
                  'V_DC'            : 200,                                                                  # [V] - DC voltage source.
                  'n_prim'          : 4,                                                                    # []  - primary side turn number.
                  'n_sndry'         : 4,                                                                    # []  - secondary side turn number.
                  'L_r'             : 1.55e-6,                                                              # [H] - resonant inductor.
                  'L_k'             : 1.55e-6,                                                              # [H] - resonant inductor.
                  'L_k_Iinit'       : 0,                                                                    # [H] - resonant inductor.
                  'L_r_Iinit'       : 0,                                                                    # []  - 
                  'Trafo'           : {                                                                     # []  -  
                                          'Config'		      : 1,                                            # []  - 
                                          'n_prim'    		: 4,                                            # []  - 
                                          'n_sndry'		   : 4,                                            # []  - 
                                          'Imaginit'		   : 0,                                            # []  - 
                                          'Lp'		         : 1e-9,                                         # []  - 
                                          'Rp'		         : 1e-2,                                         # []  - 
                                          'Rc'		         : 10,                                           # []  - 
                                          'Lm'		         : 1e-9,                                         # []  - 
                                          'Rs'		         : 10,                                           # []  - 
                                          'Ls'		         : 1e-9,                                         # []  -
                                          'LpIinit'		   : 0,                                            # []  - 
                                          'LmIinit'		   : 0,                                            # []  - 
                                          'LsIinit'		   : 0                                             # []  - 
 

                                      },
                  'C_r'             : {                                                                     # []  -  
                                          'Config'		      : 1,                                            # []  - 
                                          'Cap_s'    		   : 1.2e-6,                                       # []  - 
                                          'Resr_s'		      : 1e-10,                                            # []  - 
                                          'Lesl_s'		      : 1e-10,                                            # []  - 
                                          'Npara'		      : 1,                                            # []  - 
                                          'Nseri'		      : 1,                                            # []  - 
                                          'Vinit'		      : 0,                                            # []  - 
                                          'Iinit'		      : 0                                             # []  - 
                                          },
                  'L'               : 1.6e-6,                                                               # [H] - output inductor
                  'C_o'             : 480e-6,                                                               # [F] - output capacitor
                  'C_v_init'        : 0,                                                                    # [V] - output capacitor initial voltage
                  'R_o'             : 100,                                                                  # [Ohm] - output resistance       
                  'T_dt'            : 300e-9,                                                               # []  - 
                  'HS1'             :  LLC_SW,                                                              # []  -    
                  'HS2'             :  LLC_SW,                                                              # []  -    
                  'LS1'             :  LLC_SW,                                                              # []  -    
                  'LS2'             :  LLC_SW,                                                              # []  - 
                  'SRHS1'           :  LLC_SR,                                                              # []  -    
                  'SRHS2'           :  LLC_SR,                                                              # []  -    
                  'SRLS1'           :  LLC_SR,                                                              # []  -    
                  'SRLS2'           :  LLC_SR,                                                              # []  -   
                  'RC1'             :  RCSnub,                                                              # []  -    
                  'RC2'             :  RCSnub,                                                              # []  -    
                  'RC3'             :  RCSnub,                                                              # []  -    
                  'RC4'             :  RCSnub,                                                              # []  -    
                  'HS3'             :  Diode,                                                               # []  -    
                  'LS3'             :  Diode                                                                # []  -  
               }
LLC_CTRL    =  {                                                                                            #![]  - 
                  'Vref'    		   : 400 ,                                                                 # []  - 
                  'sys_clk'         : 100e6,	                                                               # [Hz] - 100 MHz
                  'max_period'      : 2000,                                                                 # Maximum system period allowed
                  'min_period'      : 200,	                                                               # Minimum system period allowed
                  'SlewStep'        : 0.25/3,                                                               # [V/ms] - slew rate
                  'StartUpInc'      : 100,                                                                  # [] - soft start frequency increment
                  'R1'              : 4700/4,                                                               # [Ohm] - sensing resistor
                  'R2'              : 160/24,                                                               # [Ohm] - sensing resistor
                  'C_sense'         : 10e-9,                                                                # [F] - sensing capacitor
                  'adc_conv'        : 15,                                                                   # [] - Number of system clock cycles required for ADC conversion
                  'T_dt'            : 300e-9                                                                # [s] - dead time
               }
Grid        =  {                                                                                            #![]  - 
                  'Config'          :  2,                                                                   # []  - 
                  'Vin'             :  230,                                                                 # []  - 
                  'Ts'              :  0,                                                                   # []  - 
                  'Fgrid'           :  50,                                                                  # []  - 
                  'Rg'              :  1e-2                                                                 # []  -                                                                                 
               }
Thermals    =  {                                                                                            #![]  - 
                  'T_amb'           :  25.0,                                                                # []  - 
                  'rth_Amb'         :  0.09                                                                 # []  - 
               }
HV_Filter   =  {                                                                                            #![]  - 
                  'Config'         :  2,                                                                    # []  - 
                  'Cy1'            : {                                                                      # []  -                       
                                          'Config'		      : 4,                                            # []  - 
                                          'Cap_s'    		   : 1e-3,                                         # []  - 
                                          'Resr_s'		      : 0,                                            # []  - 
                                          'Lesl_s'		      : 0,                                            # []  - 
                                          'Npara'		      : 1,                                            # []  - 
                                          'Nseri'		      : 1,                                            # []  - 
                                          'Vinit'		      : 0,                                            # []  - 
                                          'Iinit'		      : 0                                             # []  -           
                                          },                                                                # []  -
                  'Cy2'            : {                                                                      # []  -                       
                                          'Config'		      : 4,                                            # []  - 
                                          'Cap_s'    		   : 1e-3,                                         # []  - 
                                          'Resr_s'		      : 0,                                            # []  - 
                                          'Lesl_s'		      : 0,                                            # []  - 
                                          'Npara'		      : 1,                                            # []  - 
                                          'Nseri'		      : 1,                                            # []  - 
                                          'Vinit'		      : 0,                                            # []  - 
                                          'Iinit'		      : 0                                             # []  -           
                                          },                                                                # []  -
                  'Cx1'            : {                                                                      # []  -                       
                                          'Config'		      : 4,                                            # []  - 
                                          'Cap_s'    		   : 1e-3,                                         # []  - 
                                          'Resr_s'		      : 0,                                            # []  - 
                                          'Lesl_s'		      : 0,                                            # []  - 
                                          'Npara'		      : 1,                                            # []  - 
                                          'Nseri'		      : 1,                                            # []  - 
                                          'Vinit'		      : 0,                                            # []  - 
                                          'Iinit'		      : 0                                             # []  -           
                                          },                                                                # []  -
                  'Cx2'            : {                                                                      # []  -                       
                                          'Config'		      : 4,                                            # []  - 
                                          'Cap_s'    		   : 1e-3,                                         # []  - 
                                          'Resr_s'		      : 0,                                            # []  - 
                                          'Lesl_s'		      : 0,                                            # []  - 
                                          'Npara'		      : 1,                                            # []  - 
                                          'Nseri'		      : 1,                                            # []  - 
                                          'Vinit'		      : 0,                                            # []  - 
                                          'Iinit'		      : 0                                             # []  -           
                                          },                                                                # []  -
                  'Cx3'            : {                                                                      # []  -                       
                                          'Config'		      : 4,                                            # []  - 
                                          'Cap_s'    		   : 1e-3,                                         # []  - 
                                          'Resr_s'		      : 0,                                            # []  - 
                                          'Lesl_s'		      : 0,                                            # []  - 
                                          'Npara'		      : 1,                                            # []  - 
                                          'Nseri'		      : 1,                                            # []  - 
                                          'Vinit'		      : 0,                                            # []  - 
                                          'Iinit'		      : 0                                             # []  -           
                                          },                                                                # []  -
                  'Cx4'            : {                                                                      # []  -                       
                                          'Config'		      : 4,                                            # []  - 
                                          'Cap_s'    		   : 1e-3,                                         # []  - 
                                          'Resr_s'		      : 0,                                            # []  - 
                                          'Lesl_s'		      : 0,                                            # []  - 
                                          'Npara'		      : 1,                                            # []  - 
                                          'Nseri'		      : 1,                                            # []  - 
                                          'Vinit'		      : 0,                                            # []  - 
                                          'Iinit'		      : 0                                             # []  -           
                                          },                                                                # []  -
                  'Cx5'            : {                                                                      # []  -                       
                                          'Config'		      : 4,                                            # []  - 
                                          'Cap_s'    		   : 1e-3,                                         # []  - 
                                          'Resr_s'		      : 0,                                            # []  - 
                                          'Lesl_s'		      : 0,                                            # []  - 
                                          'Npara'		      : 1,                                            # []  - 
                                          'Nseri'		      : 1,                                            # []  - 
                                          'Vinit'		      : 0,                                            # []  - 
                                          'Iinit'		      : 0                                             # []  -           
                                          },                                                                # []  -
                  'L'              :  40e-6,                                                                # []  - 
                  'L_DMC'          :  900e-6                                                                # []  - 
            }
AC_Filter   =  {                                                                                            #![]  - 
                  'Config'          :  4 ,                                                                  # []  - 
                  'Cin'             :  1e-6,                                                                # []  - 
                  'L_CMC'           :  1.5e-3,                                                              # []  - 
                  'L_DMC'           :  900e-6,                                                              # []  - 
                  'Cx'              :  0.1e-6,                                                              # []  -    
                  'Cy1'             :  4.7e-12,                                                             # []  -    
                  'Cy2'             :  4.7e-12,                                                             # []  -    
                  'Ll'              :  10e-6                                                                # []  -    
               }
Battery     =  {  
                  'Config'                    : 2,                                                          # []  -         
                  'n_series'                  : 75,                                                         # []  -  number of series-connected cells
                  'n_parallel'                : 5,                                                          # []  -  number of parallel branches
                  'SOC_init'                  : 0.5,                                                        # []  -  initial SOC
                  'polarizingRshift'          : 0.10,                                                       # []  -  shift polarizing R by 10#
                  'cellNominalV'              : 2.9,                                                        # []  -  voltage at end of nominal zone
                  'cellFullChargeV'           : 3.3,                                                        # []  -  voltage at full SOC
                  'cellExponentialV'          : 3.05,                                                       # []  -  voltage at end of exponential zone
                  'cellRatedCapacity'         : 2.4,                                                        # []  -  cell rated capacity
                  'cellMaximumCapacity'       : 2.4,                                                        # []  -  cell maximum capacity
                  'cellNominalCapacity'       : 2.1,                                                        # []  -  cell capacity at end of nominal zone
                  'cellExponentialCapacity'   : 0.25,                                                       # []  -  cell capacity at end of exponential zone
                  'cellNominalDischargeI'     : 2.3,                                                        # []  -  nominal discharge current for cell
                  'cellInternalR'             : 6e-3,                                                       # []  -  internal cell resistance
                  'Rdis'                      : 0,                                                         # []  - 
                  'I_dc'                      : 0,                                                         # []  - 
                  'Rcell1'                    : 0,                                                         # []  - 
                  'Rcell2'                    : 0,                                                         # []  - 
                  'Ccell1'                    : 0,                                                       # []  - 
                  'Ccell2'                    : 0,                                                        # []  - 
                  'V_OC1'                     : 0,                                                          # []  - 
                  'Cdis'                      : {                                                           # []  -                                          
                                                'Config'		      : 1,                                      # []  - 
                                                'Cap_s'    		   : 0,                                   # []  - 
                                                'Resr_s'		      : 0,                                      # []  - 
                                                'Lesl_s'		      : 0,                                      # []  - 
                                                'Npara'		      : 1,                                      # []  - 
                                                'Nseri'		      : 1,                                      # []  - 
                                                'Vinit'		      : 0,                                      # []  - 
                                                'Iinit'		      : 0                                       # []  - 
                                                },                                                          # []  - 
                  'cellLPFTimeConstant'       : 30                                                          # []  - # 30 second time constant for LPF for effect of current on voltage
               }
#?----------------------------------------------------------------------------------------------------------------------------------------
ModelVars   =  {                                                                                            #![]  - 
                  'ToFile'          :  ToFile,                                                              # []  - 
                  'scopes'          :  scopes,                                                              # []  - 
                  'Sim_param'       :  Sim_param,                                                           # []  - 
                  'Grid'            :  Grid,                                                                # []  -    
                  'AC_Filter'       :  AC_Filter,                                                           # []  - 
                  'PFC_glb'         :  PFC_glb,                                                             # []  - 
                  'PFC'             :  PFC,                                                                 # []  - 
                  'CTRL_PFC'        :  CTRL_PFC,                                                            # []  - 
                  'DCLink'          :  DCLink,                                                              # []  - 
                  'LLC'             :  LLC,                                                                 # []  - 
                  'HV_Filter'       :  HV_Filter,                                                           # []  -  
                  'Battery'         :  Battery,                                                             # []  - 
                  'Load'            :  Load,                                                                # []  - 
                  'LLC_CTRL'        :  LLC_CTRL,                                                            # []  - 
                  'Thermals'        :  Thermals                                                             # []  -                                                                                
               }	
#?----------------------------------------------------------------------------------------------------------------------------------------	
Waveforms   =  [                                                                                            #![]  - 
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

