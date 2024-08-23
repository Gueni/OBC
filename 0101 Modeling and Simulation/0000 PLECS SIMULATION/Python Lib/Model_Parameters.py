
#!---------------------------------------------------------------------------------------------------------------------------------------- 
#!                                           ____  ____  ______   _    __
#!                                          / __ \/ __ )/ ____/  | |  / /___ ___________
#!                                         / / / / __  / /       | | / / __ `/ ___/ ___/
#!                                        / /_/ / /_/ / /___     | |/ / /_/ / /  (__  )
#!                                        \____/_____/\____/     |___/\__,_/_/  /____/
#!----------------------------------------------------------------------------------------------------------------------------------------
import os 
#!----------------------------------------------------------------------------------------------------------------------------------------                                                         
current_directory   = os.getcwd()                                                                                                                                                              
Traces_path         = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Traces/"           
ToFile_path         = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/CSV/"              
logfile_path        = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/Log/"              
output_html_path    = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/RES/html/"             
model_path          = "0101 Modeling and Simulation/0000 PLECS SIMULATION/Model/OBC.plecs"                  
model_directory     = (os.path.join(current_directory, model_path)).replace("\\", "/")                                     
#!----------------------------------------------------------------------------------------------------------------------------------------
Sim_param 	= {                                                                                            
                  'tSim'	    	   : 1.0,                                                                  #? [s]     - Total simulation time
                  'load_tflip'	   : 1.0/2,                                                                #? [s]     - Time at which the load changes state 
                  'maxStep'		   : 1e-3,                                                                 #? [s]     - Maximum simulation time step
                  'ZeroCross'       : 1000,                                                                 #? [/]     - Zero-crossing detection limit
                  'rel_tol'		   : 1e-7                                                                  #? [/]     - Relative tolerance for the numerical solver
               }
ToFile      = {   
                  'Ts'              : 0,                                                                    #? [s]     - Sampling time for saving data
                  'tsave' 	    	   : Sim_param['tSim']-200e-6                                              #? [s]     - Time point at which the data is saved
               }
PFC_glb     = {                                                                                             
                  'L'               :  22e-6,                                                               #? [H]      - 
                  'Rbusin'          :  0.01,                                                                #? [Ohm]    - 
                  'Rbusout'         :  0.01,                                                                #? [Ohm]    - 
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
                  'Config'          : 1,                                                                    #? [/]      - Switch configuration 
                  'therm_mosfet'    : 'file:C3M0021120K',                                                   #? [/]      - MOSFET thermal model file path
                  'Rgon'            : 2.5,                                                                  #? [Ohm]    - Gate resistance for turn-on 
                  'Rgoff'           : 2.5,                                                                  #? [Ohm]    - Gate resistance for turn-off
                  'ron_mosfet'      : 0,                                                                #? [Ohm]    - MOSFET on-state resistance 
                  'Iinit'           : 0,                                                                    #? [A]      - Initial current through the MOSFET 
                  'Coss'            :  {                                                                                           
                                          'Config'		      : 5,                                            #? [/]      - Capacitance configuration
                                          'Cap_s'    		   : 197e-12,                                      #? [F]      - Capacitance value 
                                          'Resr_s'		      : 1e-12,                                        #? [F]      - Equivalent series resistance of the capacitance
                                          'Lesl_s'		      : 1e-12,                                        #? [H]      - Equivalent series inductance of the capacitance
                                          'Npara'		      : 1,                                            #? [/]      - Number of parallel capacitors
                                          'Nseri'		      : 1,                                            #? [/]      - Number of series capacitors
                                          'Vinit'		      : 0,                                            #? [V]      - Initial voltage across the capacitance
                                          'Iinit'		      : 0                                             #? [A]      - Initial current through the capacitance      
                                          },                                                               
                  'therm_body_diode': 'file:C3M0021120K_bodydiode',                                         #? [/]      - Body diode thermal model file path
                  'ron_body_diode'  : 5e-3,                                                                 #? [Ohm]    - Body diode on-state resistance 
                  'Rdb_off'         : 0,                                                                    #? [Ohm]    - Resistance when the body diode is off 
                  'vf_body_diode'   : 0.6,                                                                  #? [V]      - Body diode forward voltage 
                  'nPara'           : 1,                                                                    #? [/]      - Number of parallel MOSFETs
                  'T_init'          : 25,                                                                   #? [°C]     - Initial temperature of the MOSFET 
                  'Tamb'            : 25,                                                                   #? [°C]     - Ambient temperature 
                  't_init'          : 25,                                                                   #? [/]      - Initial time for thermal calculations 
                  'rth_sw'          : 0.72,                                                                 #? [K/W]    - Thermal resistance between the switch junction and case 
                  'rth_ch'          : 62.5,                                                                 #? [K/W]    - Thermal resistance between the case and heatsink 
                  'Rth'             : 0.34 	                                                               #? [K/W]    - Total thermal resistance 				    	                           
               }
LLC_SW      = {                                                                                             
                  'Config'          : 1,                                                                    #? [/]      - Switch configuration 
                  'therm_mosfet'    : 'file:C3M0021120K',                                                   #? [/]      - MOSFET thermal model file path
                  'Rgon'            : 2.5,                                                                  #? [Ohm]    - Gate resistance for turn-on 
                  'Rgoff'           : 2.5,                                                                  #? [Ohm]    - Gate resistance for turn-off
                  'ron_mosfet'      : 67e-3,                                                                #? [Ohm]    - MOSFET on-state resistance 
                  'Iinit'           : 0,                                                                    #? [A]      - Initial current through the MOSFET 
                  'Coss'            :  {                                                                                           
                                          'Config'		      : 5,                                            #? [/]      - Capacitance configuration
                                          'Cap_s'    		   : 197e-12,                                      #? [F]      - Capacitance value 
                                          'Resr_s'		      : 1e-12,                                        #? [F]      - Equivalent series resistance of the capacitance
                                          'Lesl_s'		      : 1e-12,                                        #? [H]      - Equivalent series inductance of the capacitance
                                          'Npara'		      : 1,                                            #? [/]      - Number of parallel capacitors
                                          'Nseri'		      : 1,                                            #? [/]      - Number of series capacitors
                                          'Vinit'		      : 0,                                            #? [V]      - Initial voltage across the capacitance
                                          'Iinit'		      : 0                                             #? [A]      - Initial current through the capacitance      
                                          },                                                               
                  'therm_body_diode': 'file:C3M0021120K_bodydiode',                                         #? [/]      - Body diode thermal model file path
                  'ron_body_diode'  : 5e-3,                                                                 #? [Ohm]    - Body diode on-state resistance 
                  'Rdb_off'         : 0,                                                                    #? [Ohm]    - Resistance when the body diode is off 
                  'vf_body_diode'   : 0.6,                                                                  #? [V]      - Body diode forward voltage 
                  'nPara'           : 1,                                                                    #? [/]      - Number of parallel MOSFETs
                  'T_init'          : 25,                                                                   #? [°C]     - Initial temperature of the MOSFET 
                  'Tamb'            : 25,                                                                   #? [°C]     - Ambient temperature 
                  't_init'          : 25,                                                                   #? [/]      - Initial time for thermal calculations 
                  'rth_sw'          : 0.72,                                                                 #? [K/W]    - Thermal resistance between the switch junction and case 
                  'rth_ch'          : 62.5,                                                                 #? [K/W]    - Thermal resistance between the case and heatsink 
                  'Rth'             : 0.34 	                                                               #? [K/W]    - Total thermal resistance 				    	                           
               }
LLC_SR      = {                                                                                             
                  'Config'          : 1,                                                                    #? [/]      - Switch configuration 
                  'therm_mosfet'    : 'file:C3M0021120K',                                                   #? [/]      - MOSFET thermal model file path
                  'Rgon'            : 2.5,                                                                  #? [Ohm]    - Gate resistance for turn-on 
                  'Rgoff'           : 2.5,                                                                  #? [Ohm]    - Gate resistance for turn-off
                  'ron_mosfet'      : 67e-3,                                                                #? [Ohm]    - MOSFET on-state resistance 
                  'Iinit'           : 0,                                                                    #? [A]      - Initial current through the MOSFET 
                  'Coss'            :  {                                                                                           
                                          'Config'		      : 5,                                            #? [/]      - Capacitance configuration
                                          'Cap_s'    		   : 197e-12,                                      #? [F]      - Capacitance value 
                                          'Resr_s'		      : 1e-12,                                        #? [F]      - Equivalent series resistance of the capacitance
                                          'Lesl_s'		      : 1e-12,                                        #? [H]      - Equivalent series inductance of the capacitance
                                          'Npara'		      : 1,                                            #? [/]      - Number of parallel capacitors
                                          'Nseri'		      : 1,                                            #? [/]      - Number of series capacitors
                                          'Vinit'		      : 0,                                            #? [V]      - Initial voltage across the capacitance
                                          'Iinit'		      : 0                                             #? [A]      - Initial current through the capacitance      
                                          },                                                               
                  'therm_body_diode': 'file:C3M0021120K_bodydiode',                                         #? [/]      - Body diode thermal model file path
                  'ron_body_diode'  : 5e-3,                                                                 #? [Ohm]    - Body diode on-state resistance 
                  'Rdb_off'         : 0,                                                                    #? [Ohm]    - Resistance when the body diode is off 
                  'vf_body_diode'   : 0.6,                                                                  #? [V]      - Body diode forward voltage 
                  'nPara'           : 1,                                                                    #? [/]      - Number of parallel MOSFETs
                  'T_init'          : 25,                                                                   #? [°C]     - Initial temperature of the MOSFET 
                  'Tamb'            : 25,                                                                   #? [°C]     - Ambient temperature 
                  't_init'          : 25,                                                                   #? [/]      - Initial time for thermal calculations 
                  'rth_sw'          : 0.72,                                                                 #? [K/W]    - Thermal resistance between the switch junction and case 
                  'rth_ch'          : 62.5,                                                                 #? [K/W]    - Thermal resistance between the case and heatsink 
                  'Rth'             : 0.34 	                                                               #? [K/W]    - Total thermal resistance 				    	                           
               }
PFC         = {                                                                                             
                  'Config'          :  1,                                                                   #? [/]      - diode thermal description  
                  'HS1'             :  PFC_SW,                                                              #? [/]      - diode thermal description  
                  'HS2'             :  PFC_SW,                                                              #? [/]      - diode thermal description   
                  'LS1'             :  PFC_SW,                                                              #? [/]      - diode thermal description  
                  'LS2'             :  PFC_SW,                                                              #? [/]      - diode thermal description 
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
               }
DCLink      = {                                                                                             
                      'Config'		      : 5,                                                              #? [/]      - Capacitance configuration
                      'Cap_s'    		   : 100e-6,                                      #? [F]      - Capacitance value 
                      'Resr_s'		      : 1e-12,                                        #? [F]      - Equivalent series resistance of the capacitance
                      'Lesl_s'		      : 1e-12,                                        #? [H]      - Equivalent series inductance of the capacitance
                      'Npara'		      : 10,                                            #? [/]      - Number of parallel capacitors
                      'Nseri'		      : 1,                                            #? [/]      - Number of series capacitors
                      'Vinit'		      : 0,                                            #? [V]      - Initial voltage across the capacitance
                      'Iinit'		      : 0                                             #? [A]      - Initial current through the capacitance   
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
                  'HS1'             :  LLC_SW,                                                              #? [/]      - diode thermal description    
                  'HS2'             :  LLC_SW,                                                              #? [/]      - diode thermal description    
                  'LS1'             :  LLC_SW,                                                              #? [/]      - diode thermal description    
                  'LS2'             :  LLC_SW,                                                              #? [/]      - diode thermal description 
                  'SRHS1'           :  LLC_SR,                                                              #? [/]      - diode thermal description   
                  'SRHS2'           :  LLC_SR,                                                              #? [/]      - diode thermal description    
                  'SRLS1'           :  LLC_SR,                                                              #? [/]      - diode thermal description    
                  'SRLS2'           :  LLC_SR,                                                              #? [/]      - diode thermal description   
                  'RC1'             :  RCSnub,                                                              #? [/]      - diode thermal description    
                  'RC2'             :  RCSnub,                                                              #? [/]      - diode thermal description    
                  'RC3'             :  RCSnub,                                                              #? [/]      - diode thermal description    
                  'RC4'             :  RCSnub,                                                              #? [/]      - diode thermal description    
                  'HS3'             :  Diode,                                                               #? [/]      - diode thermal description    
                  'LS3'             :  Diode                                                                #? [/]      - diode thermal description  
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
               }	
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
Units       =  [                                                                                            
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ W ]',                  
                  #!-------------------------
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ V ]',                  
                  '[ V ]',                  
                  '[ V ]',                  
                  '[ W ]',                  
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',                  
                  #!-------------------------
                  '[A/m]',
                  '[Wb/m²]',
                  '[A/m]',
                  '[Wb/m²]',
                  #!-------------------------
                  '[A·turns]',
                  '[Wb]',
                  '[A·turns]',
                  '[Wb]',
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ V ]',                  
                  '[ A ]',                  
                  #!-------------------------
                  '[ V ]',                  
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ W ]',                  
                  '[ C ]',                  
                  '[ W ]',                  
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ W ]',                  
                  #!-------------------------                 
                  '[ W ]',                  
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ W ]',   
                  '[ W ]', 
                  '[ W ]',               
                  '[ % ]', 
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ W ]'                  
               ]
#!----------------------------------------------------------------------------------------------------------------------------------------