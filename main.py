#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?
#?                              _
#?             ____ ___  ____ _(_)___
#?            / __ `__ \/ __ `/ / __ \
#?           / / / / / / /_/ / / / / /
#?          /_/ /_/ /_/\__,_/_/_/ /_/
#?
#?
#? Name:        main.py
#? Purpose:     Entry point: sweeps the SWEEP parameters and runs the PLECS model (7 kW OBC) for each point.
#?              Optional: parallel points, code generation, RT Box run.
#?              System specific: MODE, SWEEP and the run settings below.
#?
#? Author:      Mohamed Gueni ( mohamedgueni@outlook.com)
#?
#? Created:     09/15/2024
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------
#? -------------------------------------------------------------------------------
import os
import time

from   lib              import  plecs   as  plc
from   lib              import  vars    as  prm
from   lib.calc         import  Derived         
from   lib.process      import  PPlots
from   lib.signals      import  SignalNames
from   lib.standalone   import  Standalone
#?----------------------------------------------------------------------------------------------------------------------------------------
#? Model depth: 'ideal' or 'real' sets all block configurations at once (vars.MODES); None = vars.Configs.
MODE                                   = 'ideal'

#? Sweep definition: every combination of the values below is simulated (keep a single value to hold a parameter fixed).
#? Key = the parameter name in vars.py ('Vin'), or the end of its path when the name is used several times ('Choke.L1');
#? an unknown or ambiguous key stops the run with the possible names. Parameters that follow another one (CTRL.Pout,
#? the switch temperatures, the load R) are set by Derived.update in calc.py.
#? The model is vars.MODEL_NAME (OBC by default; PFC / LLC have no To File block: they run, but give no report).
SWEEP                                  = {
                                          'Vin'           : [230],
                                          'Load.Pout'     : [7e3],
                                          'Vset'          : [400],
                                          'T_amb'         : [25],
                                         }

#? What to run (in this order): the sweep, then code generation, then the RT Box (RTBOX implies CODEGEN).
STANDALONE                             = False                                                 # write Model/<model>_std.plecs: no library links, parameters of sweep point STD_POINT
STD_POINT                              = 0                                                     # index of the sweep point the standalone copy is set to
SWEEP_EN                               = True                                                  # run the simulation sweep
CODEGEN                                = False                                                 # generate code (PLECS Coder) with the base ModelVars
RTBOX                                  = False                                                 # upload + run the generated code on the RT Box
SCOPES                                 = None                                                  # scope names to clear/hold/save: None = all scopes in the model, [] = none
HOLD_TRACES                            = True                                                  # hold traces after each simulation point, to save them all at the end
SAVE_TRACES                            = True                                                 # save all traces at the end of the sweep
PARASIM                                = False                                                 # run several sweep points in parallel
PARANUM                                = None                                                  # max sweep points per parallel batch (None = auto from the CPU threads)
ANALYSIS_NAME                          = ''                                                    # PLECS analysis name, for plcsim.launch_analysis

modelname                              = prm.MODEL_NAME
port                                   = "1080"
url                                    = f"http://localhost:{port}/RPC2"
model_directory                        = prm.MODEL_PATH.as_posix()
paths                                  = plc.ResultPaths(prm.DATA_DIR)

#? Code generation / RT Box settings (only used when CODEGEN or RTBOX is True)
CODEGEN_TARGET                         = ""                                                    # subsystem with 'Enable code generation' checked, e.g. "PFC CTRL"
CODEGEN_DIR                            = prm.DATA_DIR / "codegen"                              # where PLECS Coder writes the generated code / .elf
RTBOX_URL                              = "http://192.168.0.10:9998/RPC2"                       # RT Box XML-RPC server (its IP, port 9998)
RTBOX_SET                              = {}                                                    # Programmable Value blocks to write after start: {'Vref': [400]}
RTBOX_CAPTURE                          = []                                                    # Data Capture blocks to read before stop: ['Capture1']
RTBOX_TIMEOUT                          = 30                                                    # [s] max wait for a capture trigger (None = forever)
#?----------------------------------------------------------------------------------------------------------------------------------------
plcsim                                 = plc.simpy(
                                                    url             =   url                 ,
                                                    port            =   port                ,
                                                    path            =   model_directory     ,
                                                    modelvar        =   prm.ModelVars       ,
                                                    analysisvars    =   prm.ModelVars       ,
                                                    analysisName    =   ANALYSIS_NAME       ,
                                                    parasim         =   PARASIM             ,
                                                    paranum         =   PARANUM or 1
                                                    )
if MODE:
        prm.Configs.update(prm.MODES[MODE])
        plc.Sweep.apply_configs(prm.ModelVars, prm.MODES[MODE], prm.CONFIG_PATHS)

if STANDALONE:
        std_label, std_vars            = plc.Sweep.build_points(prm.ModelVars, SWEEP, 'std', paths, update_derived=Derived.update)[STD_POINT]
        print(f"standalone copy set to {std_label}")
        Standalone.write(prm.MODEL_PATH, std_vars, prm.PLECS_LIB_DIR)

plcsim.rpc_connect()
plcsim.load_model()

if SWEEP_EN:
        plcsim.clear_data_folders(paths.folders)
        scopes                         = plcsim.get_scopes(modelname, only=SCOPES)
        scopes                         = plcsim.ClearAllTraces(scopes)
        run_id                         = time.strftime("%Y%m%d%H%M%S", time.gmtime())
        points                         = plc.Sweep.build_points(prm.ModelVars, SWEEP, run_id, paths, update_derived=Derived.update)
        batch_size                     = plc.Sweep.auto_batch_size(len(points), PARANUM) if PARASIM else 1
        plcsim.paranum                 = batch_size
        for start in range(0, len(points), batch_size):
                batch                  = points[start:start + batch_size]
                plcsim.Set_sim_param([mv for _, mv in batch] if PARASIM else batch[0][1])
                plcsim.launch_sim(modelname=modelname)
                if HOLD_TRACES: plcsim.HoldAllTraces(scopes)

        if SAVE_TRACES: plcsim.saveAllTraces(scopes, paths.traces.as_posix(), run_id)
        csv                            = points[0][1][plc.OUTPUT_KEY]['ToFile_path']
        if not os.path.isfile(csv):
                print(f"No result file {csv}: {modelname} has no To File block, no report.")
                raise SystemExit
        signals, units                 = SignalNames.read(                                     # result columns: names / units read from the model
                                                points[0][1][plc.OUTPUT_KEY]['ToFile_path'] ,
                                                prm.MODEL_PATH                              ,
                                                prm.PLECS_LIB_DIR                           ,
                                                points[0][1]                                ,
                                                labels  =   getattr(prm, 'SIGNAL_LABELS', None),
                                                units   =   True
                                                )
        PPlots.gen_sweep_plots(
                                points                                                              ,
                                waveforms       =   signals                                         ,
                                units           =   units                                           ,
                                f0_path         =   getattr(prm, 'F0_PATH', None)                   ,
                                f0_overrides    =   getattr(prm, 'F0_OVERRIDES', None)              ,
                                model_name      =   modelname                                       ,
                                img_path        =   getattr(prm, 'MODEL_IMG_PATH', None)            ,
                                params_file     =   prm.__file__                                    ,
                                OPEN            =   False
                                )

if CODEGEN or RTBOX:
        rtb                            = plc.RTBox(
                                                plcsim.server                       ,
                                                modelname       =   modelname       ,
                                                codegen_target  =   CODEGEN_TARGET  ,
                                                output_dir      =   CODEGEN_DIR     ,
                                                rtbox_url       =   RTBOX_URL
                                                )
        rtb.generate_code(prm.ModelVars)
        if RTBOX:
                captured               = rtb.run(set_values=RTBOX_SET, capture_blocks=RTBOX_CAPTURE, timeout=RTBOX_TIMEOUT)
                print(f"RT Box captured: {list(captured)}")
#?----------------------------------------------------------------------------------------------------------------------------------------
