
#!---------------------------------------------------------------------------------------------------------------------------------------- 
#!                                           ____  ____  ______   _    __
#!                                          / __ \/ __ )/ ____/  | |  / /___ ___________
#!                                         / / / / __  / /       | | / / __ `/ ___/ ___/
#!                                        / /_/ / /_/ / /___     | |/ / /_/ / /  (__  )
#!                                        \____/_____/\____/     |___/\__,_/_/  /____/
#!----------------------------------------------------------------------------------------------------------------------------------------
import os 
from datetime import datetime, timezone
#!----------------------------------------------------------------------------------------------------------------------------------------
utc_now             = datetime.now(timezone.utc)                                                            
utc_numeric         = utc_now.strftime("%H%M%S")                                                            
current_directory   = os.getcwd()                                                                           
sim_idx             = 0                                                                                     
Traces_path         = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Traces/"           
ToFile_path         = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/CSV/"              
logfile_path        = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Log/"              
<<<<<<< HEAD
output_html_path    = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/html/"
#!----------------------------------------------------------------------------------------------------------------------------------------
Sim_param 	= {                                                                                            
                  'tSim'	    	   : 20.0,                                                                                             #? [s]     - Total simulation time
                  'load_tflip'	   : 2.0/2,                                                                                           #? [s]     - Time at which the load changes state 
                  'maxStep'		   : 1e-3,                                                                                            #? [s]     - Maximum simulation time step
                  'ZeroCross'       : 1000,                                                                                            #? [/]     - Zero-crossing detection limit
                  'rel_tol'		   : 1e-7                                                                                             #? [/]     - Relative tolerance for the numerical solver
=======
output_html_path    = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/html/"             
model_path          = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Model/OBC.plecs"                  
model_directory     = (os.path.join(current_directory, model_path)).replace("\\", "/")                                        
#!----------------------------------------------------------------------------------------------------------------------------------------
Sim_param 	= {                                                                                             
                  'tSim'	    	   : 0.4,                                                                  #? [s]     - 
                  'tsave_i'	    	: 0.01,                                                                  #? [s]     - 
                  'load_tflip'	   : 0.04 * 0.5,                                                            #? [s]     -  
                  'maxStep'		   : 1e-3,                                                                  #? [/]     - 
                  'ZeroCross'       : 1000,                                                                  #? [/]     - 
                  'rel_tol'		   : 1e-7                                                                   #? [/]     - 
>>>>>>> parent of 1b0789f (merging changes for back up (#30))
               }
ToFile      = {                                                                                             
                  'ToFile_path'		: (os.path.join(current_directory,                                      #? [/]      - 
                   ToFile_path+f"Results_{utc_numeric}_{sim_idx}.csv")).replace("\\", "/"),                                 
                  'logfile'		   : (os.path.join(current_directory,                                      #? [/]      - 
                   logfile_path+f"Log_{utc_numeric}_{sim_idx}.log")).replace("\\", "/"),                                 
                  'output_html'     : (os.path.join(current_directory,                                      #? [/]      - 
                   output_html_path+f"Html_{utc_numeric}_{sim_idx}.html")).replace("\\", "/"),              
                  'Traces'		      : (os.path.join(current_directory,                                      #? [/]      - 
                   Traces_path)).replace("\\", "/")  ,                                                      
                  'Ts'              : 0,                                                                    #? [s]      - 
                  'tsave' 	    	   : Sim_param['tSim']-Sim_param['tsave_i']                                #? [s]      - 
               }  
PFC_glb     = {                                                                                             
                  'L'               :  1.5e-3,                                                              #? [H]      - 
                  'Rbusin'          :  0.001,                                                               #? [Ohm]    - 
                  'Rbusout'         :  0.001,                                                               #? [Ohm]    - 
                  'Cout'            :  {                                                                     
                                             'Config'		      : 6,                                         #? [/]      - 
                                             'Cap_s'    		   : 400e-6,                                    #? [/]      - 
                                             'Resr_s'		      : 19e-9,                                     #? [Ohm]    -
                                             'Lesl_s'		      : 1e-12,                                     #? [/]      - 
                                             'Npara'		      : 1,                                         #? [/]      - 
                                             'Nseri'		      : 1,                                         #? [/]      - 
                                             'Vinit'		      : 0,                                         #? [/]      - 
                                             'Iinit'		      : 0                                          #? [/]      -        
                                       }                                                      
               }
PFC_SW      = {                                                                                             
                  'Config'          : 1,                                                                    #? [/]      - 
                  'therm_mosfet'    : 'file:C3M0021120K',                                                   #? [/]      - 
                  'Rgon'            : 2.5,                                                                  #? [Ohm]    - 
                  'Rgoff'           : 2.5,                                                                  #? [Ohm]    - 
                  'Vdsmax'          : 1200,                                                                 #? [/]      - 
                  'Idsmax'          : 100,                                                                  #? [/]      - 
                  'Tjmax'           : 175,                                                                  #? [/]      -                   
                  'Tjmin'           : -40,                                                                  #? [/]      -                  
                  'TcDerating'      : [-55,27,45,70,95,108,120,132,145,158,170,175],                        #? [/]      -         
                  'IdsMaxDerated'   : [100,100,95,86,77, 71, 65, 58, 49, 37, 20,  0],                       #? [/]      -   
                  'ron_mosfet'      : 0.021,                                                                #? [Ohm]    - 
                  'Rds_off'         : 0,                                                                    #? [Ohm]    - 
                  'Iinit'           : 0,                                                                    #? [/]      - 
                  'Coss'            :  {                                                                                           
                                          'Config'		      : 5,                                            #? [/]      - 
                                          'Cap_s'    		   : 1e-12,                                        #? [/]      - 
                                          'Resr_s'		      : 0,                                            #? [Ohm]    - 
                                          'Lesl_s'		      : 0,                                            #? [/]      - 
                                          'Npara'		      : 1,                                            #? [/]      - 
                                          'Nseri'		      : 1,                                            #? [/]      - 
                                          'Vinit'		      : 0,                                            #? [/]      - 
                                          'Iinit'		      : 0                                             #? [/]      -       
                                          },                                                               
                  'vblock'          : 0,                                                                    #? [/]      - 
                  'Idrain'          : 0,                                                                    #? [/]      - 
                  'Trise'           : 0,                                                                    #? [/]      - 
                  'Tfall'           : 0,                                                                    #? [/]      - 
                  'therm_body_diode': 'file:C3M0021120K_bodydiode',                                         #? [/]      - 
                  'ron_body_diode'  : 0.033,                                                                #? [Ohm]    - 
                  'Rdb_off'         : 0,                                                                    #? [Ohm]    - 
                  'vf_body_diode'   : 2.3,                                                                  #? [/]      - 
                  'BD_If'           : 0,                                                                    #? [/]      - 
                  'T_reverse'       : 0,                                                                    #? [/]      - 
                  'Q_reverse'       : 0,                                                                    #? [/]      -      
                  'Ldr'             : 1e-12,                                                                #? [/]      - 
                  'Ldr_Iinit'       : 0,                                                                    #? [/]      - 
                  'Lso'             : 1e-12,                                                                #? [/]      - 
                  'Lso_Iinit'       : 0,                                                                    #? [/]      - 
                  'nPara'           : 0,                                                                    #? [/]      - 
                  'T_init'          : 25,                                                                   #? [/]      - 
                  'Tamb'            : 25,                                                                   #? [/]      - 
                  't_init'          : 25,                                                                   #? [/]      - 
                  'rth_sw'          : 0.09,                                                                 #? [/]      - 
                  'rth_ch'          : 0.5,                                                                  #? [/]      - 
                  'Rth'             : 0.34 	                                                               #? [/]      - 				    	                           
               }
LLC_SW      = {                                                                                             
                  'Config'          : 1,                                                                    #? [/]      - 
                  'therm_mosfet'    : 'file:C3M0021120K',                                                   #? [/]      - 
                  'Rgon'            : 2.5,                                                                  #? [Ohm]    - 
                  'Rgoff'           : 2.5,                                                                  #? [Ohm]    - 
                  'Vdsmax'          : 1200,                                                                 #? [/]      - 
                  'Idsmax'          : 100,                                                                  #? [/]      - 
                  'Tjmax'           : 175,                                                                  #? [/]      -         
                  'Tjmin'           : -40,                                                                  #? [/]      -               
                  'TcDerating'      : [-55,27,45,70,95,108,120,132,145,158,170,175],                        #? [/]      -         
                  'IdsMaxDerated'   : [100,100,95,86,77, 71, 65, 58, 49, 37, 20,  0],                       #? [/]      -  
                  'ron_mosfet'      : 0.021,                                                                #? [Ohm]    -
                  'Rds_off'         : 0,                                                                    #? [Ohm]    - 
                  'Iinit'           : 0,                                                                    #? [/]      - 
                  'Coss'            :  {                                                                                            
                                          'Config'		      : 1,                                            #? [/]      - 
                                          'Cap_s'    		   : 1e-12,                                        #? [/]      - 
                                          'Resr_s'		      : 0,                                            #? [Ohm]    -
                                          'Lesl_s'		      : 0,                                            #? [/]      - 
                                          'Npara'		      : 1,                                            #? [/]      - 
                                          'Nseri'		      : 1,                                            #? [/]      - 
                                          'Vinit'		      : 0,                                            #? [/]      - 
                                          'Iinit'		      : 0                                             #? [/]      -        
                                          },
                  'vblock'          : 0,                                                                    #? [/]      - 
                  'Idrain'          : 0,                                                                    #? [/]      - 
                  'Trise'           : 0,                                                                    #? [/]      - 
                  'Tfall'           : 0,                                                                    #? [/]      - 
                  'therm_body_diode': 'file:C3M0021120K_bodydiode',                                         #? [/]      -  
                  'ron_body_diode'  : 0.033,                                                                #? [Ohm]    -
                  'Rdb_off'         : 0,                                                                    #? [Ohm]    - 
                  'vf_body_diode'   : 2.3,                                                                  #? [/]      - 
                  'BD_If'           : 0,                                                                    #? [/]      - 
                  'T_reverse'       : 0,                                                                    #? [/]      - 
                  'Q_reverse'       : 0,                                                                    #? [/]      -             
                  'Ldr'             : 1e-12,                                                                #? [/]      - 
                  'Ldr_Iinit'       : 0,                                                                    #? [/]      - 
                  'Lso'             : 1e-12,                                                                #? [/]      - 
                  'Lso_Iinit'       : 0,                                                                    #? [/]      - 
                  'nPara'           : 0,                                                                    #? [/]      - 
                  'T_init'          : 25,                                                                   #? [/]      - 
                  'Tamb'            : 25,                                                                   #? [/]      - 
                  't_init'          : 25,                                                                   #? [/]      - 
                  'rth_sw'          : 0.09,                                                                 #? [/]      - 
                  'rth_ch'          : 0.5,                                                                  #? [/]      - 
                  'Rth'             : 0.34 			                                                         #? [/]      - 		    	                           
               }
<<<<<<< HEAD
PFC         = {
                  'Config'          : 1,                                                                                               #? [/]      - Diode thermal description
                  'Choke'           : {
                     'Config'       : 1,                                                                                               #? [/]      - Diode thermal description
                     'L1'           : 15e-6,                                                                                          #? [H]      - Inductance of the first choke winding
                     'L2'           : 15e-6,                                                                                          #? [H]      - Inductance of the second choke winding
                     'R1'           : 0.01,                                                                                            #? [Ohm]    - Resistance of the first choke winding
                     'R2'           : 0.01,                                                                                            #? [Ohm]    - Resistance of the second choke winding
                     'Lm'           : 0.001,                                                                                           #? [H]      - Mutual inductance of the choke
                     'Rm'           : 0.001,                                                                                           #? [Ohm]    - Resistance of the mutual inductance
                     'i1'           : 0,                                                                                               #? [A]      - Initial current in the first choke winding
                     'i2'           : 0                                                                                                #? [A]      - Initial current in the second choke winding
                  },
                  'Cout'            : 100e-6,                                                                                          #? [V]      - Input voltage of the grid
                  'SW'              : {
                     'Config'       : 1,                                                                                               #? [/]      - Switch configuration
                     'therm_mosfet' : 'file:C3M0021120K',                                                                              #? [/]      - MOSFET thermal model file path
                     'Rgon'         : 2.5,                                                                                             #? [Ohm]    - Gate resistance for turn-on
                     'Rgoff'        : 2.5,                                                                                             #? [Ohm]    - Gate resistance for turn-off
                     'ron_mosfet'   : 20e-3,                                                                                           #? [Ohm]    - MOSFET on-state resistance
                     'Iinit'        : 0,                                                                                               #? [A]      - Initial current through the MOSFET
                     'Coss'         : {
                           'Config' : 5,                                                                                               #? [/]      - Capacitance configuration
                           'Cap_s'  : 197e-12,                                                                                         #? [F]      - Capacitance value
                           'Resr_s' : 1e-12,                                                                                           #? [Ohm]    - Equivalent series resistance of the capacitance
                           'Lesl_s' : 1e-12,                                                                                           #? [H]      - Equivalent series inductance of the capacitance
                           'Npara'  : 1,                                                                                               #? [/]      - Number of parallel capacitors
                           'Nseri'  : 1,                                                                                               #? [/]      - Number of series capacitors
                           'Vinit'  : 0,                                                                                               #? [V]      - Initial voltage across the capacitance
                           'Iinit'  : 0                                                                                                #? [A]      - Initial current through the capacitance
                     },
                     'therm_body_diode': 'file:C3M0021120K_bodydiode',                                                                 #? [/]      - Body diode thermal model file path
                     'ron_body_diode'  : 5e-3,                                                                                         #? [Ohm]    - Body diode on-state resistance
                     'Rdb_off'         : 0,                                                                                            #? [Ohm]    - Resistance when the body diode is off
                     'vf_body_diode'   : 0.6,                                                                                          #? [V]      - Body diode forward voltage
                     'nPara'           : 1,                                                                                            #? [/]      - Number of parallel MOSFETs
                     'T_init'          : 25,                                                                                           #? [°C]     - Initial temperature of the MOSFET
                     'Tamb'            : 25,                                                                                           #? [°C]     - Ambient temperature
                     't_init'          : 25,                                                                                           #? [s]      - Initial time for thermal calculations
                     'rth_sw'          : 0,                                                                                         #? [K/W]    - Thermal resistance between the switch junction and case
                     'rth_ch'          : 0,                                                                                         #? [K/W]    - Thermal resistance between the case and heatsink
                     'Rth'             : 0                                                                                          #? [K/W]    - Total thermal resistance
                  }
=======
LLC_SR      = {                                                                                             
                  'Config'          : 1,                                                                    #? [/]      - 
                  'therm_mosfet'    : 'file:C3M0021120K',                                                   #? [/]      -  
                  'Rgon'            : 2.5,                                                                  #? [Ohm]    - 
                  'Rgoff'           : 2.5,                                                                  #? [Ohm]    - 
                  'Vdsmax'          : 1200,                                                                 #? [/]      - 
                  'Idsmax'          : 100,                                                                  #? [/]      - 
                  'Tjmax'           : 175,                                                                  #? [/]      -            
                  'Tjmin'           : -40,                                                                  #? [/]      -   
                  'TcDerating'      : [-55,27,45,70,95,108,120,132,145,158,170,175],                        #? [/]      -            
                  'IdsMaxDerated'   : [100,100,95,86,77, 71, 65, 58, 49, 37, 20,  0],                       #? [/]      - 
                  'ron_mosfet'      : 0.021,                                                                #? [Ohm]    - 
                  'Rds_off'         : 0,                                                                    #? [Ohm]    - 
                  'Iinit'           : 0,                                                                    #? [/]      - 
                  'Coss'            :  {                                                                                                         
                                          'Config'		      : 1,                                            #? [/]      -   
                                          'Cap_s'    		   : 1e-12,                                        #? [/]      - 
                                          'Resr_s'		      : 0,                                            #? [Ohm]    - 
                                          'Lesl_s'		      : 0,                                            #? [/]      - 
                                          'Npara'		      : 1,                                            #? [/]      - 
                                          'Nseri'		      : 1,                                            #? [/]      - 
                                          'Vinit'		      : 0,                                            #? [/]      - 
                                          'Iinit'		      : 0                                             #? [/]      -           
                                          },                                                                #? [/]      - 
                  'vblock'          : 0,                                                                    #? [/]      - 
                  'Idrain'          : 0,                                                                    #? [/]      - 
                  'Trise'           : 0,                                                                    #? [/]      - 
                  'Tfall'           : 0,                                                                    #? [/]      - 
                  'therm_body_diode': 'file:C3M0021120K_bodydiode',                                         #? [/]      - 
                  'ron_body_diode'  : 0.033,                                                                #? [Ohm]    - 
                  'Rdb_off'         : 0,                                                                    #? [Ohm]    - 
                  'vf_body_diode'   : 2.3,                                                                  #? [/]      - 
                  'BD_If'           : 0,                                                                    #? [/]      - 
                  'T_reverse'       : 0,                                                                    #? [/]      - 
                  'Q_reverse'       : 0,                                                                    #? [/]      -     
                  'Ldr'             : 1e-12,                                                                #? [/]      - 
                  'Ldr_Iinit'       : 0,                                                                    #? [/]      - 
                  'Lso'             : 1e-12,                                                                #? [/]      - 
                  'Lso_Iinit'       : 0,                                                                    #? [/]      - 
                  'nPara'           : 0,                                                                    #? [/]      - 
                  'T_init'          : 25,                                                                   #? [/]      - 
                  'Tamb'            : 25,                                                                   #? [/]      - 
                  't_init'          : 25,                                                                   #? [/]      - 
                  'rth_sw'          : 0.09,                                                                 #? [/]      - 
                  'rth_ch'          : 0.5,                                                                  #? [/]      - 
                  'Rth'             : 0.34 			                                                         #? [/]      - 		    	                           
               }
PFC         = {                                                                                             
                  'Config'          :  1,                                                                    
                  'HS1'             :  PFC_SW,                                                               
                  'HS2'             :  PFC_SW,                                                                
                  'LS1'             :  PFC_SW,                                                               
                  'LS2'             :  PFC_SW,
                  'diode'		      : 'file:C4D40120D',                                                     #? [/]      - diode thermal description       
                  'ron_diode'		   : 1,                                                                    #? [Ohm]    - diode forward voltage    
                  'vf_diode'		   : 1.4,                                                                  #? [V]      - diode forward voltage
                  'rth_ch_diode'		: 0.5,                                                                  #? [K/W]    - thermal resistance case-heatsink (grease)       
                  'num_par_diode'   : 4,                                                                    #? [/]      - Number of parallel diodes      
                  'Rth'		         : 0.1,                                                                  #? [K/W]    - Heatsink to ambient thermal resistance    
                  't_init'		      : 25                                                                    #? [C]      - initial temperature   
                                                                                                  
               }	
CTRL_PFC    = {                                                                                             
                  'Vref'    		   :  400,                                                                 #? [/]      - 
                  'fs'    		      :  70e-3,                                                               #? [/]      -  
                  'Ri_Kp'           :  0.1,                                                                 #? [/]      - 
                  'Ri_Ki'           :  600,                                                                 #? [/]      - 
                  'Rv_Kp'           :  5,                                                                   #? [/]      - 
                  'Rv_Ki'           :  800                                                                  #? [/]      - 
>>>>>>> parent of 1b0789f (merging changes for back up (#30))
               }
DCLink      = {                                                                                             
<<<<<<< HEAD
                  'Config'		      : 1,                                                                    #? [/]      - 
                  'Cdc'    		   : 100e-6,                                                               #? [/]      -  
                  'ESR'		         : 19e-9,                                                                #? [Ohm]    - 
                  'ESL'		         : 1e-19,                                                                #? [/]      - 
                  'nPara'		      : 6,                                                                    #? [/]      - 
                  'nSeri'		      : 1,                                                                    #? [/]      - 
                  'Vinit'		      : 0,                                                                    #? [/]      - 
                  'Iinit'		      : 1e-3                                                                  #? [/]      - 
               }
Load        = {                                                                                             
                  'Config'		      : 1,                                                                    #? [/]      - 
                  'CL'    		      : 0,                                                                    #? [/]      - 
                  'RL'		         : 50,                                                                   #? [Ohm]    -
                  'LL'		         : 0,                                                                    #? [/]      - 
                  'Vinit'		      : 0,                                                                    #? [/]      - 
                  'Iinit'		      : 0,                                                                    #? [/]      - 
                  't_switch'        : Sim_param['tSim']-Sim_param['load_tflip'],                            #? [/]      - 
                  't_dead'          : (Sim_param['tSim']-Sim_param['load_tflip'])/2                         #? [/]      - 
               }
RCSnub      = {                                                                                             
                  'Config'		      : 1,                                                                    #? [/]      - 
                  'Rsnub'           : 1e-3,                                                                 #? [Ohm]    - 
                  'Csnub'           :  {                                                                                
                                          'Config'		      : 1,                                            #? [/]      - 
                                          'Cap_s'    		   :  1e-3,                                        #? [/]      - 
                                          'Resr_s'		      : 0,                                            #? [Ohm]    -           
                                          'Lesl_s'		      : 0,                                            #? [/]      -       
                                          'Npara'		      : 1,                                            #? [/]      -          
                                          'Nseri'		      : 1,                                            #? [/]      -       
                                          'Vinit'		      : 0,                                            #? [/]      -          
                                          'Iinit'		      : 0                                             #? [/]      -                 
                                          }
               }
Diode       = {
                  'diode'		         : 'file:C4D40120D',                                                  #? [/]      - diode thermal description       
                  'ron_diode'		      : 1,                                                                 #? [Ohm]    - diode forward voltage    
                  'vf_diode'		      : 1.4,                                                               #? [V]      - diode forward voltage
                  'rth_ch_diode'		   : 0.5,                                                               #? [K/W]    - thermal resistance case-heatsink (grease)       
                  'num_par_diode'		: 4,                                                                 #? [/]      - Number of parallel diodes      
                  'Rth'		            : 0.1,                                                               #? [K/W]    - Heatsink to ambient thermal resistance    
                  't_init'		         : 25                                                                 #? [C]      - initial temperature   
               }
LLC         = {                                                                                             
                  'R1'              : 4700/4,                                                               #? [Ohm]    -         
                  'R2'              : 160/24,                                                               #? [Ohm]    - 
                  'V_DC'            : 200,                                                                  #? [V]      - DC voltage source.
                  'n_prim'          : 4,                                                                    #? [/]      - primary side turn number.
                  'n_sndry'         : 4,                                                                    #? [/]      - secondary side turn number.
                  'L_r'             : 1.55e-6,                                                              #? [H]      - resonant inductor.
                  'L_k'             : 1.55e-6,                                                              #? [H]      - resonant inductor.
                  'L_k_Iinit'       : 0,                                                                    #? [H]      - resonant inductor.
                  'L_r_Iinit'       : 0,                                                                    #? [/]      - 
                  'Trafo'           :  {                                                                  
                                          'Config'		      : 1,                                            #? [/]      - 
                                          'n_prim'    		: 4,                                            #? [/]      - 
                                          'n_sndry'		   : 4,                                            #? [/]      - 
                                          'Imaginit'		   : 0,                                            #? [/]      - 
                                          'Lp'		         : 1e-9,                                         #? [/]      - 
                                          'Rp'		         : 1e-2,                                         #? [Ohm]    - 
                                          'Rc'		         : 10,                                           #? [Ohm]    - 
                                          'Lm'		         : 1e-9,                                         #? [/]      - 
                                          'Rs'		         : 10,                                           #? [/]      - 
                                          'Ls'		         : 1e-9,                                         #? [/]      -
                                          'LpIinit'		   : 0,                                            #? [/]      - 
                                          'LmIinit'		   : 0,                                            #? [/]      - 
                                          'LsIinit'		   : 0                                             #? [/]      - 
                                      },
                  'C_r'             :  {                                                                 
                                          'Config'		      : 1,                                            #? [/]      - 
                                          'Cap_s'    		   : 1.2e-6,                                       #? [/]      - 
                                          'Resr_s'		      : 1e-10,                                        #? [Ohm]    - 
                                          'Lesl_s'		      : 1e-10,                                        #? [/]      - 
                                          'Npara'		      : 1,                                            #? [/]      - 
                                          'Nseri'		      : 1,                                            #? [/]      - 
                                          'Vinit'		      : 0,                                            #? [/]      - 
                                          'Iinit'		      : 0                                             #? [/]      - 
                                          },
                  'L'               : 1.6e-6,                                                               #? [H]      - output inductor
                  'C_o'             : 480e-6,                                                               #? [F]      - output capacitor
                  'C_v_init'        : 0,                                                                    #? [V]      - output capacitor initial voltage
                  'R_o'             : 100,                                                                  #? [Ohm]    - output resistance       
                  'T_dt'            : 300e-9,                                                               #? [/]      -
                  'HS1'             :  LLC_SW,                                                                 
                  'HS2'             :  LLC_SW,                                                                 
                  'LS1'             :  LLC_SW,                                                                 
                  'LS2'             :  LLC_SW,                                                              
                  'SRHS1'           :  LLC_SR,                                                                 
                  'SRHS2'           :  LLC_SR,                                                                 
                  'SRLS1'           :  LLC_SR,                                                                 
                  'SRLS2'           :  LLC_SR,                                                                
                  'RC1'             :  RCSnub,                                                                 
                  'RC2'             :  RCSnub,                                                                 
                  'RC3'             :  RCSnub,                                                                 
                  'RC4'             :  RCSnub,                                                                 
                  'HS3'             :  Diode,                                                                  
                  'LS3'             :  Diode                                                                 
               }
LLC_CTRL    = {                                                                                             
                  'Vref'    		   : 400 ,                                                                 #? [/]      - 
                  'sys_clk'         : 100e6,	                                                               #? [Hz]     - 100 MHz
                  'max_period'      : 2000,                                                                 #? [/]      - Maximum system period allowed
                  'min_period'      : 200,	                                                               #? [/]      - Minimum system period allowed
                  'SlewStep'        : 0.25/3,                                                               #? [V/ms]   - slew rate
                  'StartUpInc'      : 100,                                                                  #? [/]      - soft start frequency increment
                  'R1'              : 4700/4,                                                               #? [Ohm]    - sensing resistor
                  'R2'              : 160/24,                                                               #? [Ohm]    - sensing resistor
                  'C_sense'         : 10e-9,                                                                #? [F]      - sensing capacitor
                  'adc_conv'        : 15,                                                                   #? [/]      - Number of system clock cycles required for ADC conversion
                  'T_dt'            : 300e-9                                                                #? [s]      - dead time
               }
Grid        = {                                                                                             
                  'Config'          :  2,                                                                   #? [/]      - 
                  'Vin'             :  230,                                                                 #? [/]      - 
                  'Ts'              :  0,                                                                   #? [/]      - 
                  'Fgrid'           :  50,                                                                  #? [/]      - 
                  'Rg'              :  1e-2                                                                 #? [Ohm]    -                                                                                 
               }
Thermals    = {                                                                                             
                  'T_amb'           :  25.0,                                                                #? [/]      - 
                  'rth_Amb'         :  0.09                                                                 #? [/]      - 
               }
=======
                      'Config'		   : 1,                                                                                            #? [/]      - Capacitance configuration
                      'Cap_s'    		: 5*100e-6,                                                                                     #? [F]      - Capacitance value 
                      'Resr_s'		   : 1e-12,                                                                                        #? [F]      - Equivalent series resistance of the capacitance
                      'Lesl_s'		   : 1e-12,                                                                                        #? [H]      - Equivalent series inductance of the capacitance
                      'Npara'		      : 10,                                                                                           #? [/]      - Number of parallel capacitors
                      'Nseri'		      : 1,                                                                                            #? [/]      - Number of series capacitors
                      'Vinit'		      : 0,                                                                                            #? [V]      - Initial voltage across the capacitance
                      'Iinit'		      : 0                                                                                             #? [A]      - Initial current through the capacitance   
                     }
LLC         = {
                     'Config'		            : 1,                                                                                      #? [/]      - configuration
                     'R1'                    : 4700/4,                                                                                 #? [Ohm]    - Resistor 1 value
                     'R2'                    : 160/24,                                                                                 #? [Ohm]    - Resistor 2 value
                     'V_DC'                  : 200,                                                                                    #? [V]      - DC voltage source
                     'n_prim'                : 4,                                                                                      #? [/]      - Primary side turn number
                     'n_sndry'               : 4,                                                                                      #? [/]      - Secondary side turn number
                     'L_r'                   : 20e-6,                                                                                  #? [H]      - Resonant inductor
                     'L_k'                   : 5e-6,                                                                                   #? [H]      - Resonant inductor
                     'L_k_Iinit'             : 0,                                                                                      #? [H]      - Initial inductance of resonant inductor
                     'L_r_Iinit'             : 0,                                                                                      #? [/]      - Initial current in resonant inductor
                     'Trafo'                 : {
                        'Config'             : 1,                                                                                      #? [/]      - Transformer configuration
                        'n_prim'             : 4,                                                                                      #? [/]      - Primary side turn number
                        'n_sndry'            : 4,                                                                                      #? [/]      - Secondary side turn number
                        'Imaginit'           : 0,                                                                                      #? [/]      - Initial magnetizing current
                        'Lp'                 : 1e-9,                                                                                   #? [H]      - Primary inductance
                        'Rp'                 : 1e-2,                                                                                   #? [Ohm]    - Primary resistance
                        'Rc'                 : 10,                                                                                     #? [Ohm]    - Core resistance
                        'Lm'                 : 1e-9,                                                                                   #? [H]      - Magnetizing inductance
                        'Rs'                 : 10,                                                                                     #? [Ohm]    - Secondary resistance
                        'Ls'                 : 1e-9,                                                                                   #? [H]      - Secondary inductance
                        'LpIinit'            : 0,                                                                                      #? [H]      - Initial inductance of primary winding
                        'LmIinit'            : 0,                                                                                      #? [H]      - Initial inductance of magnetizing winding
                        'LsIinit'            : 0,                                                                                      #? [H]      - Initial inductance of secondary winding
                       
                        'Gap_CS_area'        : 676e-6 ,                                                                                #? [m2]     - Cross sectional Area
                        'Gap_flux_len'       : 1.5e-3*2,                                                                               #? [m]      - length of flux path
                        'Gap_init_MMF'       : 0,                                                                                      #? [A]      - Initial MMF
                        'Core_CS_area'       : 676e-6,                                                                                 #? [m2]     - Cross sectional Area
                        'Core_U_r_sat'       : 1,                                                                                      #? [/]      - saturated relative permeability
                        'Core_B_sat'         : 0.49,                                                                                   #? [T]      - flux density saturation
                        'Core_init_MMF'      : 0,                                                                                      #? [A]      - Initial MMF
                        'Core_U_r_unsat'     : 6500,                                                                                   #? [/]      - unsaturated relative permeability
                        'Core_flux_len'      : 149e-3                                                                                  #? [m]      - length of flux path
                     },
                     'C_r'             : {
                        'Config'       : 1,                                                                                            #? [/]      - Capacitance configuration
                        'Cap_s'        : 47e-6,                                                                                        #? [F]      - Capacitance value
                        'Resr_s'       : 1e-10,                                                                                        #? [Ohm]    - Equivalent series resistance of the capacitance
                        'Lesl_s'       : 1e-10,                                                                                        #? [H]      - Equivalent series inductance of the capacitance
                        'Npara'        : 1,                                                                                            #? [/]      - Number of parallel capacitors
                        'Nseri'        : 1,                                                                                            #? [/]      - Number of series capacitors
                        'Vinit'        : 0,                                                                                            #? [V]      - Initial voltage across the capacitance
                        'Iinit'        : 0                                                                                             #? [A]      - Initial current through the capacitance
                     },
                     'CT'              : {
                        'Config'       : 1                                                                                             #? [/]      - Capacitance configuration
                     },
                     'L'               : 1.6e-6,                                                                                       #? [H]      - Output inductor
                     'C_o'             : 480e-6,                                                                                       #? [F]      - Output capacitor
                     'C_v_init'        : 0,                                                                                            #? [V]      - Initial voltage across the output capacitor
                     'R_o'             : 100,                                                                                          #? [Ohm]    - Output resistance
                     'T_dt'            : 300e-9,                                                                                       #? [s]      - Time delay for switching
                     'HS1'             : {
                        'Config'       : 1,                                                                                            #? [/]      - Switch configuration
                        'therm_mosfet' : 'file:C3M0021120K',                                                                           #? [/]      - MOSFET thermal model file path
                        'Rgon'         : 2.5,                                                                                          #? [Ohm]    - Gate resistance for turn-on
                        'Rgoff'        : 2.5,                                                                                          #? [Ohm]    - Gate resistance for turn-off
                        'ron_mosfet'   : 67e-3,                                                                                        #? [Ohm]    - MOSFET on-state resistance
                        'Iinit'        : 0,                                                                                            #? [A]      - Initial current through the MOSFET
                        'Coss'         : {
                              'Config' : 5,                                                                                            #? [/]      - Capacitance configuration
                              'Cap_s'  : 197e-12,                                                                                      #? [F]      - Capacitance value
                              'Resr_s' : 1e-12,                                                                                        #? [Ohm]    - Equivalent series resistance of the capacitance
                              'Lesl_s' : 1e-12,                                                                                        #? [H]      - Equivalent series inductance of the capacitance
                              'Npara'  : 1,                                                                                            #? [/]      - Number of parallel capacitors
                              'Nseri'  : 1,                                                                                            #? [/]      - Number of series capacitors
                              'Vinit'  : 0,                                                                                            #? [V]      - Initial voltage across the capacitance
                              'Iinit'  : 0                                                                                             #? [A]      - Initial current through the capacitance
                        },
                        'therm_body_diode'   : 'file:C3M0021120K_bodydiode',                                                           #? [/]      - Body diode thermal model file path
                        'ron_body_diode'     : 5e-3,                                                                                   #? [Ohm]    - Body diode on-state resistance
                        'Rdb_off'            : 0,                                                                                      #? [Ohm]    - Resistance when the body diode is off
                        'vf_body_diode'      : 0.6,                                                                                    #? [V]      - Body diode forward voltage
                        'nPara'              : 1,                                                                                      #? [/]      - Number of parallel MOSFETs
                        'T_init'             : 25,                                                                                     #? [°C]     - Initial temperature of the MOSFET
                        'Tamb'               : 25,                                                                                     #? [°C]     - Ambient temperature
                        't_init'             : 25,                                                                                     #? [s]      - Initial time for thermal calculations
                        'rth_sw'             : 0.72,                                                                                   #? [K/W]    - Thermal resistance between the switch junction and case
                        'rth_ch'             : 62.5,                                                                                   #? [K/W]    - Thermal resistance between the case and heatsink
                        'Rth'                : 0.34                                                                                    #? [K/W]    - Total thermal resistance
                     },
                     'SRHS1'                 : {                                                                                             
                        'Config'             : 1,                                                                                      #? [/]      - Switch configuration 
                        'therm_mosfet'       : 'file:C3M0021120K',                                                                     #? [/]      - MOSFET thermal model file path
                        'Rgon'               : 2.5,                                                                                    #? [Ohm]    - Gate resistance for turn-on 
                        'Rgoff'              : 2.5,                                                                                    #? [Ohm]    - Gate resistance for turn-off
                        'ron_mosfet'         : 67e-3,                                                                                  #? [Ohm]    - MOSFET on-state resistance 
                        'Iinit'              : 0,                                                                                      #? [A]      - Initial current through the MOSFET 
                        'Coss'               : {                                                                                           
                              'Config'       : 5,                                                                                      #? [/]      - Capacitance configuration
                              'Cap_s'        : 197e-12,                                                                                #? [F]      - Capacitance value 
                              'Resr_s'       : 1e-12,                                                                                  #? [F]      - Equivalent series resistance of the capacitance
                              'Lesl_s'       : 1e-12,                                                                                  #? [H]      - Equivalent series inductance of the capacitance
                              'Npara'        : 1,                                                                                      #? [/]      - Number of parallel capacitors
                              'Nseri'        : 1,                                                                                      #? [/]      - Number of series capacitors
                              'Vinit'        : 0,                                                                                      #? [V]      - Initial voltage across the capacitance
                              'Iinit'        : 0                                                                                       #? [A]      - Initial current through the capacitance      
                        },                                                               
                        'therm_body_diode'   : 'file:C3M0021120K_bodydiode',                                                           #? [/]      - Body diode thermal model file path
                        'ron_body_diode'     : 5e-3,                                                                                   #? [Ohm]    - Body diode on-state resistance 
                        'Rdb_off'            : 0,                                                                                      #? [Ohm]    - Resistance when the body diode is off 
                        'vf_body_diode'      : 0.6,                                                                                    #? [V]      - Body diode forward voltage 
                        'nPara'              : 1,                                                                                      #? [/]      - Number of parallel MOSFETs
                        'T_init'             : 25,                                                                                     #? [°C]     - Initial temperature of the MOSFET 
                        'Tamb'               : 25,                                                                                     #? [°C]     - Ambient temperature 
                        't_init'             : 25,                                                                                     #? [/]      - Initial time for thermal calculations 
                        'rth_sw'             : 0.72,                                                                                   #? [K/W]    - Thermal resistance between the switch junction and case 
                        'rth_ch'             : 62.5,                                                                                   #? [K/W]    - Thermal resistance between the case and heatsink 
                        'Rth'                : 0.34 	                                                                                 #? [K/W]    - Total thermal resistance 				    	                           
                     },
                     'RC1' : {
                           'Config'          : 2,                                                                                      #? [/]      - Configuration setting (e.g., 1 for enabled)
                           'Rsnub'           : 1e-3,                                                                                   #? [Ohm]    - Snubber resistor value
                           'Csnub'           : {
                              'Config'       : 1,                                                                                      #? [/]      - Configuration setting for the snubber capacitor
                              'Cap_s'        : 1e-3,                                                                                   #? [F]      - Snubber capacitor value
                              'Resr_s'       : 0,                                                                                      #? [Ohm]    - Equivalent series resistance of the snubber capacitor
                              'Lesl_s'       : 0,                                                                                      #? [H]      - Equivalent series inductance of the snubber capacitor
                              'Npara'        : 1,                                                                                      #? [/]      - Number of parallel snubber capacitors
                              'Nseri'        : 1,                                                                                      #? [/]      - Number of series snubber capacitors
                              'Vinit'        : 0,                                                                                      #? [V]      - Initial voltage across the snubber capacitor
                              'Iinit'        : 0                                                                                       #? [A]      - Initial current through the snubber capacitor
                           }
                        }
         
                  }
CTRL        = {                                                                                             
                     'Vref'                  : 400,                                                                                    #? [V]      - Reference voltage
                     'sys_clk'               : 100e6,                                                                                  #? [Hz]     - System clock frequency (100 MHz)
                     'max_period'            : 2000,                                                                                   #? [µs]     - Maximum system period allowed
                     'min_period'            : 200,                                                                                    #? [µs]     - Minimum system period allowed
                     'SlewStep'              : 0.25/3,                                                                                 #? [V/ms]   - Slew rate
                     'StartUpInc'            : 100,                                                                                    #? [Hz]     - Soft start frequency increment
                     'R1'                    : 4700/4,                                                                                 #? [Ohm]    - Sensing resistor
                     'R2'                    : 160/24,                                                                                 #? [Ohm]    - Sensing resistor
                     'C_sense'               : 10e-9,                                                                                  #? [F]      - Sensing capacitor
                     'adc_conv'              : 15,                                                                                     #? [/]      - Number of system clock cycles required for ADC conversion
                     'T_dt'                  : 300e-9,                                                                                 #? [s]      - Dead time
                     'fs'                    : 70e-3,                                                                                  #? [Hz]     - Switching frequency
                     'Ri_Kp'                 : 0.1,                                                                                    #? [/]      - Proportional gain for current control
                     'Ri_Ki'                 : 600,                                                                                    #? [/]      - Integral gain for current control
                     'Rv_Kp'                 : 5,                                                                                      #? [/]      - Proportional gain for voltage control
                     'Rv_Ki'                 : 800                                                                                     #? [/]      - Integral gain for voltage control
                  }
>>>>>>> parent of 9eaedad (llc model updated)
HV_Filter   = {                                                                                             
                  'Config'         :  2,                                                                    #? [/]      - 
                  'Cy1'            :  {                                                                                        
                                          'Config'		      : 4,                                            #? [/]      - 
                                          'Cap_s'    		   : 1e-3,                                         #? [/]      - 
                                          'Resr_s'		      : 0,                                            #? [Ohm]    - 
                                          'Lesl_s'		      : 0,                                            #? [/]      - 
                                          'Npara'		      : 1,                                            #? [/]      - 
                                          'Nseri'		      : 1,                                            #? [/]      - 
                                          'Vinit'		      : 0,                                            #? [/]      - 
                                          'Iinit'		      : 0                                             #? [/]      -           
                                          },                                                             
                  'Cy2'            :  {                                                                                 
                                          'Config'		      : 4,                                            #? [/]      - 
                                          'Cap_s'    		   : 1e-3,                                         #? [/]      - 
                                          'Resr_s'		      : 0,                                            #? [Ohm]    - 
                                          'Lesl_s'		      : 0,                                            #? [/]      - 
                                          'Npara'		      : 1,                                            #? [/]      - 
                                          'Nseri'		      : 1,                                            #? [/]      - 
                                          'Vinit'		      : 0,                                            #? [/]      - 
                                          'Iinit'		      : 0                                             #? [/]      -           
                                          },                                                                
                  'Cx1'            :  {                                                                                      
                                          'Config'		      : 4,                                            #? [/]      - 
                                          'Cap_s'    		   : 1e-3,                                         #? [/]      - 
                                          'Resr_s'		      : 0,                                            #? [Ohm]    - 
                                          'Lesl_s'		      : 0,                                            #? [/]      - 
                                          'Npara'		      : 1,                                            #? [/]      - 
                                          'Nseri'		      : 1,                                            #? [/]      - 
                                          'Vinit'		      : 0,                                            #? [/]      - 
                                          'Iinit'		      : 0                                             #? [/]      -           
                                          },                                                          
                  'Cx2'            :  {                                                                                       
                                          'Config'		      : 4,                                            #? [/]      - 
                                          'Cap_s'    		   : 1e-3,                                         #? [/]      - 
                                          'Resr_s'		      : 0,                                            #? [Ohm]    - 
                                          'Lesl_s'		      : 0,                                            #? [/]      - 
                                          'Npara'		      : 1,                                            #? [/]      - 
                                          'Nseri'		      : 1,                                            #? [/]      - 
                                          'Vinit'		      : 0,                                            #? [/]      - 
                                          'Iinit'		      : 0                                             #? [/]      -           
                                          },                                                            
                  'Cx3'            :  {                                                                                    
                                          'Config'		      : 4,                                            #? [/]      - 
                                          'Cap_s'    		   : 1e-3,                                         #? [/]      - 
                                          'Resr_s'		      : 0,                                            #? [Ohm]    - 
                                          'Lesl_s'		      : 0,                                            #? [/]      - 
                                          'Npara'		      : 1,                                            #? [/]      - 
                                          'Nseri'		      : 1,                                            #? [/]      - 
                                          'Vinit'		      : 0,                                            #? [/]      - 
                                          'Iinit'		      : 0                                             #? [/]      -           
                                          },                                                               
                  'Cx4'            :  {                                                                              
                                          'Config'		      : 4,                                            #? [/]      - 
                                          'Cap_s'    		   : 1e-3,                                         #? [/]      - 
                                          'Resr_s'		      : 0,                                            #? [Ohm]    - 
                                          'Lesl_s'		      : 0,                                            #? [/]      - 
                                          'Npara'		      : 1,                                            #? [/]      - 
                                          'Nseri'		      : 1,                                            #? [/]      - 
                                          'Vinit'		      : 0,                                            #? [/]      - 
                                          'Iinit'		      : 0                                             #? [/]      -           
                                          },                                                              
                  'Cx5'            :  {                                              
                                          'Config'		      : 4,                                            #? [/]      - 
                                          'Cap_s'    		   : 1e-3,                                         #? [/]      - 
                                          'Resr_s'		      : 0,                                            #? [Ohm]    - 
                                          'Lesl_s'		      : 0,                                            #? [/]      - 
                                          'Npara'		      : 1,                                            #? [/]      - 
                                          'Nseri'		      : 1,                                            #? [/]      - 
                                          'Vinit'		      : 0,                                            #? [/]      - 
                                          'Iinit'		      : 0                                             #? [/]      -           
                                          },                                                       
                  'L'              :  40e-6,                                                                #? [/]      - 
                  'L_DMC'          :  900e-6                                                                #? [/]      - 
            }
AC_Filter   = {                                                                                             
                  'Config'          :  4 ,                                                                  #? [/]      - 
                  'Cin'             :  1e-6,                                                                #? [/]      - 
                  'L_CMC'           :  1.5e-3,                                                              #? [/]      - 
                  'L_DMC'           :  900e-6,                                                              #? [/]      - 
                  'Cx'              :  0.1e-6,                                                              #? [/]      -    
                  'Cy1'             :  4.7e-12,                                                             #? [/]      -    
                  'Cy2'             :  4.7e-12,                                                             #? [/]      -    
                  'Ll'              :  10e-6                                                                #? [/]      -    
               }
Battery     = {  
                  'Config'                    : 2,                                                          #? [/]      -         
                  'n_series'                  : 75,                                                         #? [/]      -  number of series-connected cells
                  'n_parallel'                : 5,                                                          #? [/]      -  number of parallel branches
                  'SOC_init'                  : 0.5,                                                        #? [/]      -  initial SOC
                  'polarizingRshift'          : 0.10,                                                       #? [/]      -  shift polarizing R by 10#
                  'cellNominalV'              : 2.9,                                                        #? [/]      -  voltage at end of nominal zone
                  'cellFullChargeV'           : 3.3,                                                        #? [/]      -  voltage at full SOC
                  'cellExponentialV'          : 3.05,                                                       #? [/]      -  voltage at end of exponential zone
                  'cellRatedCapacity'         : 2.4,                                                        #? [/]      -  cell rated capacity
                  'cellMaximumCapacity'       : 2.4,                                                        #? [/]      -  cell maximum capacity
                  'cellNominalCapacity'       : 2.1,                                                        #? [/]      -  cell capacity at end of nominal zone
                  'cellExponentialCapacity'   : 0.25,                                                       #? [/]      -  cell capacity at end of exponential zone
                  'cellNominalDischargeI'     : 2.3,                                                        #? [/]      -  nominal discharge current for cell
                  'cellInternalR'             : 6e-3,                                                       #? [/]      -  internal cell resistance
                  'Rdis'                      : 0,                                                          #? [/]      - 
                  'I_dc'                      : 0,                                                          #? [/]      - 
                  'Rcell1'                    : 0,                                                          #? [Ohm]    - 
                  'Rcell2'                    : 0,                                                          #? [/]      - 
                  'Ccell1'                    : 0,                                                          #? [/]      - 
                  'Ccell2'                    : 0,                                                          #? [/]      - 
                  'V_OC1'                     : 0,                                                          #? [/]      - 
                  'Cdis'                      :  {                                                                                    
                                                'Config'		      : 1,                                      #? [/]      - 
                                                'Cap_s'    		   : 0,                                      #? [/]      - 
                                                'Resr_s'		      : 0,                                      #? [Ohm]    -
                                                'Lesl_s'		      : 0,                                      #? [/]      - 
                                                'Npara'		      : 1,                                      #? [/]      - 
                                                'Nseri'		      : 1,                                      #? [/]      - 
                                                'Vinit'		      : 0,                                      #? [/]      - 
                                                'Iinit'		      : 0                                       #? [/]      - 
                                                },                                                          
<<<<<<< HEAD
                     'L'                     : 40e-6,                                                                                  #? [H]      - Inductor value
                     'Choke'                 : {
                        'Config'             : 1,                                                                                      #? [/]      - Diode thermal description
                        'L1'                 : 1.5e-3,                                                                                 #? [H]      - Inductance of the first choke winding
                        'L2'                 : 1.5e-3,                                                                                 #? [H]      - Inductance of the second choke winding
                        'R1'                 : 0.01,                                                                                   #? [Ohm]    - Resistance of the first choke winding
                        'R2'                 : 0.01,                                                                                   #? [Ohm]    - Resistance of the second choke winding
                        'Lm'                 : 0.001,                                                                                  #? [H]      - Mutual inductance of the choke
                        'Rm'                 : 0.001,                                                                                  #? [Ohm]    - Resistance of the mutual inductance
                        'i1'                 : 0,                                                                                      #? [A]      - Initial current in the first choke winding
                        'i2'                 : 0                                                                                       #? [A]      - Initial current in the second choke winding
                     },
                  }
Load        = {
                     'Config'                : 1,                                                                                      #? [/]      - Configuration type for the load setup
                     'CL'                    : 0,                                                                                      #? [F]      - Load capacitance value
                     'R'                     : 50,                                                                                     #? [Ohm]    - Load resistance value
                     'L'                     : 0,                                                                                      #? [H]      - Load inductance value
                     'Vinit'                 : 0,                                                                                      #? [V]      - Initial voltage across the load
                     'Iinit'                 : 0,                                                                                      #? [A]      - Initial current through the load
                     't_switch'              : Sim_param['tSim'] - Sim_param['load_tflip'],                                            #? [s]      - Time when the load switching occurs
                     't_dead'                : (Sim_param['tSim'] - Sim_param['load_tflip']) / 2                                       #? [s]      - Dead time for load switching
                  }
Thermals    = {
                     'T_amb'                 : 25.0,                                                                                   #? [°C]     - Ambient temperature
                     'rth_Amb'               : 0                                                                                    #? [K/W]    - Thermal resistance from junction to ambient
                  }
=======
                  'cellLPFTimeConstant'       : 30                                                          #? [/]      -  30 second time constant for LPF for effect of current on voltage
               }
>>>>>>> parent of 1b0789f (merging changes for back up (#30))
#!----------------------------------------------------------------------------------------------------------------------------------------
ModelVars   = {                                                                                             
                  'Sim_param'       :  Sim_param   ,      
                  'ToFile'          :  ToFile      ,    
                  'PFC_glb'         :  PFC_glb     ,     
                  'PFC_SW'          :  PFC_SW      ,                                                             
                  'LLC_SW'          :  LLC_SW      ,                                                             
                  'LLC_SR'          :  LLC_SR      ,                                                             
                  'PFC'             :  PFC         ,                                                                 
                  'CTRL_PFC'        :  CTRL_PFC    ,                                                            
                  'DCLink'          :  DCLink      ,                                                              
                  'Load'            :  Load        ,                                                                
                  'RCSnub'          :  RCSnub      ,                                                                
                  'Diode'           :  Diode       ,                                                                
                  'LLC'             :  LLC         ,                                                                 
                  'LLC_CTRL'        :  LLC_CTRL    ,                                                            
                  'Grid'            :  Grid        ,                                                                   
                  'Thermals'        :  Thermals    ,
                  'HV_Filter'       :  HV_Filter   ,                                                            
                  'AC_Filter'       :  AC_Filter   ,                                                           
                  'Battery'         :  Battery                                                             
               }	
<<<<<<< HEAD
SolverOpts  = {
                  'Sim_param'       :  ModelVars['Sim_param'] 
               }
AnalysisOpts= {
                  'system_period'   :  1/100e3     ,      
                  'freq_range_min'  :  1          ,
                  'freq_range_max'  :  1e7         ,
                  'amplitude'       :  1e-1        ,                                                                   
                  'sim_Tstart'      :  0           ,                                                           
                  'NB_pts'          :  10000        ,                                                                 
                  'additional_freq' :  []          ,                                                              
                  'NB_init_cycles'  :  0           ,                                                                 
                  'Termination_tol' :  1e-3        ,                                                            
                  'max_iter_NB'     :  50          ,   
                  'Jacobian_rel_tol':  1e-6        
                                                                           
              }
#!----------------------------------------------------------------------------------------------------------------------------------------
def set_scopes(model):
    	
   scopes      =  [                                                                                            
                     f"{model}/Scope",                                                                             
                     f"{model}/Scopes/grid_scope",                                                                 
                     f"{model}/Scopes/EMI_scope",                                                                                         
                     f"{model}/Scopes/grid vs filter",                                                             
                     f"{model}/Scopes/PFC Input Output",                                                                                        
                     f"{model}/Scopes/PFC Gates",                                                                                        
                     f"{model}/Scopes/PFC Choke",                                                                                      
                     f"{model}/Scopes/PFC SW Voltages",                                                                                    
                     f"{model}/Scopes/PFC SW Currents",                                                                                    
                     f"{model}/Scopes/PFC SW junction Temp",                                                                                    
                     f"{model}/Scopes/PFC SW switching losses",                                                                                  
                     f"{model}/Scopes/PFC SW conduction losses",                                                                                
                     f"{model}/Scopes/PFC Cout",  
                     f"{model}/Scopes/Efficiency",   
                     f"{model}/Scopes/Load",                                                                                                                                                                                                                                                                                                                         
                     f"{model}/Scopes/PFC TL"                                                                                 
                  ]	
   return scopes
=======
#!----------------------------------------------------------------------------------------------------------------------------------------	
scopes      =  [                                                                                            
				      "OBC/Scope",                                                                             
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
                  "OBC/Scopes/load_scope",                                                                              
                  "OBC/Scopes/relays",                                                                                  
                  "OBC/Scopes/battery"                                                                                  

               ]	
>>>>>>> parent of 1b0789f (merging changes for back up (#30))
Waveforms   =  [                                                                                            
                  'Grid Voltage',                  
                  'Grid Current',
                  #!-------------------------
                  'EMI Filter Voltage',
                  'EMI Filter Current',
                  #!-------------------------
                  'PFC Input Voltage',
                  #!-------------------------
                  'PFC Input Current',
                  #!-------------------------
                  'PFC output voltage',
                  #!-------------------------
                  'PFC gates signal HS1',
                  'PFC gates signal HS2',
                  'PFC gates signal LS1',
                  'PFC gates signal LS2',
                  #!-------------------------
                  'PFC Input choke Voltage',
                  'PFC Input choke Current',
                  #!-------------------------
                  'PFC HS1 voltage',
                  'PFC Diode HS1 voltage',
                  'PFC HS2 voltage',
                  'PFC Diode HS2 voltage',
                  'PFC LS1 voltage',
                  'PFC Diode LS1 voltage',
                  'PFC LS2 voltage',
                  'PFC Diode LS2 voltage',
                  #!-------------------------
                  'PFC HS1 Current',
                  'PFC Diode HS1 Current',
                  'PFC HS2 Current',
                  'PFC Diode HS2 Current',
                  'PFC LS1 Current',
                  'PFC Diode LS1 Current',
                  'PFC LS2 Current',
                  'PFC Diode LS2 Current',
                  #!-------------------------
                  'PFC HS1 junction Temp',
                  'PFC Diode HS1 junction Temp',
                  'PFC HS2 junction Temp',
                  'PFC Diode HS2 junction Temp',
                  'PFC LS1 junction Temp',
                  'PFC Diode LS1 junction Temp',
                  'PFC LS2 junction Temp',
                  'PFC Diode LS2 junction Temp',
                  #!-------------------------
                  'PFC case Temp HS1',
                  'PFC case Temp HS2',
                  'PFC case Temp LS1',
                  'PFC case Temp LS2',
                  #!-------------------------
                  'PFC HS1 switching losses',
                  'PFC HS2 switching losses',
                  'PFC LS1 switching losses',
                  'PFC LS2 switching losses',
                  #!-------------------------
                  'PFC HS1 conduction losses',
                  'PFC Diode HS1 conduction losses',
                  'PFC HS2 conduction losses',
                  'PFC Diode HS2 conduction losses',
                  'PFC LS1 conduction losses',
                  'PFC Diode LS1 conduction losses',
                  'PFC LS2 conduction losses',
                  'PFC Diode LS2 conduction losses',
                  #!-------------------------
                  'PFC output capacitor voltage',
                  'PFC output capacitor current',
                  'PFC output capacitor dissipation',
                  #!-------------------------                 
                  'PFC input busbar+ Resistor Voltage',
                  'PFC input busbar+ Resistor Current',
                  'PFC input busbar+ Resistor Dissipation',
                  'PFC input busbar- Resistor Voltage',
                  'PFC input busbar- Resistor Current',
                  'PFC input busbar- Resistor Dissipation',
                  #!-------------------------
                  'PFC output busbar+ Resistor Voltage',
                  'PFC output busbar+ Resistor Current',
                  'PFC output busbar+ Resistor Dissipation',
                  'PFC output busbar- Resistor Voltage',
                  'PFC output busbar- Resistor Current',
                  'PFC output busbar- Resistor Dissipation',
                  #!-------------------------
                  'DCLink Capacitor Voltage',
                  'DCLink Capacitor Current',
                  #!-------------------------
                  'Battery Pack SOC',
                  'Battery Pack depleted charge',
                  'Battery Pack Voltage',
                  'Battery Pack Current',
                  #!-------------------------
                  'Load Voltage',
                  'Load Current'
               ]		
#!----------------------------------------------------------------------------------------------------------------------------------------	