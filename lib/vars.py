#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?
#?           _   ______ ___________
#?          | | / / __ `/ ___/ ___/
#?          | |/ / /_/ / /  (__  )
#?          |___/\__,_/_/  /____/
#?
#?
#? Name:        vars.py
#? Purpose:     System parameters (7 kW EV OBC: TPB PFC + dual LLC): paths, configurations, modes, ModelVars structs.
#?              Every value carries '#? [unit] - comment' (shown in the HTML report).
#?              Required: MODEL_NAME, MODEL_PATH, DATA_DIR, PLECS_LIB_DIR, ModelVars (with ToFile).
#?              Optional: SIGNAL_LABELS, MODEL_IMG_PATH, F0_PATH, F0_OVERRIDES.
#?
#? Author:      Mohamed Gueni ( mohamedgueni@outlook.com)
#?
#? Created:     09/15/2024
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------
#? -------------------------------------------------------------------------------
import   copy
from     pathlib     import   Path
import   numpy       as       np
#? -------------------------------------------------------------------------------

#! All paths are resolved from this file's location, so the scripts work from any working directory.
LIB_DIR        =  Path(__file__).resolve().parent                    # <repo>/lib
ROOT_DIR       =  LIB_DIR.parent                                     # <repo>
MODEL_NAME     =  "OBC"                                              # model name (without .plecs extension)
MODEL_PATH     =  ROOT_DIR / "model" / f"{MODEL_NAME}.plecs"
MODEL_IMG_PATH =  ROOT_DIR / "asset" / "obc.png"
DATA_DIR       =  ROOT_DIR / "data"                                  # results: data/timeseries, data/mat, data/html, data/log, data/traces
PLECS_LIB_DIR  =  ROOT_DIR.parent / "0000_libraries" / "Plecs"      # PLECS libraries (Power, Switches ...): names of the probe signals
F0_PATH        =  ('Grid', 'f')                                      # fundamental of the harmonic plots (None = no harmonic plots)
F0_OVERRIDES   =  {                                                  # waveform name keyword -> its own fundamental (first match wins)
                  'HS1'             : ('CTRL', 'fsw'),                # fast leg switches at fsw
                  'LS1'             : ('CTRL', 'fsw'),
               }
TSIM           =  0.3                                              # simulation time [s] (PFC settled after ~75 ms, LLC enabled at CTRL.t_llc_en)
TSAVE          =  TSIM - 0.05                                      # time point at which the data is saved [s]
#? -------------------------------------------------------------------------------

Configs        =  {
                  'Grid'            : 1,                                                                                                                #? [/]     - EVSE/GRID: 1 1 PH, 2 3 PH
                  'AC_Filter'       : 1,                                                                                                                #? [/]     - Power/EMI FILTER: 1 1PH, 2 3PH, 3 Pass
                  'Cx'              : 2,                                                                                                                #? [/]     - EMI filter Cx, Passives/C: 1 Ideal, 2 Real
                  'Cx1'             : 2,                                                                                                                #? [/]     - EMI filter Cx1, Passives/C: 1 Ideal, 2 Real
                  'Cy1'             : 2,                                                                                                                #? [/]     - EMI filter Cy1, Passives/C: 1 Ideal, 2 Real
                  'Cy2'             : 2,                                                                                                                #? [/]     - EMI filter Cy2, Passives/C: 1 Ideal, 2 Real
                  'CMC'             : 2,                                                                                                                #? [/]     - EMI filter common-mode choke, Magnatic Components/Choke: 1 Ideal (L, Lm), 2 Real (+ R, Rm)
                  'DMC'             : 2,                                                                                                                #? [/]     - EMI filter differential-mode choke, Magnatic Components/Choke: 1 Ideal, 2 Real
                  'PFC'             : 1,                                                                                                                #? [/]     - Power/PFC (and PFC CTRL): 1 TPB 2 Leg, 2 TPB 3 Leg, 3 TPB Diodes
                  'PFC_Choke'       : 2,                                                                                                                #? [/]     - PFC boost choke, Magnatic Components/Choke: 1 Ideal (L, Lm), 2 Real (+ R, Rm)
                  'PFC_SW'          : 2,                                                                                                                #? [/]     - PFC switches, Switches/FET: 1 Ideal, 2 Real (physical equivalent circuit)
                  'PFC_SW_BD'       : 2,                                                                                                                #? [/]     - Body diode of the Real switch, Switches/D: 1 Ideal, 2 Real (charge-control recovery)
                  'DCLink'          : 2,                                                                                                                #? [/]     - DC-link capacitor, Passives/C: 1 Ideal, 2 Real
                  'LLC_Stage'       : 1,                                                                                                                #? [/]     - DUAL LLC (model subsystem): 1 Dual LLC (2 x Power/LLC in parallel), 2 Single LLC, 3 Pass (PFC only)
                  'LLC'             : 2,                                                                                                                #? [/]     - Power/LLC: 1 LLC SR (synchronous rectifier), 2 LLC AR (diode rectifier), 3 Pass
                  'LLC_SW'          : 1,                                                                                                                #? [/]     - LLC primary switches, Switches/FET: 1 Ideal, 2 Real
                  'LLC_SR'          : 1,                                                                                                                #? [/]     - LLC rectifier switches (LLC SR), Switches/FET: 1 Ideal, 2 Real
                  'Trafo'           : 1,                                                                                                                #? [/]     - LLC transformer, Magnatic Components/Tr: 1 Ideal, 2 Real (core + gap)
                  'LLC_CTRL'        : 1,                                                                                                                #? [/]     - LLC CTRL (model subsystem): 1 VF PI (output voltage), 2 Fixed frequency (CTRL.f_llc)
                  'HV_Filter'       : 3,                                                                                                                #? [/]     - Power/DC FILTER (LLC output): 1 Simple Model, 2 Pi, 3 Pass
                  'Load'            : 1,                                                                                                                #? [/]     - Passives/Load: 1 RL, 2 RL Parallel
                  'WarmStart'       : 0                                                                                                                 #? [/]     - Start: 0 from the pre-charge with soft start (TSIM), 1 at the operating point (Sim_param.warm_tSim)
               }
Sim_param      =  {
                  'tSim'            : TSIM,                                                                                                             #? [s]     - Total simulation time
                  'load_tflip'      : TSIM/2,                                                                                                           #? [s]     - Time at which the load changes state
                  'maxStep'         : 1e-3,                                                                                                             #? [s]     - Maximum simulation time step
                  'ZeroCross'       : 1000,                                                                                                             #? [/]     - Zero-crossing detection limit
                  'rel_tol'         : 1e-3,                                                                                                             #? [/]     - Relative tolerance for the numerical solver (PLECS default; 1e-7 was ~4x slower for < 0.02 % difference)
                  'warm_start'      : Configs['WarmStart'],                                                                                             #? [/]     - 1: start at the operating point (DC link at Vref, power loop at Pout, no soft start) for warm_tSim
                  'warm_tSim'       : 0.06,                                                                                                             #? [s]     - Simulation time with warm start (3 line cycles: load step after 1.5, last cycle saved)
                  'warm_t_en'       : 0.2e-3,                                                                                                           #? [s]     - Controller enable with warm start (sensor filters settled)
               }

#! Where each configuration is written in ModelVars (used to apply a mode).
CONFIG_PATHS   =  {
                  'Grid'            : [('Grid', 'Config')],
                  'AC_Filter'       : [('AC_Filter', 'Config')],
                  'Cx'              : [('AC_Filter', 'Cx', 'Config')],
                  'Cx1'             : [('AC_Filter', 'Cx1', 'Config')],
                  'Cy1'             : [('AC_Filter', 'Cy1', 'Config')],
                  'Cy2'             : [('AC_Filter', 'Cy2', 'Config')],
                  'CMC'             : [('AC_Filter', 'CMC', 'Config')],
                  'DMC'             : [('AC_Filter', 'DMC', 'Config')],
                  'PFC'             : [('PFC', 'Config')],
                  'PFC_Choke'       : [('PFC', 'Choke', 'Config')],
                  'PFC_SW'          : [('PFC', 'SW', 'Config')],
                  'PFC_SW_BD'       : [('PFC', 'SW', 'therm_body_diode', 'Config')],
                  'DCLink'          : [('DCLink', 'Config')],
                  'LLC_Stage'       : [('LLC', 'Stage')],
                  'LLC'             : [('LLC', 'Config')],
                  'LLC_SW'          : [('LLC', 'HS1', 'Config')],
                  'LLC_SR'          : [('LLC', 'SRHS1', 'Config')],
                  'Trafo'           : [('LLC', 'Trafo', 'Config')],
                  'LLC_CTRL'        : [('CTRL', 'LLC_Config')],
                  'HV_Filter'       : [('HV_Filter', 'Config')],
                  'Load'            : [('Load', 'Config')],
                  'WarmStart'       : [('Sim_param', 'warm_start')]
               }

#! Modes: configuration presets selected in main.py with MODE (None = Configs as above). Grid, PFC / LLC topology, LLC
#! stage, controllers and load keep their Configs value.
MODES          =  {
                  'ideal'           : {'AC_Filter': 3, 'Cx': 1, 'Cx1': 1, 'Cy1': 1, 'Cy2': 1, 'CMC': 1, 'DMC': 1, 'PFC_Choke': 1, 'DCLink': 1, 'PFC_SW': 1, 'PFC_SW_BD': 1, 'LLC_SW': 1, 'LLC_SR': 1, 'Trafo': 1, 'WarmStart': 0},   #? [/]     - EMI filter Pass, ideal capacitors, chokes and switches (DC link starts at 0 V, see Derived): fastest
                  'real'            : {'AC_Filter': 1, 'Cx': 2, 'Cx1': 2, 'Cy1': 2, 'Cy2': 2, 'CMC': 2, 'DMC': 2, 'PFC_Choke': 2, 'DCLink': 2, 'PFC_SW': 2, 'PFC_SW_BD': 2, 'LLC_SW': 2, 'LLC_SR': 2, 'Trafo': 2, 'WarmStart': 1}    #? [/]     - EMI filter on, real capacitors and chokes, physical switches and body diodes (switching detail, slow)
               }
ToFile         =  {
                  'Ts'              : 0,                                                                                                                #? [s]     - Sampling time for saving data
                  'tsave'           : TSAVE,                                                                                                            #? [s]     - Time point at which the data is saved
               }
Grid           =  {                                                                                                                                          # EVSE / grid source
                  'Config'          : Configs['Grid'],                                                                                                   #? [/]     - Configuration of the grid: 1 1 PH, 2 3 PH
                  'Vin'             : 230,                                                                                                               #? [V]     - Input voltage of the grid
                  'Ts'              : 1/80e3,                                                                                                            #? [s]     - Sampling time for grid operations
                  'f'               : 50,                                                                                                                #? [Hz]    - Grid frequency
                  'phase'           : 0,                                                                                                                 #? [rad]   - Grid voltage phase angle
                  'R'               : 0                                                                                                               #? [Ohm]   - Grid resistance
               }
AC_Filter      =  {                                                                                                                                   # Power/EMI FILTER, 1PH: CMC -> Cx, Cy1/Cy2 -> L1/L5 (Ll) -> DMC -> Cx1 // (Rd + Cd) -> PFC
                                                                                                                                                     # two-stage DM filter: stage 1 = CMC leakage + Cx (~23 kHz), stage 2 = DMC + Ll + Cx1 (~10 kHz),
                                                                                                                                                     # ~80 dB DM attenuation at 2*fsw = 160 kHz; Rd + Cd = optimum parallel damping of stage 2 (n = Cd/Cx1 = 4)
                  'Config'        : Configs['AC_Filter'],                                                                                             #? [/]      - Configuration of the EMI filter (1 = 1PH, 2 = 3PH, 3 = Pass)
                  'Ll'            : 2e-6,                                                                                                             #? [H]      - Line / neutral series inductance L1, L5 (wiring between the two stages)
                  'CMC'           : {                                                                                                                 # common-mode choke, 2 coupled windings (nanocrystalline, 10 A)
                     'Config'     : Configs['CMC'],                                                                                                   #? [/]      - 1 Ideal (L, Lm), 2 Real (+ R, Rm) (Magnatic Components/Choke)
                     'L1'         : 4.7e-3,                                                                                                           #? [H]      - Self inductance of winding 1 (CMC 4.7 mH; leakage 23.5 uH per winding = stage-1 DM inductance)
                     'L2'         : 4.7e-3,                                                                                                           #? [H]      - Self inductance of winding 2 (CMC 4.7 mH; leakage 23.5 uH per winding = stage-1 DM inductance)
                     'R1'         : 30e-3,                                                                                                            #? [Ohm]    - DC resistance of winding 1
                     'R2'         : 30e-3,                                                                                                            #? [Ohm]    - DC resistance of winding 2
                     'Lm'         : 0.995 * 4.7e-3,                                                                                                   #? [H]      - Mutual inductance (coupling k = 0.995; leakage L - Lm per winding)
                     'Rm'         : 0,                                                                                                                #? [Ohm]    - Mutual resistance
                     'i1'         : 0,                                                                                                                #? [A]      - Initial current in winding 1
                     'i2'         : 0                                                                                                                 #? [A]      - Initial current in winding 2
                  },
                  'DMC'           : {                                                                                                                 # differential-mode choke, 2 uncoupled windings (powder core, 10 A)
                     'Config'     : Configs['DMC'],                                                                                                   #? [/]      - 1 Ideal (L, Lm), 2 Real (+ R, Rm) (Magnatic Components/Choke)
                     'L1'         : 120e-6,                                                                                                           #? [H]      - Self inductance of winding 1 (DM choke 120 uH)
                     'L2'         : 120e-6,                                                                                                           #? [H]      - Self inductance of winding 2 (DM choke 120 uH)
                     'R1'         : 25e-3,                                                                                                            #? [Ohm]    - DC resistance of winding 1
                     'R2'         : 25e-3,                                                                                                            #? [Ohm]    - DC resistance of winding 2
                     'Lm'         : 0,                                                                                                                #? [H]      - Mutual inductance (coupling k = 0; leakage L - Lm per winding)
                     'Rm'         : 0,                                                                                                                #? [Ohm]    - Mutual resistance
                     'i1'         : 0,                                                                                                                #? [A]      - Initial current in winding 1
                     'i2'         : 0                                                                                                                 #? [A]      - Initial current in winding 2
                  },
                  'Cx'            : {                                                                                                                 # X2 capacitor, grid side (Passives/C)
                     'Config'     : Configs['Cx'],                                                                                                      #? [/]      - 1 Ideal, 2 Real (Passives/C)
                     'Cap_s'      : 1e-6,                                                                                                             #? [F]      - X2 film capacitance, 1 uF / 310 VAC
                     'Resr_s'     : 10e-3,                                                                                                            #? [Ohm]    - Equivalent series resistance (used with Config 2)
                     'Lesl_s'     : 10e-9,                                                                                                            #? [H]      - Equivalent series inductance (used with Config 2)
                     'Npara'      : 1,                                                                                                                #? [/]      - Number of parallel capacitors
                     'Nseri'      : 1,                                                                                                                #? [/]      - Number of series capacitors
                     'Vinit'      : 0,                                                                                                                #? [V]      - Initial voltage
                     'Iinit'      : 0                                                                                                                 #? [A]      - Initial current
                  },
                  'Cx1'           : {                                                                                                                 # X2 capacitor, PFC side (Passives/C)
                     'Config'     : Configs['Cx1'],                                                                                                     #? [/]      - 1 Ideal, 2 Real (Passives/C)
                     'Cap_s'      : 1e-6,                                                                                                             #? [F]      - X2 film capacitance, 1 uF / 310 VAC
                     'Resr_s'     : 10e-3,                                                                                                            #? [Ohm]    - Equivalent series resistance (used with Config 2)
                     'Lesl_s'     : 10e-9,                                                                                                            #? [H]      - Equivalent series inductance (used with Config 2)
                     'Npara'      : 1,                                                                                                                #? [/]      - Number of parallel capacitors
                     'Nseri'      : 1,                                                                                                                #? [/]      - Number of series capacitors
                     'Vinit'      : 0,                                                                                                                #? [V]      - Initial voltage
                     'Iinit'      : 0                                                                                                                 #? [A]      - Initial current
                  },
                  'Rd'            : 10,                                                                                                               #? [Ohm]    - Damping resistor in series with Cd across Cx1 (~0.6 * sqrt(L_stage2 / Cx1))
                  'Cd'            : 4e-6,                                                                                                             #? [F]      - Damping capacitor (n = Cd / Cx1 = 4), X2 film 4 uF
                  'Cy1'           : {                                                                                                                 # Y capacitor line -> PE (Passives/C)
                     'Config'     : Configs['Cy1'],                                                                                                     #? [/]      - 1 Ideal, 2 Real (Passives/C)
                     'Cap_s'      : 2.2e-9,                                                                                                           #? [F]      - Y1 ceramic capacitance, 2.2 nF (leakage < 0.2 mA at 265 V)
                     'Resr_s'     : 0.2,                                                                                                              #? [Ohm]    - Equivalent series resistance (used with Config 2)
                     'Lesl_s'     : 0,                                                                                                                #? [H]      - Equivalent series inductance (0: a Y-cap ESL with ideal-edge commutation forces a current jump; resonance ~48 MHz, not resolved)
                     'Npara'      : 1,                                                                                                                #? [/]      - Number of parallel capacitors
                     'Nseri'      : 1,                                                                                                                #? [/]      - Number of series capacitors
                     'Vinit'      : 0,                                                                                                                #? [V]      - Initial voltage
                     'Iinit'      : 0                                                                                                                 #? [A]      - Initial current
                  },
                  'Cy2'           : {                                                                                                                 # Y capacitor neutral -> PE (Passives/C)
                     'Config'     : Configs['Cy2'],                                                                                                     #? [/]      - 1 Ideal, 2 Real (Passives/C)
                     'Cap_s'      : 2.2e-9,                                                                                                           #? [F]      - Y1 ceramic capacitance, 2.2 nF (leakage < 0.2 mA at 265 V)
                     'Resr_s'     : 0.2,                                                                                                              #? [Ohm]    - Equivalent series resistance (used with Config 2)
                     'Lesl_s'     : 0,                                                                                                                #? [H]      - Equivalent series inductance (0: a Y-cap ESL with ideal-edge commutation forces a current jump; resonance ~48 MHz, not resolved)
                     'Npara'      : 1,                                                                                                                #? [/]      - Number of parallel capacitors
                     'Nseri'      : 1,                                                                                                                #? [/]      - Number of series capacitors
                     'Vinit'      : 0,                                                                                                                #? [V]      - Initial voltage
                     'Iinit'      : 0                                                                                                                 #? [A]      - Initial current
                  }
               }

#! Switch library: one entry per device of the PLECS Thermal Lib (/0000_libraries/Plecs/Thermal Lib).
#! PFC['SW'] takes a copy of the device selected by PFC_SWITCH.
Switches       =  {
                  'C3M0021120K'    : {                                                                                                                # Wolfspeed C3M0021120K, 1200 V / 100 A / 21 mOhm SiC MOSFET (selected)
                     'Config'         : Configs['PFC_SW'],                                                                                            #? [/]      - FET config: 1 Ideal, 2 Real (physical equivalent circuit, fields Drv ... Th below)
                     'therm_mosfet'   : 'file:C3M0021120K',                                                                                           #? [/]      - Thermal description of the switch (Thermal Lib)
                     'Rgon'           : 2.5,                                                                                                          #? [Ohm]    - External turn-on gate resistance
                     'Rgoff'          : 2.5,                                                                                                          #? [Ohm]    - External turn-off gate resistance
                     'ron_mosfet'     : 21e-3,                                                                                                        #? [Ohm]    - R_DS(on) at 25 °C (C3M0021120K: 21 mOhm typ, 1200 V / 100 A)
                     'Iinit'          : 0,                                                                                                            #? [A]      - Initial current through the switch
                     'therm_body_diode': {                                                                                                            # body diode (Switches/D), used by FET config 2 (Real)
                        'Config'        : Configs['PFC_SW_BD'],                                                                                         #? [/]     - Diode config: 1 Ideal (vf_diode, ron_diode), 2 Real (charge-control recovery)
                        #! ---- config 1: Ideal (uses vf_diode, ron_diode)
                        'therm_diode'   : 'file:C3M0021120K_bodydiode',                                                                               #? [/]      - Thermal description of the body diode (Thermal Lib, not used by the Ideal / Real configs)
                        'vf_diode'      : 4.5,                                                                                                        #? [V]      - Body diode forward voltage
                        'ron_diode'     : 5e-3,                                                                                                       #? [Ohm]    - Body diode on-state resistance
                        't_init'        : 25,                                                                                                         #? [°C]     - Initial junction temperature of the body diode
                        'num_par_diode' : 1,                                                                                                          #? [/]      - Number of parallel diodes
                        'Case_Cth'      : 0,                                                                                                          #? [J/K]    - Thermal capacitance of the diode case node (0: no extra thermal state, ~4x faster)
                        'Case_Tinit'    : 25,                                                                                                         #? [°C]     - Initial temperature of the diode case node
                        'Case_Amb_rth'  : 0.1,                                                                                                        #? [K/W]    - Thermal resistance diode case -> switch thermal port
                        #! ---- config 2: Real (charge-control reverse recovery), used as a die-level body diode
                        'nPara'         : 1,                                                                                                          #? [/]      - Number of parallel diodes (= nPara of the switch)
                        'VI'            : {                                                                                                           # forward curve at Vgs = -4 V (vendor table), I = 0 column = knee voltage
                           'T'          : [-40, 25, 175],                                                                                             #? [°C]     - Temperature axis
                           'I'          : [0, 0.5, 2, 5, 8, 15, 20, 30, 40, 60, 80, 100, 120, 140, 160, 180, 200],                                    #? [A]      - Current axis
                           'V'          : [[2.85, 3.00, 3.50, 3.90, 4.15, 4.60, 4.77, 5.10, 5.42, 5.90, 6.30, 6.59, 6.90, 7.14, 7.40, 7.60, 7.84],    #? [V]      - Forward voltage, one row per temperature
                                           [2.75, 2.90, 3.15, 3.50, 3.75, 4.10, 4.30, 4.66, 4.89, 5.37, 5.77, 6.10, 6.40, 6.65, 6.90, 7.13, 7.35],
                                           [2.30, 2.45, 2.74, 3.10, 3.30, 3.60, 3.80, 4.12, 4.40, 4.78, 5.16, 5.46, 5.75, 6.00, 6.25, 6.47, 6.70]]
                        },
                        'Ron'           : 0.012,                                                                                                      #? [Ohm]    - Storage-phase branch resistance
                        'RR'            : {                                                                                                           # datasheet recovery test (its Qrr of 928 nC includes Coss -> trr + Irrm used)
                           'IF'         : 50,                                                                                                         #? [A]      - Forward current
                           'didt'       : 2600e6,                                                                                                     #? [A/s]    - Turn-off slope
                           'Irrm'       : 42,                                                                                                         #? [A]      - Peak reverse current (0 = no stored charge)
                           'trr'        : 34e-9,                                                                                                      #? [s]      - Reverse recovery time (0 -> Qrr used)
                           'Qrr'        : 0,                                                                                                          #? [C]      - Junction recovery charge
                           'Tmeas'      : 175,                                                                                                        #? [°C]     - Test junction temperature
                           'ktau'       : 2.0                                                                                                         #? [/]      - Lifetime temperature exponent
                        },
                        'Cj'            : {'V': [0], 'C': [1e-12]},                                                                                   #? [V],[F]  - Junction capacitance (already part of Coss)
                        'Roff'          : 1e9,                                                                                                        #? [Ohm]    - Leakage resistance
                        'Aval'          : {'Vbr': 0, 'Rav': 1},                                                                                       #? [V],[Ohm] - Disabled (avalanche is in the channel model)
                        'FR'            : {'Vfr': 0.5, 'IF': 50, 'tfr': 0},                                                                           #? [V],[A],[s] - No forward recovery (tfr = 0); Vfr/IF = 10 mOhm across the recovery L keeps the junction solvable (1 uOhm floor: ~16x slower)
                        'Pkg'           : {'La': 0, 'Lk': 0, 'Rp': 100},                                                                              #? [H],[H],[Ohm] - No package: the FET package is in series
                        'Th'            : {'Rth': [1e-3], 'Cth': [1e-4], 'Tinit': 25}                                                                 #? [K/W],[J/K],[°C] - Die -> FET junction (same die: near zero)
                     },
                     'nPara'          : 1,                                                                                                            #? [/]      - Number of parallel switches
                     'T_init'         : 25,                                                                                                           #? [°C]     - Initial junction temperature
                     'Tamb'           : 25,                                                                                                           #? [°C]     - Ambient temperature
                     't_init'         : 25,                                                                                                           #? [°C]     - Initial temperature of the thermal chain
                     'rth_sw'         : 0.1,                                                                                                          #? [K/W]    - Thermal resistance junction -> case
                     'rth_ch'         : 0.1,                                                                                                          #? [K/W]    - Thermal resistance case -> heatsink (TIM)
                     'Rth'            : 0.2,                                                                                                          #? [K/W]    - Total thermal resistance junction -> heatsink
                     'foster_rth'     : [0.0472 ,0.0688],                                                                                             #? [/]      - Foster representation of the thermal resistance
                     'foster_cth'     : [0.95 , 2.4],                                                                                                 #? [/]      - Foster representation of the thermal capacitance
                     #! ---- FET config 2 (Real): physical equivalent circuit (datasheet Rev.4 + vendor Thermal Lib model, see 0000_libraries/Plecs/Device Models/C3M0021120K.m)
                     'Drv'            : {                                                                                                             # gate driver (totem pole, separate on/off paths)
                        'Von'     : 15,                                                                                                               #? [V]      - Turn-on gate voltage
                        'Voff'    : -4,                                                                                                               #? [V]      - Turn-off gate voltage
                        'Rgon'    : 2.5,                                                                                                              #? [Ohm]    - External turn-on resistance incl. driver
                        'Rgoff'   : 2.5                                                                                                               #? [Ohm]    - External turn-off resistance incl. driver
                     },
                     'Pkg'            : {                                                                                                             # package parasitics (TO-247-4 estimates)
                        'Lg'      : 7e-9,                                                                                                             #? [H]      - Gate lead + bond wire
                        'Ld'      : 4.5e-9,                                                                                                           #? [H]      - Drain tab + bond
                        'Ls'      : 6e-9,                                                                                                             #? [H]      - Power source lead
                        'Lcs'     : 1e-9,                                                                                                             #? [H]      - Common source (gate + power loop); ~7 nH for a TO-247-3
                        'Lk'      : 6e-9,                                                                                                             #? [H]      - Kelvin source lead
                        'Rp'      : 20                                                                                                                #? [Ohm]    - Damping resistance across each lead inductance (~4.5x the lead/Coss impedance: realistic ringing; 100 Ohm rang ~1.7x longer to simulate, same losses)
                     },
                     'Rg_int'         : 3.3,                                                                                                          #? [Ohm]    - Internal gate resistance
                     'Ch'             : {                                                                                                             # channel (fitted to Fig. 1-3, 6, 11 and the vendor Vds(Id, Tj) tables)
                        'Vt0'     : 3.1058,                                                                                                           #? [V]      - Effective threshold at 25 °C
                        'aVt'     : 0,                                                                                                                #? [V/K]    - Threshold temperature coefficient
                        'nphi0'   : 0.38494,                                                                                                          #? [V]      - Subthreshold slope voltage at 25 °C
                        'K0'      : 4.9771,                                                                                                           #? [A/V²]   - Transconductance factor at 25 °C
                        'bK'      : 0.94102,                                                                                                          #? [/]      - K ~ (T/298 K)^bK
                        'Rd0'     : 3.2856e-3,                                                                                                        #? [Ohm]    - JFET/drift resistance at 25 °C
                        'bRd'     : 4.89,                                                                                                             #? [/]      - Rd ~ (T/298 K)^bRd
                        'Iq0'     : 220.62,                                                                                                           #? [A]      - Drift quasi-saturation current at 25 °C
                        'bIq'     : 0.09561,                                                                                                          #? [/]      - Iq ~ (T/298 K)^bIq
                        'theta'   : 0,                                                                                                                #? [1/V]    - Mobility degradation
                        'lambda'  : 1.1658e-4,                                                                                                        #? [1/V]    - Channel length modulation
                        'm'       : 2.7144                                                                                                            #? [/]      - Linear/saturation transition sharpness
                     },
                     'Cap'            : {                                                                                                             # capacitances (Fig. 17/18 at Vgs = 0 V)
                        'V'       : [0, 1, 2, 5, 10, 20, 30, 50, 75, 100, 150, 200, 300, 400, 600, 800, 1000, 1200],                                  #? [V]      - Voltage axis
                        'Coss'    : [c * 1e-12 for c in [4300, 3300, 2700, 1900, 1300, 950, 820, 650, 560, 500, 420, 360, 280, 235, 195, 182, 180, 180]], #? [F] - Output capacitance
                        'Crss'    : [c * 1e-12 for c in [1000, 800, 600, 250, 80, 45, 38, 30, 26, 23, 19, 17, 14.5, 13, 12, 12, 12, 12.3]],           #? [F]      - Reverse transfer capacitance
                        'Ciss'    : 4818e-12,                                                                                                         #? [F]      - Input capacitance ...
                        'Vciss'   : 1000,                                                                                                             #? [V]      - ... measured at this Vds
                        'Cgd_ox'  : 3.4e-9,                                                                                                           #? [F]      - Gate-drain oxide capacitance for Vdg < 0 (from Fig. 12)
                        'kdyn'    : 1.7,                                                                                                              #? [/]      - Large-signal Cgd factor with inverted channel (from Fig. 25/27)
                        'Vacc'    : 1.0                                                                                                               #? [V]      - Cgd accumulation transition width
                     },
                     'Leak'           : {
                        'Idss'    : 1e-6,                                                                                                             #? [A]      - Drain leakage ...
                        'Vdss'    : 1200,                                                                                                             #? [V]      - ... at this Vds
                        'Igss'    : 10e-9,                                                                                                            #? [A]      - Gate leakage ...
                        'Vgss'    : 15                                                                                                                #? [V]      - ... at this Vgs
                     },
                     'Aval'           : {
                        'Vbr'     : 1500,                                                                                                             #? [V]      - Avalanche onset (datasheet guarantees >= 1200 V)
                        'Rav'     : 0.5                                                                                                               #? [Ohm]    - Avalanche dynamic resistance
                     },
                     'Th'             : {                                                                                                             # junction -> Ambient port (vendor Cauer chain, sum 0.324 K/W)
                        'Rth'     : [0.0441, 0.104, 0.06378, 0.1121],                                                                                 #? [K/W]    - Cauer resistances
                        'Cth'     : [0.002214, 0.0126, 0.03416, 0.1294],                                                                              #? [J/K]    - Cauer capacitances
                        'Tinit'   : 25                                                                                                                #? [°C]     - Initial temperature
                     }
                  }
               }
PFC_SWITCH     = 'C3M0021120K'                                                                                                                           # device of Switches used by the PFC stage
PFC            =  {
                  'Config'          : Configs['PFC'],                                                                                                    #? [/]     - Configuration of the PFC stage (also selects the PFC CTRL configuration)
                  'Choke'           : {                                                                                                                  # boost choke (Magnatic Components/Choke)
                     'Config'       : Configs['PFC_Choke'],                                                                                              #? [/]      - 1 Ideal (L, Lm), 2 Real (+ R, Rm)
                     'L1'           : 90e-6,                                                                                                           #? [H]      - Inductance of the first choke winding (boost inductor; L_boost = 98 uH -> 13 A p-p = 30 % of the 43 A line peak at 7 kW / 230 V, 80 kHz)
                     'L2'           : 10e-6,                                                                                                             #? [H]      - Inductance of the second choke winding
                     'R1'           : 0.01,                                                                                                              #? [Ohm]    - Resistance of the first choke winding
                     'R2'           : 0.01,                                                                                                              #? [Ohm]    - Resistance of the second choke winding
                     'Lm'           : 1e-6,                                                                                                              #? [H]      - Mutual inductance of the choke
                     'Rm'           : 0.001,                                                                                                             #? [Ohm]    - Resistance of the mutual inductance
                     'i1'           : 0,                                                                                                                 #? [A]      - Initial current in the first choke winding
                     'i2'           : 0                                                                                                                  #? [A]      - Initial current in the second choke winding
                  },
                  'Cout'            : 10e-6,                                                                                                             #? [F]      - PFC output (HF decoupling) capacitance
                  'SW'              : copy.deepcopy(Switches[PFC_SWITCH])                                                                             # selected switch (see Switches / PFC_SWITCH)
               }
DCLink         =  {
                  'Config'          : Configs['DCLink'],                                                                                                #? [/]      - Capacitance configuration: 1 Ideal, 2 Real
                  'Cap_s'           : 470e-6,                                                                                                            #? [F]      - Capacitance value
                  'Resr_s'          : 50e-3,                                                                                                            #? [Ohm]    - Equivalent series resistance of the capacitance
                  'Lesl_s'          : 20e-9,                                                                                                            #? [H]      - Equivalent series inductance of the capacitance
                  'Npara'           : 4,                                                                                                                #? [/]      - Number of parallel capacitors (1.88 mF: ~15 V p-p 100 Hz ripple at 7 kW)
                  'Nseri'           : 1,                                                                                                                #? [/]      - Number of series capacitors
                  'Vinit'           : -2**0.5 * Grid['Vin'],                                                                                            #? [V]      - Initial voltage: line peak, inrush bypass assumed (negative: CDC is placed flipped)
                  'Iinit'           : 0                                                                                                                 #? [A]      - Initial current through the capacitance
               }
def _switch(config):
   """Copy of the LLC device with its FET configuration (body diode Ideal)."""
   sw                               = copy.deepcopy(Switches[LLC_SWITCH])
   sw['Config']                     = config
   sw['therm_body_diode']['Config'] = 1
   return sw


def _cap(value, esr=1e-3, esl=1e-9, config=1):
   """Passives/C dictionary."""
   return {
                     'Config'       : config,                                                                                                           #? [/]      - 1 Ideal, 2 Real
                     'Cap_s'        : value,                                                                                                            #? [F]      - Capacitance
                     'Resr_s'       : esr,                                                                                                              #? [Ohm]    - Equivalent series resistance (Config 2)
                     'Lesl_s'       : esl,                                                                                                              #? [H]      - Equivalent series inductance (Config 2)
                     'Npara'        : 1,                                                                                                                #? [/]      - Number of parallel capacitors
                     'Nseri'        : 1,                                                                                                                #? [/]      - Number of series capacitors
                     'Vinit'        : 0,                                                                                                                #? [V]      - Initial voltage
                     'Iinit'        : 0                                                                                                                 #? [A]      - Initial current
          }


LLC_SWITCH     = 'C3M0021120K'                                                                                                                          # device of Switches used by the LLC primary and rectifier
LLC            =  {                                                                                                                                     # Power/LLC (full-bridge primary, full-bridge rectifier); DUAL LLC runs two in parallel
                  'Stage'           : Configs['LLC_Stage'],                                                                                             #? [/]      - DUAL LLC subsystem: 1 Dual LLC, 2 Single LLC, 3 Pass
                  'Config'          : Configs['LLC'],                                                                                                   #? [/]      - 1 LLC SR, 2 LLC AR, 3 Pass
                  'Rp'              : 10e-3,                                                                                                            #? [Ohm]    - Primary resistance (LLC AR)
                  'Rs'              : 10e-3,                                                                                                            #? [Ohm]    - Secondary resistance (LLC AR)
                  'L_r'             : 1.55e-6,                                                                                                          #? [H]      - Series resonant inductor
                  'L_k'             : 5e-6,                                                                                                             #? [H]      - Parallel (magnetizing) inductor, Ln = L_k / L_r = 3.2
                  'L_k_Iinit'       : 0,                                                                                                                #? [A]      - Initial current in L_k
                  'L_r_Iinit'       : 0,                                                                                                                #? [A]      - Initial current in L_r
                  'Trafo'           : {                                                                                                                 # Magnatic Components/Tr
                     'Config'       : Configs['Trafo'],                                                                                                 #? [/]      - 1 Ideal, 2 Real (core + gap)
                     'n_prim'       : 4,                                                                                                                #? [/]      - Primary turns
                     'n_sndry'      : 4,                                                                                                                #? [/]      - Secondary turns (1:1)
                     'Imaginit'     : 0,                                                                                                                #? [A]      - Initial magnetizing current
                     'Lp'           : 1e-9,                                                                                                             #? [H]      - Primary leakage inductance
                     'Rp'           : 1e-2,                                                                                                             #? [Ohm]    - Primary resistance
                     'Rc'           : 10e3,                                                                                                             #? [Ohm]    - Core-loss resistance (was 10 Ohm: 16 kW at 400 V)
                     'Lm'           : 1e-9,                                                                                                             #? [H]      - Extra magnetizing inductance (the core path sets Lm)
                     'Rs'           : 1e-2,                                                                                                             #? [Ohm]    - Secondary resistance (was 10 Ohm)
                     'Ls'           : 1e-9,                                                                                                             #? [H]      - Secondary leakage inductance
                     'LpIinit'      : 0,                                                                                                                #? [A]      - Initial current, primary
                     'LmIinit'      : 0,                                                                                                                #? [A]      - Initial current, magnetizing
                     'LsIinit'      : 0,                                                                                                                #? [A]      - Initial current, secondary
                     'Gap_CS_area'  : 676e-6,                                                                                                           #? [m2]     - Gap cross-section
                     'Gap_flux_len' : 1.5e-3*2,                                                                                                         #? [m]      - Gap length (two legs)
                     'Gap_init_MMF' : 0,                                                                                                                #? [A]      - Initial MMF
                     'Core_CS_area' : 676e-6,                                                                                                           #? [m2]     - Core cross-section
                     'Core_U_r_sat' : 1,                                                                                                                #? [/]      - Saturated relative permeability
                     'Core_B_sat'   : 0.49,                                                                                                             #? [T]      - Saturation flux density
                     'Core_init_MMF': 0,                                                                                                                #? [A]      - Initial MMF
                     'Core_U_r_unsat': 6500,                                                                                                            #? [/]      - Unsaturated relative permeability
                     'Core_flux_len': 149e-3                                                                                                            #? [m]      - Core path length
                  },
                  'C_r'             : _cap(1.2e-6),                                                                                                     # resonant capacitor: fr = 1/(2 pi sqrt(L_r C_r)) = 116 kHz, Z0 = 1.1 Ohm
                  'CT'              : {'Config': 1},                                                                                                    #? [/]      - Current transformer configuration
                  'L'               : 1.6e-6,                                                                                                           #? [H]      - Output inductor
                  'C_o'             : _cap(480e-6),                                                                                                     # output capacitor
                  'HS1'             : _switch(Configs['LLC_SW']),                                                                                       # primary switches (HS1, LS1, HS2, LS2)
                  'SRHS1'           : _switch(Configs['LLC_SR']),                                                                                       # rectifier switches (LLC SR)
                  'RC1'             : {                                                                                                                 # RC snubbers (Snubbers/RC Snub)
                     'Config'       : 2,                                                                                                                #? [/]      - 1 Enable, 2 Disable
                     'Rsnub'        : 100,                                                                                                              #? [Ohm]    - Snubber resistor
                     'Csnub'        : _cap(1e-9, esr=0, esl=0)                                                                                          # snubber capacitor
                  }
               }
HV_Filter      =  {                                                                                                                                     # Power/DC FILTER (LLC output -> battery)
                  'Config'          : Configs['HV_Filter'],                                                                                             #? [/]      - 1 Simple Model, 2 Pi, 3 Pass
                  'Cy'              : _cap(1e-6),                                                                                                       # Y capacitor
                  'Cx'              : _cap(10e-6),                                                                                                      # X capacitor
                  'L'               : 40e-6,                                                                                                            #? [H]      - Series inductor
                  'Choke'           : {                                                                                                                 # common-mode choke
                     'Config'       : 1,                                                                                                                #? [/]      - 1 Ideal, 2 Real
                     'L1'           : 1.5e-3,                                                                                                           #? [H]      - Inductance of winding 1
                     'L2'           : 1.5e-3,                                                                                                           #? [H]      - Inductance of winding 2
                     'R1'           : 0.01,                                                                                                             #? [Ohm]    - Resistance of winding 1
                     'R2'           : 0.01,                                                                                                             #? [Ohm]    - Resistance of winding 2
                     'Lm'           : 0.995 * 1.5e-3,                                                                                                   #? [H]      - Mutual inductance
                     'Rm'           : 0,                                                                                                                #? [Ohm]    - Resistance of the mutual inductance
                     'i1'           : 0,                                                                                                                #? [A]      - Initial current in winding 1
                     'i2'           : 0                                                                                                                 #? [A]      - Initial current in winding 2
                  }
               }
CTRL           =  {                                                                                                                                       # TPB PFC controller (PFC CTRL configuration 'TPB PFC')
                     'Vref'                  : 400,                                                                                                      #? [V]      - Reference voltage
                     'Pout'                  : 7e3,                                                                                                      #? [W]      - Rated output power
                     'T_dt'                  : 300e-9,                                                                                                   #? [s]      - Dead time
                     'fsw'                   : 80e3,                                                                                                     #? [Hz]    - Fast-leg PWM (carrier) frequency
                     'L_boost'               : PFC['Choke']['L1'] + PFC['Choke']['L2'] - 2 * PFC['Choke']['Lm'],                                         #? [H]     - Effective boost inductance seen by the current loop
                     'C_out'                 : PFC['Cout'] + DCLink['Cap_s'] * DCLink['Npara'] / DCLink['Nseri'],                                        #? [F]     - Total DC-link capacitance seen by the voltage loop
                     'fc_i'                  : 80e3/10,                                                                                                  #? [Hz]    - Current loop crossover frequency
                     'Kp_i'                  : 2 * np.pi * 80e3/10 * (PFC['Choke']['L1'] + PFC['Choke']['L2'] - 2 * PFC['Choke']['Lm']),                 #? [V/A]   - Current PI proportional gain (2*pi*fc_i*L_boost)
                     'Ki_i'                  : (2 * np.pi * 80e3/10)**2 / 10 * (PFC['Choke']['L1'] + PFC['Choke']['L2'] - 2 * PFC['Choke']['Lm']),       #? [V/As]  - Current PI integral gain (zero at fc_i/10)
                     'uL_max'                : 400,                                                                                                      #? [V]     - Current PI output (inductor voltage) limit
                     'fc_v'                  : 10,                                                                                                       #? [Hz]    - Voltage loop crossover frequency
                     'Kp_v'                  : 2 * np.pi * 10 * (PFC['Cout'] + DCLink['Cap_s'] * DCLink['Npara'] / DCLink['Nseri']) * 400,               #? [W/V]   - Voltage PI proportional gain (2*pi*fc_v*C_out*Vref)
                     'Ki_v'                  : (2 * np.pi * 10)**2 / 2 * (PFC['Cout'] + DCLink['Cap_s'] * DCLink['Npara'] / DCLink['Nseri']) * 400,      #? [W/Vs]  - Voltage PI integral gain (zero at fc_v/2)
                     'f_lpf_v'               : 20,                                                                                                       #? [Hz]    - Cut-off of the voltage-error low-pass filter (attenuates 2*f_line ripple)
                     'Pmax'                  : 8.5e3,                                                                                                    #? [W]     - Power command limit (voltage PI output)
                     'Ipk_max'               : 60,                                                                                                       #? [A]     - Peak current reference limit (Iin sensor range; 7 kW needs >= 176 Vrms)
                     'Vdc_min'               : 50,                                                                                                       #? [V]     - Lower clamp of Vdc used in the duty feedforward
                     'Vrms_min'              : 80,                                                                                                       #? [V]     - Lower clamp of the line RMS in Iref (the RMS block starts from an empty window: ~0 V in the first line cycle)
                     'Dmax'                  : 0.98,                                                                                                     #? [/]     - Maximum duty of the active fast-leg switch
                     'Vzc'                   : 20,                                                                                                       #? [V]     - |Vac| below which all gates are blanked (zero crossing)
                     'eps_s'                 : 0.1,                                                                                                      #? [V]     - Offset in sign(vac) = vac/(|vac|+eps_s)
                     't_ss'                  : 0.05,                                                                                                     #? [s]     - Soft-start ramp time of Vref from sqrt(2)*Vin to Vref
                     't_en'                  : 1e-3,                                                                                                     #? [s]     - Controller enable: gates off and Iref = 0 until the sensors / ADC readings are valid
                     'P0'                    : 0,                                                                                                        #? [W]     - Initial value of the voltage-loop integrator (power command at enable)
                     't_car'                 : 1/80e3 - 1/(2*np.pi*200e3),                                                                               #? [s]     - PWM carrier delay: Ts - current-sensor delay 1/(2*pi*Sensors.Iin.BW), so the ADC samples the average iL in both half-cycles
                     #! ---- LLC CTRL (model subsystem, C-Script gate generator: one sample hit per gate edge)
                     'LLC_Config'            : Configs['LLC_CTRL'],                                                                                      #? [/]     - 1 VF PI (output voltage), 2 Fixed frequency
                     'Vset'                  : 400,                                                                                                      #? [V]     - LLC output (battery) voltage setpoint
                     'Kp_llc'                : 2000,                                                                                                     #? [Hz/V]  - Frequency PI proportional gain (plant ~2 mV/Hz near fr -> ~50 Hz crossover)
                     'Ki_llc'                : 2000 * 2*np.pi*14,                                                                                        #? [Hz/Vs] - Frequency PI integral gain (zero at the output RC pole, ~14 Hz)
                     'f_min'                 : 70e3,                                                                                                     #? [Hz]    - Lowest switching frequency (stays above the peak-gain / capacitive region, fp ~ 57 kHz)
                     'f_max'                 : 300e3,                                                                                                    #? [Hz]    - Highest switching frequency (start-up frequency)
                     'f_llc'                 : 1 / (2*np.pi*(1.55e-6*1.2e-6)**0.5),                                                                     #? [Hz]    - Fixed frequency of LLC CTRL config 2 (series resonance L_r, C_r = 116 kHz)
                     't_llc_en'              : 0.12,                                                                                                     #? [s]     - LLC enable (after the PFC soft start: DC link at Vref)
                     'slew_llc'              : 20e3,                                                                                                     #? [V/s]   - Output voltage reference slew rate (soft start 0 -> 400 V in 20 ms)
                     'T_dt_llc'              : 100e-9,                                                                                                   #? [s]     - LLC dead time
                  }
Load           =  {
                     'Config'                : Configs['Load'],                                                                                          #? [/]     - Configuration of the load
                     'Pout'                  : 7e3,                                                                                                      #? [W]      - Load power
                     'Vout1'                 : 400,                                                                                                      #? [V]      - Load voltage (first step)
                     'Vout2'                 : 400,                                                                                                      #? [V]      - Load voltage (second step)
                     'CL'                    : 0,                                                                                                        #? [F]      - Load capacitance value
                     'R'                     : 400**2 / 7e3,                                                                                             #? [Ohm]    - Load resistance value
                     'L'                     : 10e-6,                                                                                                    #? [H]      - Load inductance value (> 0: the RL loads are singular with L = 0)
                     'Vinit'                 : 0,                                                                                                        #? [V]      - Initial voltage across the load
                     'Iinit'                 : 0,                                                                                                        #? [A]      - Initial current through the load
                     't_switch'              : Sim_param['tSim'] - Sim_param['load_tflip'],                                                              #? [s]      - Time when the load switching occurs
                     't_dead'                : (Sim_param['tSim'] - Sim_param['load_tflip']) / 2                                                        #? [s]      - Dead time for load switching

               }
Thermals       =  {
                     'T_amb'                 : 25.0,                                                                                                     #? [°C]     - Ambient temperature
                     'rth_Amb'               : 0.09                                                                                                      #? [K/W]    - Thermal resistance from junction to ambient
                  }
Sensors        =  {                                                                                                                                   # measurement chain on the board (Sensors library): v_out = clamp(Vofs + err_ofs + G*(1+err_g)*x, Vmin, Vmax)
                  'Iin'           : {                                                                                                                 # input (inductor) current: 1 mOhm shunt + AMC1301 (x8.2) + level shift, +-62.5 A -> 1.65 +- 1.25 V
                     'G'       : 0.02,                                                                                                                #? [V/A]    - Sensitivity
                     'Vofs'    : 1.65,                                                                                                                #? [V]      - Output at 0 A (mid-rail)
                     'BW'      : 200e3,                                                                                                               #? [Hz]     - Bandwidth (isolated amplifier)
                     'err_g'   : 0,                                                                                                                   #? [/]      - Gain error (e.g. 0.005 = +0.5 %)
                     'err_ofs' : 0,                                                                                                                   #? [V]      - Offset error
                     'Vmin'    : 0,                                                                                                                   #? [V]      - Output clamp low (ADC rail)
                     'Vmax'    : 3.3,                                                                                                                 #? [V]      - Output clamp high (ADC rail)
                  },
                  'Vac'           : {                                                                                                                 # AC input voltage: resistive divider + RC + AMC1311, +-400 V -> 1.65 +- 1.5 V
                     'G'       : 1.5/400,                                                                                                             #? [V/V]    - Divider + amplifier gain
                     'Vofs'    : 1.65,                                                                                                                #? [V]      - Output at 0 V (mid-rail)
                     'BW'      : 10e3,                                                                                                                #? [Hz]     - RC anti-alias filter corner
                     'BW2'     : 275e3,                                                                                                               #? [Hz]     - Isolated amplifier bandwidth
                     'err_g'   : 0,                                                                                                                   #? [/]      - Gain error
                     'err_ofs' : 0,                                                                                                                   #? [V]      - Offset error
                     'Vmin'    : 0,                                                                                                                   #? [V]      - Output clamp low
                     'Vmax'    : 3.3,                                                                                                                 #? [V]      - Output clamp high
                  },
                  'Vdc'           : {                                                                                                                 # DC-link voltage: resistive divider + RC + AMC1311, 0..500 V -> 0..3 V
                     'G'       : 3/500,                                                                                                               #? [V/V]    - Divider + amplifier gain
                     'Vofs'    : 0.02,                                                                                                                #? [V]      - Output at 0 V (amplifier offset; keeps the ADC off its 0 V clamp at start-up, calibrated out)
                     'BW'      : 5e3,                                                                                                                 #? [Hz]     - RC anti-alias filter corner
                     'BW2'     : 275e3,                                                                                                               #? [Hz]     - Isolated amplifier bandwidth
                     'err_g'   : 0,                                                                                                                   #? [/]      - Gain error
                     'err_ofs' : 0,                                                                                                                   #? [V]      - Offset error
                     'Vmin'    : -0.3,                                                                                                                #? [V]      - Output clamp low (ADC input protection diode; 0 V would sit on the clamp at Vdc = 0 and chatter)
                     'Vmax'    : 3.3,                                                                                                                 #? [V]      - Output clamp high
                  }
               }
MCU            =  {                                                                                                                                   # microcontroller: ADC + firmware calibration (nominal sensor gain / offset, without the errors)
                  'ADC'           : {                                                                                                                 # ADC used for all three channels (Sensors/ADC)
                     'N'       : 12,                                                                                                                  #? [bit]    - Resolution
                     'Vref'    : 3.3,                                                                                                                 #? [V]      - Full scale
                     'Ts'      : 1/CTRL['fsw'],                                                                                                       #? [s]      - Sampling period (once per PWM period)
                     'Toffs'   : 0,                                                                                                                   #? [s]      - Sampling instant in the period (0 = carrier valley -> average inductor current)
                     'err_g'   : 0,                                                                                                                   #? [/]      - ADC gain error
                     'err_ofs' : 0,                                                                                                                   #? [V]      - ADC offset error
                  },
                  'Cal'           : {                                                                                                                 # calibration the firmware uses to convert counts back to V / A
                     'Iin'     : {                                                                                                                    # Iin channel
                        'G'    : Sensors['Iin']['G'],                                                                                                 #? [V/unit] - Nominal sensor gain
                        'ofs'  : Sensors['Iin']['Vofs']                                                                                               #? [V]      - Nominal sensor offset
                     },
                     'Vac'     : {                                                                                                                    # Vac channel
                        'G'    : Sensors['Vac']['G'],                                                                                                 #? [V/unit] - Nominal sensor gain
                        'ofs'  : Sensors['Vac']['Vofs']                                                                                               #? [V]      - Nominal sensor offset
                     },
                     'Vdc'     : {                                                                                                                    # Vdc channel
                        'G'    : Sensors['Vdc']['G'],                                                                                                 #? [V/unit] - Nominal sensor gain
                        'ofs'  : Sensors['Vdc']['Vofs']                                                                                               #? [V]      - Nominal sensor offset
                     }
                  }
               }
#? -------------------------------------------------------------------------------

ModelVars      =  {
                  'Sim_param'             :  Sim_param               ,
                  'ToFile'                :  ToFile                  ,
                  'Grid'                  :  Grid                    ,
                  'AC_Filter'             :  AC_Filter               ,
                  'PFC'                   :  PFC                     ,
                  'DCLink'                :  DCLink                  ,
                  'LLC'                   :  LLC                     ,
                  'HV_Filter'             :  HV_Filter               ,
                  'CTRL'                  :  CTRL                    ,
                  'Load'                  :  Load                    ,
                  'Thermals'              :  Thermals                ,
                  'Sensors'               :  Sensors                 ,
                  'MCU'                   :  MCU
               }
AnalysisOpts   =  {                                                                         # model/HV_Filter_Analysis.plecs (analysis.py): DC filter AC sweep
                  'DC_Filter'             :  HV_Filter               ,
                  'system_period'         :  1/100e3                 ,
                  'freq_range_min'        :  1                       ,
                  'freq_range_max'        :  1e7                     ,
                  'amplitude'             :  1e-1                    ,
                  'sim_Tstart'            :  0                       ,
                  'NB_pts'                :  10000                   ,
                  'additional_freq'       :  []                      ,
                  'NB_init_cycles'        :  0                       ,
                  'Termination_tol'       :  1e-3                    ,
                  'max_iter_NB'           :  50                      ,
                  'Jacobian_rel_tol'      :  1e-6

              }
#! Result CSV columns: names and units are read from the To File header and the model by signals.SignalNames; the
#! elements of vector probes are named after the library mask probes. Labels only for vectors no library block names:
SIGNAL_LABELS  =  {                                                                                            # 'component:probe signal' -> element names
                  'PFC:Gate Signals'                      : ['HS1', 'LS1', 'HS2', 'LS2', 'HS3', 'LS3'],                # g_PFC order of the PFC CTRL
               }
#? -------------------------------------------------------------------------------
