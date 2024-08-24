
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
Sim_param 	      = {                                                                                            
                  'tSim'	    	   : 1.0,                                                                                             #? [s]     - Total simulation time
                  'load_tflip'	   : 1.0/2,                                                                                           #? [s]     - Time at which the load changes state 
                  'maxStep'		   : 1e-3,                                                                                            #? [s]     - Maximum simulation time step
                  'ZeroCross'       : 1000,                                                                                            #? [/]     - Zero-crossing detection limit
                  'rel_tol'		   : 1e-7                                                                                             #? [/]     - Relative tolerance for the numerical solver
               }
ToFile            = {   
                  'Ts'              : 0,                                                                                               #? [s]     - Sampling time for saving data
                  'tsave' 	    	   : Sim_param['tSim']-0.1                                                                            #? [s]     - Time point at which the data is saved
               }
Grid              = {
                  'Config'          : 1,                                                                                               #? [/]     - Configuration setting for the grid
                  'Vin'             : 230,                                                                                             #? [V]     - Input voltage of the grid
                  'Ts'              : 0,                                                                                               #? [s]     - Sampling time for grid operations
                  'f'               : 50,                                                                                              #? [Hz]    - Grid frequency
                  'phase'           : 0,                                                                                               #? [Hz]    - Grid frequency
                  'R'               : 0                                                                                                #? [Ohm]   - Grid resistance
               }
AC_Filter         = {
                  'Config'          : 5,                                                                                               #? [/]      - Configuration setting for the AC filter
                  'Cin'             : 1e-6,                                                                                            #? [F]      - Input capacitance
                  'L_CMC'           : 1.5e-3,                                                                                          #? [H]      - Common-mode choke inductance
                  'L_DMC'           : 900e-6,                                                                                          #? [H]      - Differential-mode choke inductance
                  'Cx'              : 0.1e-6,                                                                                          #? [F]      - X-capacitor value
                  'Cy1'             : 4.7e-12,                                                                                         #? [F]      - Y-capacitor value (first)
                  'Cy2'             : 4.7e-12,                                                                                         #? [F]      - Y-capacitor value (second)
                  'Ll'              : 10e-6                                                                                            #? [H]      - Filter inductor leakage inductance
               }
PFC               = {
                  'Config'          : 1,                                                                                               #? [/]      - Diode thermal description
                  'Choke'           : {
                     'Config'       : 1,                                                                                               #? [/]      - Diode thermal description
                     'L1'           : 1.5e-3,                                                                                          #? [H]      - Inductance of the first choke winding
                     'L2'           : 1.5e-3,                                                                                          #? [H]      - Inductance of the second choke winding
                     'R1'           : 1,                                                                                            #? [Ohm]    - Resistance of the first choke winding
                     'R2'           : 1,                                                                                            #? [Ohm]    - Resistance of the second choke winding
                     'Lm'           : 0.001,                                                                                           #? [H]      - Mutual inductance of the choke
                     'Rm'           : 0.001,                                                                                           #? [Ohm]    - Resistance of the mutual inductance
                     'i1'           : 0,                                                                                               #? [A]      - Initial current in the first choke winding
                     'i2'           : 0                                                                                                #? [A]      - Initial current in the second choke winding
                  },
                  'Cout'            : {
                           'Config' : 5,                                                                                               #? [/]      - Capacitance configuration
                           'Cap_s'  : 470e-6,                                                                                          #? [F]      - Capacitance value
                           'Resr_s' : 1e-12,                                                                                           #? [Ohm]    - Equivalent series resistance of the capacitance
                           'Lesl_s' : 1e-12,                                                                                           #? [H]      - Equivalent series inductance of the capacitance
                           'Npara'  : 5,                                                                                               #? [/]      - Number of parallel capacitors
                           'Nseri'  : 1,                                                                                               #? [/]      - Number of series capacitors
                           'Vinit'  : 0,                                                                                               #? [V]      - Initial voltage across the capacitance
                           'Iinit'  : 0                                                                                                #? [A]      - Initial current through the capacitance
                                    },
                  'SW'              : {
                     'Config'       : 1,                                                                                               #? [/]      - Switch configuration
                     'therm_mosfet' : 'file:C3M0021120K',                                                                              #? [/]      - MOSFET thermal model file path
                     'Rgon'         : 2.5,                                                                                             #? [Ohm]    - Gate resistance for turn-on
                     'Rgoff'        : 2.5,                                                                                             #? [Ohm]    - Gate resistance for turn-off
                     'ron_mosfet'   : 0,                                                                                               #? [Ohm]    - MOSFET on-state resistance
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
                     'rth_sw'          : 0.72,                                                                                         #? [K/W]    - Thermal resistance between the switch junction and case
                     'rth_ch'          : 62.5,                                                                                         #? [K/W]    - Thermal resistance between the case and heatsink
                     'Rth'             : 0.34                                                                                          #? [K/W]    - Total thermal resistance
                  }
               }
DCLink            = {                                                                                             
                      'Config'		   : 5,                                                                                            #? [/]      - Capacitance configuration
                      'Cap_s'    		: 100e-6,                                                                                       #? [F]      - Capacitance value 
                      'Resr_s'		   : 1e-12,                                                                                        #? [F]      - Equivalent series resistance of the capacitance
                      'Lesl_s'		   : 1e-12,                                                                                        #? [H]      - Equivalent series inductance of the capacitance
                      'Npara'		      : 10,                                                                                           #? [/]      - Number of parallel capacitors
                      'Nseri'		      : 1,                                                                                            #? [/]      - Number of series capacitors
                      'Vinit'		      : 0,                                                                                            #? [V]      - Initial voltage across the capacitance
                      'Iinit'		      : 0                                                                                             #? [A]      - Initial current through the capacitance   
                     }
LLC               = {
                     'R1'              : 4700/4,                                                                                       #? [Ohm]    - Resistor 1 value
                     'R2'              : 160/24,                                                                                       #? [Ohm]    - Resistor 2 value
                     'V_DC'            : 200,                                                                                          #? [V]      - DC voltage source
                     'n_prim'          : 4,                                                                                            #? [/]      - Primary side turn number
                     'n_sndry'         : 4,                                                                                            #? [/]      - Secondary side turn number
                     'L_r'             : 1.55e-6,                                                                                      #? [H]      - Resonant inductor
                     'L_k'             : 1.55e-6,                                                                                      #? [H]      - Resonant inductor
                     'L_k_Iinit'       : 0,                                                                                            #? [H]      - Initial inductance of resonant inductor
                     'L_r_Iinit'       : 0,                                                                                            #? [/]      - Initial current in resonant inductor
                     'Trafo'           : {
                        'Config'       : 1,                                                                                            #? [/]      - Transformer configuration
                        'n_prim'       : 4,                                                                                            #? [/]      - Primary side turn number
                        'n_sndry'      : 4,                                                                                            #? [/]      - Secondary side turn number
                        'Imaginit'     : 0,                                                                                            #? [/]      - Initial magnetizing current
                        'Lp'           : 1e-9,                                                                                         #? [H]      - Primary inductance
                        'Rp'           : 1e-2,                                                                                         #? [Ohm]    - Primary resistance
                        'Rc'           : 10,                                                                                           #? [Ohm]    - Core resistance
                        'Lm'           : 1e-9,                                                                                         #? [H]      - Magnetizing inductance
                        'Rs'           : 10,                                                                                           #? [Ohm]    - Secondary resistance
                        'Ls'           : 1e-9,                                                                                         #? [H]      - Secondary inductance
                        'LpIinit'      : 0,                                                                                            #? [H]      - Initial inductance of primary winding
                        'LmIinit'      : 0,                                                                                            #? [H]      - Initial inductance of magnetizing winding
                        'LsIinit'      : 0                                                                                             #? [H]      - Initial inductance of secondary winding
                        #                   Cross sectional Area m2 676e-6          Gap_CS_area 
                        # length of flux path m 1.5e-3*2            Gap_flux_len
                        # Initial MMF A 0                         Gap_init_MMF

                        # Cross sectional Area m2 676e-6          Core_CS_area 
                        # saturated relative permeability 1       Core_U_r_sat
                        # flux density saturation B_sat 0.49 T    Core_B_sat
                        # Initial MMF A 0                         Core_init_MMF
                        # unsaturated relative permeability 6500  Core_U_r_unsat
                        # length of flux path m 149e-3            Core_flux_len
                     },
                     'C_r'             : {
                        'Config'       : 1,                                                                                            #? [/]      - Capacitance configuration
                        'Cap_s'        : 1.2e-6,                                                                                       #? [F]      - Capacitance value
                        'Resr_s'       : 1e-10,                                                                                        #? [Ohm]    - Equivalent series resistance of the capacitance
                        'Lesl_s'       : 1e-10,                                                                                        #? [H]      - Equivalent series inductance of the capacitance
                        'Npara'        : 1,                                                                                            #? [/]      - Number of parallel capacitors
                        'Nseri'        : 1,                                                                                            #? [/]      - Number of series capacitors
                        'Vinit'        : 0,                                                                                            #? [V]      - Initial voltage across the capacitance
                        'Iinit'        : 0                                                                                             #? [A]      - Initial current through the capacitance
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
                           'Config'          : 1,                                                                                      #? [/]      - Configuration setting (e.g., 1 for enabled)
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
                        },
                     'Diode'                 : {
                        'diode'              : 'file:C4D40120D',                                                                       #? [/]      - diode thermal description       
                        'ron_diode'          : 1,                                                                                      #? [Ohm]    - diode forward resistance    
                        'vf_diode'           : 1.4,                                                                                    #? [V]      - diode forward voltage
                        'rth_ch_diode'       : 0.5,                                                                                    #? [K/W]    - Thermal resistance case-heatsink (grease)       
                        'num_par_diode'      : 4,                                                                                      #? [/]      - Number of parallel diodes      
                        'Rth'                : 0.1,                                                                                    #? [K/W]    - Heatsink to ambient thermal resistance    
                        't_init'             : 25                                                                                      #? [°C]      - Initial temperature   
                     }
                  }
CTRL              = {                                                                                             
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
HV_Filter         = {                                                                                             
                     'Config'                : 3,                                                                                      #? [/]      - Filter configuration
                     'Cy1'                   : {                                                                                        
                        'Config'             : 1,                                                                                      #? [/]      - Capacitance configuration
                        'Cap_s'              : 1e-3,                                                                                   #? [F]      - Capacitance value
                        'Resr_s'             : 0,                                                                                      #? [Ohm]    - Equivalent series resistance of the capacitance
                        'Lesl_s'             : 0,                                                                                      #? [H]      - Equivalent series inductance of the capacitance
                        'Npara'              : 1,                                                                                      #? [/]      - Number of parallel capacitors
                        'Nseri'              : 1,                                                                                      #? [/]      - Number of series capacitors
                        'Vinit'              : 0,                                                                                      #? [V]      - Initial voltage across the capacitance
                        'Iinit'              : 0                                                                                       #? [A]      - Initial current through the capacitance
                                                },                                                             
                     'Cy2'                   : {                                                                                 
                        'Config'             : 1,                                                                                      #? [/]      - Capacitance configuration
                        'Cap_s'              : 1e-3,                                                                                   #? [F]      - Capacitance value
                        'Resr_s'             : 0,                                                                                      #? [Ohm]    - Equivalent series resistance of the capacitance
                        'Lesl_s'             : 0,                                                                                      #? [H]      - Equivalent series inductance of the capacitance
                        'Npara'              : 1,                                                                                      #? [/]      - Number of parallel capacitors
                        'Nseri'              : 1,                                                                                      #? [/]      - Number of series capacitors
                        'Vinit'              : 0,                                                                                      #? [V]      - Initial voltage across the capacitance
                        'Iinit'              : 0                                                                                       #? [A]      - Initial current through the capacitance
                                                },                                                                 
                     'Cx'                    : {                                                                                      
                        'Config'             : 1,                                                                                      #? [/]      - Capacitance configuration
                        'Cap_s'              : 1e-3,                                                                                   #? [F]      - Capacitance value
                        'Resr_s'             : 0,                                                                                      #? [Ohm]    - Equivalent series resistance of the capacitance
                        'Lesl_s'             : 0,                                                                                      #? [H]      - Equivalent series inductance of the capacitance
                        'Npara'              : 1,                                                                                      #? [/]      - Number of parallel capacitors
                        'Nseri'              : 1,                                                                                      #? [/]      - Number of series capacitors
                        'Vinit'              : 0,                                                                                      #? [V]      - Initial voltage across the capacitance
                        'Iinit'              : 0                                                                                       #? [A]      - Initial current through the capacitance
                                                },                                                          
                     'L'                     : 40e-6,                                                                                  #? [H]      - Inductor value
                     'DMC'                   : {                                                                                       
                        'Config'             : 1,                                                                                      #? [/]      - 
                        'Cap_s'              : 1e-3,                                                                                   #? [/]      - 
                        'Resr_s'             : 0,                                                                                      #? [/]      - 
                        'Lesl_s'             : 0,                                                                                      #? [/]      - 
                        'Npara'              : 1,                                                                                      #? [/]      - 
                        'Nseri'              : 1,                                                                                      #? [/]      - 
                        'Vinit'              : 0,                                                                                      #? [/]      - 
                        'Iinit'              : 0                                                                                       #? [/]      - 
                                                }
                  
                  
                  
                  }
Load              = {
                     'Config'                : 1,                                                                                      #? [/]      - Configuration type for the load setup
                     'CL'                    : 0,                                                                                      #? [F]      - Load capacitance value
                     'R'                     : 50,                                                                                     #? [Ohm]    - Load resistance value
                     'LL'                    : 0,                                                                                      #? [H]      - Load inductance value
                     'Vinit'                 : 0,                                                                                      #? [V]      - Initial voltage across the load
                     'Iinit'                 : 0,                                                                                      #? [A]      - Initial current through the load
                     't_switch'              : Sim_param['tSim'] - Sim_param['load_tflip'],                                            #? [s]      - Time when the load switching occurs
                     't_dead'                : (Sim_param['tSim'] - Sim_param['load_tflip']) / 2                                       #? [s]      - Dead time for load switching
                  }
Thermals          = {
                     'T_amb'                 : 25.0,                                                                                   #? [°C]    - Ambient temperature
                     'rth_Amb'               : 0.09                                                                                    #? [K/W]   - Thermal resistance from junction to ambient
                  }
#!----------------------------------------------------------------------------------------------------------------------------------------
ModelVars   = {                                                                                             
                  'Sim_param'       :  Sim_param   ,      
                  'ToFile'          :  ToFile      ,
                  'Grid'            :  Grid        ,                                                                   
                  'AC_Filter'       :  AC_Filter   ,                                                           
                  'PFC'             :  PFC         ,                                                                 
                  'DCLink'          :  DCLink      ,                                                              
                  'LLC'             :  LLC         ,                                                                 
                  'CTRL'            :  CTRL        ,                                                            
                  'HV_Filter'       :  HV_Filter   ,   
                  'Load'            :  Load        ,                                                                
                  'Thermals'        :  Thermals    
               }	
#!----------------------------------------------------------------------------------------------------------------------------------------	
scopes      =  [                                                                                            
				      "OBC/Scope",                                                                             
				      "OBC/Scopes/grid_scope",                                                                 
				      "OBC/Scopes/EMI_scope",                                                                                         
                  "OBC/Scopes/grid vs filter",                                                             
				      "OBC/Scopes/PFC Input Output",                                                                                        
				      "OBC/Scopes/PFC Gates",                                                                                        
				      "OBC/Scopes/PFC Choke",                                                                                      
				      "OBC/Scopes/PFC SW Voltages",                                                                                    
				      "OBC/Scopes/PFC SW Currents",                                                                                    
				      "OBC/Scopes/PFC SW junction Temp",                                                                                    
				      "OBC/Scopes/PFC SW  case Temp",                                                                                  
				      "OBC/Scopes/PFC SW switching losses",                                                                                  
				      "OBC/Scopes/PFC SW conduction losses",                                                                                
				      "OBC/Scopes/PFC Cout",  
				      "OBC/Scopes/Efficiency",   
				      "OBC/Scopes/Load",                                                                                                                                                                                                                                                                                                                         
				      "OBC/Scopes/PFC TL"                                                                                 
				    
               ]	
Waveforms   =  [                                                                                            
                  'Grid Voltage',                  
                  'Grid Current',
                  #!-------------------------
                  'EMI Filter Voltage',
                  'EMI Filter Current',
                  #!-------------------------
                  'PFC Input Voltage',
                  'PFC Input Current',
                  'PFC output voltage',
                  'PFC output Current',
                  #!-------------------------
                  'PFC gates signal HS1',
                  'PFC gates signal LS1',
                  #!-------------------------
                  'PFC Input choke Winding 1 Current',
                  'PFC Input choke Winding 1 Voltage',
                  'PFC Input choke Winding 3 Current',
                  'PFC Input choke Winding 2 Voltage',
                  #!-------------------------
                  'PFC HS1 voltage',
                  'PFC Diode HS1 voltage',

                  'PFC HS2 voltage',
                  'PFC Diode HS2 voltage',

                  'PFC HS3 voltage',
                  'PFC Diode HS3 voltage',

                  'PFC LS1 voltage',
                  'PFC Diode LS1 voltage',

                  'PFC LS2 voltage',
                  'PFC Diode LS2 voltage',

                  'PFC LS3 voltage',
                  'PFC Diode LS3 voltage',

                  'PFC HS1 Current',
                  'PFC Diode HS1 Current',

                  'PFC HS2 Current',
                  'PFC Diode HS2 Current',

                  'PFC HS3 Current',
                  'PFC Diode HS3 Current',

                  'PFC LS1 Current',
                  'PFC Diode LS1 Current',

                  'PFC LS2 Current',
                  'PFC Diode LS2 Current',

                  'PFC LS3 Current',
                  'PFC Diode LS3 Current',

                  'PFC HS1 junction Temp',
                  'PFC Diode HS1 junction Temp',

                  'PFC HS2 junction Temp',
                  'PFC Diode HS2 junction Temp',

                  'PFC HS3 junction Temp',
                  'PFC Diode HS3 junction Temp',

                  'PFC LS1 junction Temp',
                  'PFC Diode LS1 junction Temp',

                  'PFC LS2 junction Temp',
                  'PFC Diode LS2 junction Temp',
                  
                  'PFC LS3 junction Temp',
                  'PFC Diode LS3 junction Temp',

                  'PFC case Temp HS1',
                  'PFC case Temp HS2',
                  'PFC case Temp HS3',
                  'PFC case Temp LS1',
                  'PFC case Temp LS2',
                  'PFC case Temp LS3',

                  'PFC HS1 switching losses',
                  'PFC Diode HS1 switching losses',
                  'PFC HS1 switching losses',
                  'PFC Diode HS1 switching losses',
                  'PFC HS1 switching losses',
                  'PFC Diode HS1 switching losses',
                  'PFC HS1 switching losses',
                  'PFC Diode HS1 switching losses',
                  'PFC HS1 switching losses',
                  'PFC Diode HS1 switching losses',
                  'PFC HS1 switching losses',
                  'PFC Diode HS1 switching losses',

                  'PFC HS1 conduction losses',
                  'PFC Diode HS1 conduction losses',
                  'PFC HS1 conduction losses',
                  'PFC Diode HS1 conduction losses',
                  'PFC HS1 conduction losses',
                  'PFC Diode HS1 conduction losses',
                  'PFC HS1 conduction losses',
                  'PFC Diode HS1 conduction losses',
                  'PFC HS1 conduction losses',
                  'PFC Diode HS1 conduction losses',
                  'PFC HS1 conduction losses',
                  'PFC Diode HS1 conduction losses',

                  'PFC output capacitor voltage',
                  'PFC output capacitor current',

                  'DCLink capacitor voltage',
                  'DCLink capacitor current',

                  'Load voltage',
                  'Load current'
                 
               ]		
Units       =  [                                                                                            
                  '[ V ]',                  
                  '[ A ]',                  
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',                 
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',    
                  '[ V ]',                  
                  '[ A ]',               
                  #!-------------------------
                  '[ V ]',                  
                  '[ V ]',                  
                  #!-------------------------
                  '[ A ]',                  
                  '[ V ]',                  
                  '[ A ]',                  
                  '[ V ]',                  
                  #!-------------------------
                  '[ V ]', 
                  '[ V ]', 
                  '[ V ]', 
                  '[ V ]', 
                  '[ V ]', 
                  '[ V ]', 
                  '[ V ]', 
                  '[ V ]', 
                  '[ V ]', 
                  '[ V ]', 
                  '[ V ]', 
                  '[ V ]', 
                  #!-------------------------
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  '[ A ]',                  
                  #!-------------------------
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  '[ C ]',                  
                  #!-------------------------
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  '[ W ]',                  
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',                  

                  '[ V ]',                  
                  '[ A ]',   
                  '[ V ]',                  
                  '[ A ]'

               ]
#!----------------------------------------------------------------------------------------------------------------------------------------