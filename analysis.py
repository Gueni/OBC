#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?
#?                            __           _
#?            ____ _____  ____ _/ /_  _______(_)____
#?           / __ `/ __ \/ __ `/ / / / / ___/ / ___/
#?          / /_/ / / / / /_/ / / /_/ (__  ) (__  )
#?          \__,_/_/ /_/\__,_/_/\__, /____/_/____/
#?                             /____/
#?
#? Name:        analysis.py
#? Purpose:     AC sweep of the HV DC filter (model/HV_Filter_Analysis.plecs, analysis 'DC Filter AC Sweep'):
#?              every combination of the SWEEP values below, one HTML with magnitude / phase of all points.
#?
#? Author:      Mohamed Gueni ( mohamedgueni@outlook.com)
#?
#? Created:     09/02/2024
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------
#? -------------------------------------------------------------------------------
import copy
import itertools
import time

from   lib              import  plecs   as  plc
from   lib              import  vars    as  prm
from   lib.process      import  PPlots
#?----------------------------------------------------------------------------------------------------------------------------------------
MODEL_NAME                             = "HV_Filter_Analysis"
ANALYSIS                               = "DC Filter AC Sweep"
MODEL_PATH                             = prm.ROOT_DIR / "model" / f"{MODEL_NAME}.plecs"

#? Sweep of the DC filter (keys = path inside AnalysisOpts['DC_Filter'] = vars.HV_Filter); every combination is analysed.
SWEEP                                  = {
                                          ('Cx', 'Cap_s')     : [10e-6],
                                          ('Cy', 'Cap_s')     : [1e-6],
                                          ('L',)              : [40e-6],
                                          ('Choke', 'L1')     : [1.5e-3],
                                          ('Choke', 'L2')     : [1.5e-3],
                                         }
NB_PTS                                 = 2000                                                  # frequency points of the sweep
port                                   = "1080"
url                                    = f"http://localhost:{port}/RPC2"
paths                                  = plc.ResultPaths(prm.DATA_DIR)
#?----------------------------------------------------------------------------------------------------------------------------------------
base                                   = copy.deepcopy(prm.AnalysisOpts)
base['NB_pts']                         = NB_PTS
plcsim                                 = plc.simpy(url=url, port=port, path=MODEL_PATH.as_posix(), modelvar=base,
                                                   analysisvars=base, analysisName=ANALYSIS)
plcsim.rpc_connect()
plcsim.load_model()

results                                = []
for i, values in enumerate(itertools.product(*SWEEP.values()), start=1):
        opts                           = copy.deepcopy(base)
        for path, value in zip(SWEEP, values):
                plc.Sweep.set_nested(opts['DC_Filter'], path, value)
        print(f"point {i}: " + ", ".join(f"{'.'.join(p)} = {v:g}" for p, v in zip(SWEEP, values)))
        plcsim.set_analysis_param(opts)
        results.append(plcsim.launch_analysis(modelname=MODEL_NAME))

html                                   = paths.html / f"AC_{time.strftime('%Y%m%d%H%M%S', time.gmtime())}.html"
PPlots.plot_ac_analysis_sweep(results, html.as_posix(), base, title='HV DC Filter AC Sweep', OPEN=False)
print(f"report: {html}")
#?----------------------------------------------------------------------------------------------------------------------------------------
