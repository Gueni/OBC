
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
                  'tSim'	    	   : 2.0,                                                                                             #? [s]     - Total simulation time
                  'load_tflip'	   : 2.0/2,                                                                                           #? [s]     - Time at which the load changes state 
                  'maxStep'		   : 1e-3,                                                                                            #? [s]     - Maximum simulation time step
                  'ZeroCross'       : 1000,                                                                                            #? [/]     - Zero-crossing detection limit
                  'rel_tol'		   : 1e-7                                                                                             #? [/]     - Relative tolerance for the numerical solver
               }
ToFile      = {   
                  'Ts'              : 0,                                                                                               #? [s]     - Sampling time for saving data
                  'tsave' 	    	   : Sim_param['tSim']-0.2                                                                            #? [s]     - Time point at which the data is saved
               }
Grid        = {
                  'Config'          : 1,                                                                                               #? [/]     - Configuration setting for the grid
                  'Vin'             : 230,                                                                                             #? [V]     - Input voltage of the grid
                  'Ts'              : 0,                                                                                               #? [s]     - Sampling time for grid operations
                  'f'               : 50,                                                                                              #? [Hz]    - Grid frequency
                  'phase'           : 0,                                                                                               #? [Hz]    - Grid frequency
                  'R'               : 0.01                                                                                             #? [Ohm]   - Grid resistance
               }
AC_Filter   = {
                  'Config'          : 5,                                                                                               #? [/]      - Configuration setting for the AC filter
                  'Cin'             : 1e-6,                                                                                            #? [F]      - Input capacitance
                  'L_CMC'           : 1.5e-3,                                                                                          #? [H]      - Common-mode choke inductance
                  'L_DMC'           : 900e-6,                                                                                          #? [H]      - Differential-mode choke inductance
                  'Cx'              : 0.1e-6,                                                                                          #? [F]      - X-capacitor value
                  'Cy1'             : 4.7e-12,                                                                                         #? [F]      - Y-capacitor value (first)
                  'Cy2'             : 4.7e-12,                                                                                         #? [F]      - Y-capacitor value (second)
                  'Ll'              : 10e-6                                                                                            #? [H]      - Filter inductor leakage inductance
               }
PFC         = {
                  'Config'          : 1,                                                                                               #? [/]      - Diode thermal description
                  'Choke'           : {
                     'Config'       : 1,                                                                                               #? [/]      - Diode thermal description
                     'L1'           : 1.5e-3,                                                                                          #? [H]      - Inductance of the first choke winding
                     'L2'           : 1.5e-3,                                                                                          #? [H]      - Inductance of the second choke winding
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
                     'ron_mosfet'   : 50e-3,                                                                                           #? [Ohm]    - MOSFET on-state resistance
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
DCLink      = {                                                                                             
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
HV_Filter   = {                                                                                             
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
                     'rth_Amb'               : 0.09                                                                                    #? [K/W]    - Thermal resistance from junction to ambient
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
                  'EMI Filter Current',
                  'EMI Filter Voltage',
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
                  'PFC HS2 voltage',
                  'PFC HS3 voltage',
                  'PFC LS1 voltage',
                  'PFC LS2 voltage',
                  'PFC LS3 voltage',
                  #!-------------------------
                  'PFC HS1 Current',
                  'PFC HS2 Current',
                  'PFC HS3 Current',
                  'PFC LS1 Current',
                  'PFC LS2 Current',
                  'PFC LS3 Current',
                  #!-------------------------
                  'PFC HS1 junction Temp',
                  'PFC HS2 junction Temp',
                  'PFC HS3 junction Temp',
                  'PFC LS1 junction Temp',
                  'PFC LS2 junction Temp',
                  'PFC LS3 junction Temp',
                  #!-------------------------
                  'PFC HS1 switching losses',
                  'PFC HS1 switching losses',
                  'PFC HS1 switching losses',
                  'PFC HS1 switching losses',
                  'PFC HS1 switching losses',
                  'PFC HS1 switching losses',
                  #!-------------------------
                  'PFC HS1 conduction losses',
                  'PFC HS1 conduction losses',
                  'PFC HS1 conduction losses',
                  'PFC HS1 conduction losses',
                  'PFC HS1 conduction losses',
                  'PFC HS1 conduction losses',
                  #!-------------------------
                  'PFC output capacitor voltage',
                  'PFC output capacitor current',
                  #!-------------------------
                  'DCLink capacitor voltage',
                  'DCLink capacitor current',
                  #!-------------------------
                  'Load voltage',
                  'Load current'
               ]		
Units       =  [                                                                                            
                  '[ V ]',                  
                  '[ A ]',                  
                  #!-------------------------
                  '[ A ]',                  
                  '[ V ]',                 
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
                  #!-------------------------
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
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',                  
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]',
                  #!-------------------------
                  '[ V ]',                  
                  '[ A ]'
               ]
#!----------------------------------------------------------------------------------------------------------------------------------------