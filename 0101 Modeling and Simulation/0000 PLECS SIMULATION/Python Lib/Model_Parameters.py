
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
                  'tSim'	    	   : 10, 
                  'maxStep'		   : 1e-3,  
                  'ZeroCross'       : 1000,
                  'idx'             : 0,
                  'rel_tol'		   : 1e-3 
               }
ToFile      =  {   
                  'ToFile_path'		: os.path.join(os.getcwd(),f'/0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/Results_{Sim_param['idx']}.csv'),                     
                  'Ts'              : 1/100e3,
                  'output_html'     : os.path.join(os.getcwd(),'/0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/output_html.html') 
                           
               }  
scopes      =  {
				      'Scope'	    	   : "OBC/Scope",                                
               }	
PFC_glb     =  {
                  'L'               :  1.5e-3,
                  'Rl'              :  0.001,
                  'Cout'            :  {
                                             'Config'		      : 1,
                                             'Cap_s'    		   : 400e-6,  
                                             'Resr_s'		      : 19e-6,  
                                             'Lesl_s'		      : 0,  
                                             'Npara'		      : 1,  
                                             'Nseri'		      : 1,  
                                             'Vinit'		      : 0,  
                                             'Iinit'		      : 0             
                                       },  
                  # 'CF'              :  100e3,  
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
                  'Ldr'             : 0,
                  'Ldr_Iinit'       : 0,
                  'Lso'             : 0,
                  'Lso_Iinit'       : 0,
                  'nPara'           : 0,
                  'T_init'          : 25,
                  'Tamb'            : 25, 
                  't_init'          : 25, 
                  'rth_ch'          : 0.5, 
                  'Rth'             : 0.34 					    	                           
               }
PFC         =  {
                  'R1'              :  4700/4,
                  'R2'              :  160/24,
                  'fs'              :  70e3,  
                  'HS1'             :  PFC_SW,   
                  'HS2'             :  PFC_SW,   
                  'LS1'             :  PFC_SW,   
                  'LS2'             :  PFC_SW,
                  'Ri_F '           :  50e3,
                  'Ri_Ts'           :  1/50e3,
                  'Ri_Tp'           :  (1/50e3)/2.0,
                  'Ri_Ti'           :  2/PFC_glb['Rl']*((1/50e3)/2.0),
                  'Ri_Tn'           :  PFC_glb['L']/PFC_glb['Rl'],
                  'Ri_Kp'           :  (PFC_glb['L']/PFC_glb['Rl'])/(2/PFC_glb['Rl']*((1/50e3)/2.0)),
                  'Ri_Ki'           :  1/(2/PFC_glb['Rl']*((1/50e3)/2.0)),
                  'Rv_F '           :  2e3,
                  'Rv_Ts'           :  1/2e3,
                  'Rv_Tp'           :  (1/2e3)/2*10,
                  'Rv_Ti'           :  8/PFC_glb['Cout']['Cap_s']*((1/2e3)/2*10)*((1/2e3)/2*10),
                  'Rv_Tn'           :  4*((1/2e3)/2*10),
                  'Rv_Kp'           :  (4*((1/2e3)/2*10))/(8/PFC_glb['Cout']['Cap_s']*((1/2e3)/2*10)*((1/2e3)/2*10)),
                  'Rv_Ki'           :  1/(8/PFC_glb['Cout']['Cap_s']*((1/2e3)/2*10)*((1/2e3)/2*10))
               }		
DCLink      =  {
                  'Config'		      : 1,
                  'Cdc'    		   : 500e-3,  
                  'ESR'		         : 19e-6,
                  'ESL'		         : 0, 
                  'nPara'		      : 1, 
                  'nSeri'		      : 1, 
                  'Vinit'		      : 0, 
                  'Iinit'		      : 0, 

               }
Load      =  {
                  'Config'		      : 4,  
                  'CL'    		      : 0, 
                  'RL'		         : (400*400)/7000,  
                  'LL'		         : 1e-9, 
                  'Vinit'		      : 0,  
                  'Iinit'		      : 0, 
               }
LLC       =  {
                  ## Sensing
                  'R1'               : 4700/4,           # [Ohm] - sensing resistor
                  'R2'               : 160/24,           # [Ohm] - sensing resistor
                  'V_DC'          : 400,            # [V] - DC voltage source
                  'n_prim'          : 10,            # [] - primary side turn number
                  'n_sndry'         : 2,           # [] - secondary side turn number
                  ## Primary side
                  'L_r'               : 1.55e-6,   		  # [H] - resonant inductor
                  'C_r'               : 1.2e-6,   		  # [F] - resonant capacitor
                  ## Secondary side
                  'L'               : 1.6e-6,   			  # [H] - output inductor
                  'C_o'               : 480e-6,   		  # [F] - output capacitor
                  'C_v_init'               : 0,   		  # [V] - output capacitor initial voltage
                  ## Controller
                  'sys_clk'               : 100e6,   	  # [Hz] - 100 MHz
                  'max_period'               : 2000,     # Maximum system period allowed
                  'min_period'               : 200,   	  # Minimum system period allowed
                  ## Voltage change control
                  'SlewStep'               : 50/3,     # [V/ms] - slew rate
                  'StartUpInc'               : 500,      # [] - soft start frequency increment
                
                  'C_sense'               : 10e-9,       # [F] - sensing capacitor
                  ## ADC conversion time
                  'adc_conv'               : 15,         # [] - Number of system clock cycles required for ADC conversion
                  ## Dead time
                  'T_dt'               : 300e-9,         # [s] - dead time
                  ## Thermal parameters 
                  # 'mosfet'               : 'file:C2M0025120D',      # MOSFET thermal description
                  'ron_mosfet'               : 30e-3,    	          # MOSFET on resistance (ohms)
                  'vf_body_diode'               : 4.5,    	       # diode forward voltage (V)
                  'ron_body_diode'               : 5e-3,            # diode on resistance (ohms)
                  'rgon'               : 2.5,    				       # external turn-on gate resistance (ohms) 
                  'rgoff'               : 2.5,   				       # external turn-off gate resistance (ohms) 
                  'rth_ch'              : 0.1,   		 		       # thermal resistance case-heatsink (grease) (K/W)
                  # 'diode'               : 'file:E4D20120G',   	# diode thermal description
                  'ron_diode'               : 1,                # diode forward voltage (V)
                  'vf_diode'               : 1.4,               # diode forward voltage (V) 
                  'rth_ch_diode'              : 0.5,   		 	# thermal resistance case-heatsink (grease) (K/W)
                  'num_par_diode'               : 4,            # Number of parallel diodes
                  'Rth'               : 0.1,                    # Heatsink to ambient thermal resistance (K/W)
                  't_init'               : 25                     					# initial temperature (C)
             }

Grid      = {
                  'Config'          :  2,  
                  'Vin'             :  230,  
                  'Fgrid'           :  50,  
                  'F'               :  50,  
                  'Rg'              :  1e-3                                                                                  

}


#?----------------------------------------------------------------------------------------------------------------------------------------
ModelVars   =  {  'ToFile'          :  ToFile,
                  'scopes'          :  scopes,  
                  'Sim_param'       :  Sim_param,  
                  'Grid'            :  Grid,  

                  #? AC Input Filter Parameters  
                  'in_filter_config':  1, 
                  'Cin'             :  1e-9,  
                   'Lin'            :  1e-9,  
                   'Ro'             :  1e-9, 

                  'L_CMC'           :  (1.5e-3)/2, 
                  'L_DMC'           :  (900e-6)/2, 
                  'Cx'              :  1e-6,  
                  'Cy1'             :  4.7e-9, 
                  'Cy2'             :  4.7e-9,  
                  'Cd'              :  100e-3,  
                  'Rd'              :  470e3,  
                  #? PFC Parameters 
                  'PFC_glb'         :  PFC_glb, 
                  'PFC'             :  PFC, 
                  #? DCLink Parameters 
                  'DCLink'          :  DCLink,  
                  #? LLC Parameters 
                  'LLC'             :  LLC,  
                  #? Load Parameters 
                  'Vout'            :  400,  
                  'Load'            :  Load                                                                                   
               }	
#?----------------------------------------------------------------------------------------------------------------------------------------			
