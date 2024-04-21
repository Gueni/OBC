
import math
#?----------------------------------------------------------------------------------------------------------------------------------------
Sim_param 	=  {
                  'tSim'	    	   : 10                                                        ,  #  simulation time
                  'maxStep'		   : 1e-3                                                      ,  #  maximum step size
                  'idx'             : 0                                                         ,  #
                  'rel_tol'		   : 1e-3                                                         #  relative tolerance
               }
ToFile      =  {   
                  'ToFile_path'		: (f"D:/4 WORKSPACE/24-OBC/OBC/0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/Results_{Sim_param['idx']}.csv").replace("\\", "/")                                ,  #  Data CVS file path.
                  'Ts'              : 1/100e3            ,
                  'output_html'		: ("D:/4 WORKSPACE/24-OBC/OBC/0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/output_html.html").replace("\\", "/")                                  #  Data CVS file path.
                           
               }  
#?----------------------------------------------------------------------------------------------------------------------------------------	
scopes      =  {
				      'Scope'	    	   : "OBC/Scope"                                               ,  #                                 
               }	
PFC_glb     =  {
                  'L'               :  100e-6                                                   ,  #  Boost indutance in H.
                  'Rl'              :  1                                                        ,  #  DCR of inductor in Ω.
                  'Cout'               :  {
                                             'Config'		      : 4          ,  #  
                                             'Cap_s'    		   : 500e-6     ,  #  
                                             'Resr_s'		         : 19e-6      ,  #  
                                             'Lesl_s'		         : 0          ,  #  
                                             'Npara'		      : 1          ,  #  
                                             'Nseri'		      : 1          ,  #  
                                             'Vinit'		      : 0          ,  #  
                                             'Iinit'		      : 0             
                                          }                                                                        ,  #  Output Capacitance in F.
                  'CF'              :  100e3                                                    ,  #  Current control loop frequency in Hz.
                  'VF'              :  500                                                         #  Voltage control loop frequency in Hz.
               }

PFC_SW      =  {
                  'Config'               : 1                                                 ,  # 
                  'therm_mosfet'         : 'file:C3M0021120K'                                ,  # MOSFET thermal description
                  'Rgon'                 : 0,#2.5                                               ,  # external turn-on gate resistance (ohms)
                  'Rgoff'                : 0,#2.5                                               ,  # external turn-off gate resistance (ohms)
                  'Vdsmax'               : 1200                                              ,  # max device drain-source voltage rating (V)
                  'Idsmax'               : 100                                               ,  # max drain current rating @ 25 C(A)
                  'Tjmax'                : 175                                               ,  # max operating junction temperature (C)                        
                  'Tjmin'                : -40                                               ,  # min operating junction temperature (C)                       
                  'TcDerating'           : [-55,27,45,70,95,108,120,132,145,158,170,175]     ,  # Temperature derating curve (C)                       
                  'IdsMaxDerated'        : [100,100,95,86,77, 71, 65, 58, 49, 37, 20,  0]    ,  # Current derating curve (A)                     
                  'ron_mosfet'           : 0.021                                             ,  # MOSFET on-resistance  (ohms)
                  'Rds_off'              : 0                                                 ,  #
                  'Iinit'                : 0                                                 ,  #
                  'Coss'                 : {                                                    #
                                          'Config'		      : 6                              ,  #  
                                          'Cap_s'    		   : 1e-12                          ,  #  
                                          'Resr_s'		      : 0                              ,  #  
                                          'Lesl_s'		      : 0                              ,  #  
                                          'Npara'		      : 1                              ,  #  
                                          'Nseri'		      : 1                              ,  #  
                                          'Vinit'		      : 0                              ,  #  
                                          'Iinit'		      : 0             
                                          }                                                  ,
                  'vblock'               : 0                                                 ,  #
                  'Idrain'               : 0                                                 ,  #
                  'Trise'                : 0                                                 ,  #
                  'Tfall'                : 0                                                 ,  #
                  'therm_body_diode'     : 'file:C3M0021120K_bodydiode'                      ,  # body diode thermal description
                  'ron_body_diode'       : 0.033                                             ,  # diode on-resistance from body diode curve @25C & Vgs=0V (ohms)
                  'Rdb_off'              : 0                                                 ,  #
                  'vf_body_diode'        : 2.3                                               ,  # forward voltage diode from body diode curve @25C & Vgs=0V (V)
                  'BD_If'                : 0                                                 ,  #
                  'T_reverse'            : 0                                                 ,  #
                  'Q_reverse'            : 0                                                 ,  #            
                  'Ldr'                  : 0                                                 ,  #
                  'Ldr_Iinit'            : 0                                                 ,  #
                  'Lso'                  : 0                                                 ,  #
                  'Lso_Iinit'            : 0                                                 ,  #
                  'nPara'                : 0                                                 ,  #
                  'T_init'               : 25                                                ,  #
                  'Tamb'                 : 25                                                ,  # ambient temperature (C)
                  't_init'               : 25                                                ,  # initial junction temperature (C)
                  'rth_ch'               : 0.5                                               ,  # thermal resistance case-heatsink (grease) (K/W)
                  'Rth'                  : 0.34 					    	                           # thermal resistance heatsink-ambient (K/W)
               }
PFC         =  {
                  'R1'              : 4700/4                                                    ,  # [Ohm] - sensing resistor
                  'R2'              : 160/24                                                    ,  # [Ohm] - sensing resistor
                  'fs'              :  70e3                                                    ,  #  Switching frequency in Hz.
                  'C_Ts'            :  1/70e3                                                  ,  #  Sample time in s.
                  'C_Tp'            :  1*(1/70e3)                                              ,  #
                  'C_K1'            :  1                                                        ,  #  Sample time in s.
                  'C_Tn'            :  100e-6                                                   ,  #  Sample time in s.
                  'C_Ti'            :  2*(1/1)*(1*1/PFC_glb['CF'])                              ,  #  Sample time in s.
                  'C_Kp'            :  (PFC_glb['L'] /1)/(2*(1/1)*(1*1/PFC_glb['CF']))          ,  #  Sample time in s.
                  'C_Ki'            :  1/ (2*(1/1)*(1*1/70e3))                                 ,  #  Sample time in s.
                  'V_Ts'            :  1/PFC_glb['VF']                                          ,  #  Sample time in s.
                  'V_Tp'            :  1*(1/PFC_glb['VF'])                                      ,  # Equivalent delay (PWM delay + calculation delay) in s
                  'V_T2'            :  PFC_glb['Cout']['Cap_s']                                          ,  #  Sample time in s.
                  'V_Ti'            :  8/PFC_glb['Cout']['Cap_s']*math.pow((1*(1/PFC_glb['VF'])), 2)     ,  #  Sample time in s.
                  'V_Tn'            :  4*( 1*(1/PFC_glb['VF']))                                 ,  #  Sample time in s.
                  'V_Kp'            :  (4*( 1*(1/PFC_glb['VF'])) )/(8/PFC_glb['Cout']['Cap_s']
                                                *math.pow((1*(1/PFC_glb['VF'])), 2))            ,  #  Sample time in s.
                  'V_Ki'            :  1/(8/PFC_glb['Cout']['Cap_s']*math.pow((1*(1/PFC_glb['VF'])), 2)) ,  #  Sample time in s.
                  'HS1'             :  PFC_SW                                                   ,  #   
                  'HS2'             :  PFC_SW                                                   ,  #   
                  'LS1'             :  PFC_SW                                                   ,  #   
                  'LS2'             :  PFC_SW                                                      #   

               }		
DCLink      =  {
                  'Config'		      : 1                                  ,  #  DCLink Cap model Config.
                  'Cdc'    		   : 500e-3                                ,  #  DCLink Cap Capacitance.
                  'ESR'		         : 19e-6                                 ,  #  Series Resistance.
                  'ESL'		         : 0                                 ,  #  Series Inductance.
                  'nPara'		      : 1                                 ,  #  Number of Parallel Units.
                  'nSeri'		      : 1                                 ,  #  Number of Units in Series.
                  'Vinit'		      : 0                                 ,  #  DCLink Cap Initial Voltage.
                  'Iinit'		      : 0                                 ,  #  DCLink ESL Initial Current.

               }
Load      =  {
                  'Config'		      : 4                                    ,  #  DCLink Cap model Config.
                  'CL'    		      : 0                                ,  #  DCLink Cap Capacitance.
                  'RL'		         : (400*400)/7000                                ,  #  Series Resistance.
                  'LL'		         : 1e-9                                ,  #  Series Inductance.
                  # 'nPara'		      : 1                                ,  #  Number of Parallel Units.
                  # 'nSeri'		      : 1                                 ,  #  Number of Units in Series.
                  'Vinit'		      :0                                ,  #  DCLink Cap Initial Voltage.
                  'Iinit'		      : 0                                 ,  #  DCLink ESL Initial Current.
               }
LLC       =  {
    ## Sensing
                  'R1'               : 4700/4                   ,           # [Ohm] - sensing resistor
                  'R2'               : 160/24                   ,           # [Ohm] - sensing resistor
                  'V_DC'          : 400                   ,            # [V] - DC voltage source
                  'n_prim'          : 10                   ,            # [] - primary side turn number
                  'n_sndry'         : 2                   ,           # [] - secondary side turn number
                  ## Primary side
                  'L_r'               : 1.55e-6                   ,   		  # [H] - resonant inductor
                  'C_r'               : 1.2e-6                   ,   		  # [F] - resonant capacitor
                  ## Secondary side
                  'L'               : 1.6e-6                   ,   			  # [H] - output inductor
                  'C_o'               : 480e-6                   ,   		  # [F] - output capacitor
                  'C_v_init'               : 0                   ,   		  # [V] - output capacitor initial voltage
                  ## Controller
                  'sys_clk'               : 100e6                   ,   	  # [Hz] - 100 MHz
                  'max_period'               : 2000                   ,     # Maximum system period allowed
                  'min_period'               : 200                   ,   	  # Minimum system period allowed
                  ## Voltage change control
                  'SlewStep'               : 50/3                   ,     # [V/ms] - slew rate
                  'StartUpInc'               : 500                   ,      # [] - soft start frequency increment
                
                  'C_sense'               : 10e-9                   ,       # [F] - sensing capacitor
                  ## ADC conversion time
                  'adc_conv'               : 15                   ,         # [] - Number of system clock cycles required for ADC conversion
                  ## Dead time
                  'T_dt'               : 300e-9                   ,         # [s] - dead time
                  ## Thermal parameters 
                  # 'mosfet'               : 'file:C2M0025120D'                   ,      # MOSFET thermal description
                  'ron_mosfet'               : 30e-3                   ,    	          # MOSFET on resistance (ohms)
                  'vf_body_diode'               : 4.5                   ,    	       # diode forward voltage (V)
                  'ron_body_diode'               : 5e-3                   ,            # diode on resistance (ohms)
                  'rgon'               : 2.5                   ,    				       # external turn-on gate resistance (ohms) 
                  'rgoff'               : 2.5                   ,   				       # external turn-off gate resistance (ohms) 
                  'rth_ch'              : 0.1                   ,   		 		       # thermal resistance case-heatsink (grease) (K/W)
                  # 'diode'               : 'file:E4D20120G'                   ,   	# diode thermal description
                  'ron_diode'               : 1                   ,                # diode forward voltage (V)
                  'vf_diode'               : 1.4                   ,               # diode forward voltage (V) 
                  'rth_ch_diode'              : 0.5                   ,   		 	# thermal resistance case-heatsink (grease) (K/W)
                  'num_par_diode'               : 4                   ,            # Number of parallel diodes
                  'Rth'               : 0.1                   ,                    # Heatsink to ambient thermal resistance (K/W)
                  't_init'               : 25                     					# initial temperature (C)
             }

Grid      = {
       #? EVSE/Grid Parameters :-------------------------------- 
                  'Config'     :  2                                                                                         ,  #  1: 3PH config | 2: 1PH config . 
                  'Vin'             :  230                                                                                       ,  #  Input voltage in V (RMS)
                  'Fgrid'           :  50                                                                                        ,  #  Grid frequency in Hz
                  'Rg'              :  1e-3                                                                                        #  Grid bus resistance in ohm.  

}


#?----------------------------------------------------------------------------------------------------------------------------------------
ModelVars   =  {  'ToFile'          :  ToFile                                                                                    ,  #
                  'scopes'          :  scopes                                                                                    ,  #  scopes paths dictionary. 
                  'Sim_param'       :  Sim_param                                                                                 ,  #  simulation parameters dictionary.
                  'Grid'       :  Grid                                                                                 ,  #  simulation parameters dictionary.

                  #? AC Input Filter Parameters :--------------------------- 
                  'in_filter_config':  1                                                                                         ,  #  1: 1PH config | 2: pass .
                  'Cin'           :  1e-9                                                                                   ,  #  CM choke inductor value in H.
                   'Lin'           :  1e-9                                                                                   ,  #  CM choke inductor value in H.
                   'Ro'           :  1e-9                                                                                   ,  #  CM choke inductor value in H.

                  'L_CMC'           :  (1.5e-3)/2                                                                                    ,  #  CM choke inductor value in H.
                  'L_DMC'           :  (900e-6)/2                                                                                     ,  #  DM choke inductor value in H.
                  'Cx'              :  1e-6                                                                                    ,  #  X capacitor value in F.
                  'Cy1'             :  4.7e-9                                                                                    ,  #  Y capacitor 1 value in F.
                  'Cy2'             :  4.7e-9                                                                                    ,  #  Y capacitor 2 value in F.
                  'Cd'              :  100e-3                                                                                     ,  #  Damping Capacitor value in F.
                  'Rd'              :  470e3                                                                                      ,  #  Damping Resistor value in ohm.
                  #? PFC Parameters :--------------------------------------- 
                  'PFC_glb'         :  PFC_glb                                                                                   ,  #  PFC Parameters dictionary. 
                  'PFC'             :  PFC                                                                                       ,  #  PFC Parameters dictionary. 
                  #? DCLink Parameters :-------------------------------------- 
                  'DCLink'          :  DCLink                                                                                 ,  #  DC Link Capacitor dictionary.
                  #? LLC Parameters :-------------------------------------- 
                  'LLC'          :  LLC                                                                                 ,  #  DC Link Capacitor dictionary.
                  #? Load Parameters :-------------------------------------- 
                  'Vout'            :  400                                                                                       ,  #  Output voltage in V.
                  'Load'           :  Load                                                                                         #  Load resistance in Ω.
               }	
#?----------------------------------------------------------------------------------------------------------------------------------------			
