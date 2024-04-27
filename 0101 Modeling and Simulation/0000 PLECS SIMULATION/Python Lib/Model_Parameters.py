
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
ToFile      =  {   #! change dir to generic later
                  'ToFile_path'		: f'D:/4 WORKSPACE/24-OBC/OBC/0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/Results_{Sim_param['idx']}.csv',                     
                  'Ts'              : 0,
                  'output_html'     : f'D:/4 WORKSPACE/24-OBC/OBC/0101 Modeling and Simulation/0000 PLECS SIMULATION/Python Lib/output_html{Sim_param['idx']}.html',
                           
               }  
scopes      =  {
				      'Scope'	    	   : "OBC/Scope",                                
               }	
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
                  'R1'              :  4700/4,
                  'R2'              :  160/24,
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
                  'Config'		      : 4,  
                  'CL'    		      : 0, 
                  'Vout'            :  400,  
                  'RL'		         : 40,  
                  'LL'		         : 1e-9, 
                  'Vinit'		      : 0,  
                  'Iinit'		      : 0
               }
LLC         =  {
                  'R1'              : 4700/4,          
                  'R2'              : 160/24,          
                  'V_DC'            : 400,          
                  'n_prim'          : 10,            
                  'n_sndry'         : 2,          
                  'L_r'             : 1.55e-6,   		  
                  'C_r'             : 1.2e-6,   		 
                  'L'               : 1.6e-6,   			  
                  'C_o'             : 480e-6,   		 
                  'C_v_init'        : 0,   		  
                  'sys_clk'         : 100e6,   	  
                  'max_period'      : 2000,     
                  'min_period'      : 200,   	 
                  'SlewStep'        : 50/3,    
                  'StartUpInc'      : 500,     
                  'C_sense'         : 10e-9,       
                  'adc_conv'        : 15,       
                  'T_dt'            : 300e-9                          					
               }
Grid        =  {
                  'Config'          :  2,  
                  'Vin'             :  230,  
                  'Fgrid'           :  50,  
                  'Rg'              :  1e-3                                                                                  
               }
Thermals    =  {
                  'T_amb'           :  25.0,  
                  'rth_Amb'         :  0.09,  
               }
HV_Filter   =  {
                  'Config'         :  1,
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
ModelVars   =  {  'ToFile'          :  ToFile,
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