#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?
#?                     __
#?              ____  / /__  __________
#?             / __ \/ / _ \/ ___/ ___/
#?            / /_/ / /  __/ /__(__  )
#?           / .___/_/\___/\___/____/
#?          /_/
#?
#?
#? Name:        plecs.py
#? Purpose:     interface: XML-RPC (simpy), scopes, result folders, sweep points.
#?              Code generation and RT Box (RTBox).
#?
#? Author:      Mohamed Gueni ( mohamedgueni@outlook.com)
#?
#? Created:     09/15/2024
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------
#? -------------------------------------------------------------------------------
import copy
import glob
import itertools
import math
import time
import xmlrpc.client
import subprocess
import shutil
import os
from   pathlib              import  Path

#?----------------------------------------------------------------------------------------------------------------------------------------
#? Convention with the PLECS model: ModelVars[OUTPUT_KEY] holds the output files of a run; the model's To File block writes
#? its CSV to ToFile.ToFile_path. OUTPUT_FIELDS are filled in per run by Sweep.set_output_files (not real model parameters).
OUTPUT_KEY                     = 'ToFile'
OUTPUT_FIELDS                  = ('sim_idx', 'utc_numeric', 'ToFile_path', 'logfile', 'output_html', 'Traces', 'Mat')
#?----------------------------------------------------------------------------------------------------------------------------------------
class ResultPaths:
    """Result folders of a project under data_dir (created if missing):
    timeseries (simulation CSVs), mat (one <type>_<run>.csv matrix per result type of PMath.RESULT_TYPES), log, html, traces."""

    def __init__(self,data_dir):
        self.root                   =   Path(data_dir)
        self.timeseries             =   self.root / "timeseries"
        self.mat                    =   self.root / "mat"
        self.log                    =   self.root / "log"
        self.html                   =   self.root / "html"
        self.traces                 =   self.root / "traces"
        self.folders                =   [self.timeseries, self.mat, self.html, self.log, self.traces]
        for folder in self.folders:
            folder.mkdir(parents=True, exist_ok=True)
#?----------------------------------------------------------------------------------------------------------------------------------------
class simpy:
    """PLECS session over XML-RPC: launch PLECS, load the model, set ModelVars, simulate / analyse, drive the scopes."""

    EXE                         =   "PLECS.exe"

    def __init__(self, url, port, path, modelvar, analysisvars=None, analysisName='', parasim=False, paranum=1):
        self.url                =   url
        self.port               =   port
        self.path               =   path
        self.modelvar           =   modelvar
        self.analysisName       =   analysisName
        self.parasim            =   parasim
        self.paranum            =   paranum
        self.server             =   None
        self.opts               =   {}
        self.set_analysis_param(analysisvars or modelvar)

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? PLECS process and connection
    #?------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def is_running(process_name):
        """True if a process of that name appears in the Windows task list."""
        try:
            return process_name.lower() in os.popen('tasklist').read().lower()
        except OSError as e:
            print(f"Cannot read the task list: {e}")
            return False

    @staticmethod
    def find_executable(exe_name):
        """PLECS_EXE environment variable, else PATH, else the standard install folders and ~/Documents."""
        env_path                =   os.environ.get("PLECS_EXE")
        if env_path and os.path.isfile(env_path):
            return env_path
        on_path                 =   shutil.which(exe_name)
        if on_path:
            return on_path
        roots                   =   [os.path.join(os.environ.get(v, ""), "Plexim") for v in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA")]
        for root in roots + [os.path.expanduser("~/Documents")]:
            for folder, _, files in os.walk(root) if os.path.isdir(root) else ():
                if exe_name in files:
                    return os.path.join(folder, exe_name)
        return None

    def launch_if_not_running(self):
        if self.is_running(self.EXE):
            print(f"{self.EXE} is already running.")
            return
        exe_path                =   self.find_executable(self.EXE)
        if not exe_path:
            print(f"Could not find {self.EXE} on your system.")
            return
        subprocess.Popen(exe_path)
        print(f"{self.EXE} has been launched from {exe_path}.")

    def rpc_connect(self):
        self.launch_if_not_running()
        self.server             =   xmlrpc.client.ServerProxy(self.url)

    def load_model(self):
        self.server.plecs.load(self.path)

    def close_cnx(self, modelname):
        self.server.plecs.close(modelname)

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? Simulation and analysis
    #?------------------------------------------------------------------------------------------------------------------------------------
    def Set_sim_param(self, mdlvars):
        """ModelVars of the next run: one dict, or (parallel) a list of dicts / one dict copied paranum times."""
        self.modelvar           =   mdlvars
        if not self.parasim:
            self.opts           =   {'ModelVars': mdlvars}
        else:
            runs                =   mdlvars if isinstance(mdlvars, list) else [copy.deepcopy(mdlvars) for _ in range(self.paranum)]
            self.opts           =   [{'ModelVars': mv} for mv in runs]

    def set_analysis_param(self, analysisvars):
        self.analysisvars       =   analysisvars
        self.analysisopts       =   {'ModelVars': analysisvars}

    def launch_sim(self, modelname):
        return self.server.plecs.simulate(modelname, self.opts)

    def launch_analysis(self, modelname):
        return self.server.plecs.analyze(modelname, self.analysisName, self.analysisopts)

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? Model file and scopes
    #?------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _parse_blocks(lines):
        """Tree of the 'Tag { ... }' blocks of a .plecs file: {'tag', 'props' [(key, value) in order], 'children'}."""
        root                    =   {'tag': None, 'props': [], 'children': []}
        stack                   =   [root]
        for line in lines:
            s                   =   line.strip()
            if s.endswith('{') and s[:-1].strip().isidentifier():
                node            =   {'tag': s[:-1].strip(), 'props': [], 'children': []}
                stack[-1]['children'].append(node)
                stack.append(node)
            elif s == '}' and len(stack) > 1:
                stack.pop()
            elif s.startswith('"') and stack[-1]['props']:                  # continuation of a string split over lines
                key, value      =   stack[-1]['props'][-1]
                stack[-1]['props'][-1] = (key, value + (s[1:-1] if s.endswith('"') else s[1:]))
            elif s:
                key, _, value   =   s.partition(' ')
                stack[-1]['props'].append((key, value.strip().strip('"')))
        return root

    @staticmethod
    def _prop(node, key):
        return next((v for k, v in node['props'] if k == key), None)

    def get_scopes(self, modelname, only=None):
        """Full PLECS paths ('PFC/Scopes/grid_scope', ...) of the Scope blocks of the model file.
        Commented-out blocks are skipped; of a Configurable Subsystem only the active configuration is walked.
        only: scope names to keep (None = all, [] = none). Scopes inside library references are not found."""
        with open(self.path, encoding='utf-8', errors='ignore') as f:
            root                =   self._parse_blocks(f.readlines())
        scopes                  =   []
        esc                     =   lambda name: name.replace('/', '//')

        def walk(node, parents):
            for child in node['children']:
                if child['tag'] != 'Component':
                    walk(child, parents)
                    continue
                if self._prop(child, 'CommentOut'):
                    continue
                kind, name      =   self._prop(child, 'Type'), self._prop(child, 'Name')
                if kind == 'Scope':
                    scopes.append('/'.join([modelname] + parents + [esc(name)]))
                elif kind == 'ConfigurableSubsystem':
                    configs     =   next((c for c in child['children'] if c['tag'] == 'Configurations'), None)
                    if configs is None:
                        continue
                    names       =   [v for k, v in configs['props'] if k == 'Name']
                    schematics  =   [c for c in configs['children'] if c['tag'] == 'Schematic']
                    active      =   next((self._prop(c, 'Value') for c in child['children']
                                          if c['tag'] == 'Parameter' and self._prop(c, 'Variable') == 'Configuration'), None)
                    if active is not None and active.isdigit() and 1 <= int(active) <= len(schematics):
                        selected =  [schematics[int(active) - 1]]
                    elif active in names:
                        selected =  [schematics[names.index(active)]]
                    else:                                                   # set by an expression: cannot tell offline
                        selected =  schematics
                    for schematic in selected:
                        walk(schematic, parents + [esc(name)])
                else:
                    walk(child, parents + [esc(name)])

        walk(root, [])
        return scopes if only is None else [p for p in scopes if p.split('/')[-1] in only]

    def ClearAllTraces(self, scopelist):
        """Clear the traces of the scopes; scopes PLECS cannot find are skipped. Returns the scopes that exist."""
        found                   =   []
        for scope in scopelist:
            try:
                self.server.plecs.scope(scope, 'ClearTraces')
                found.append(scope)
            except xmlrpc.client.Fault as fault:
                print(f"WARNING: scope skipped: {fault.faultString}")
        return found

    def HoldAllTraces(self, scopelist):
        for scope in scopelist:
            self.server.plecs.scope(scope, 'HoldTrace')

    def saveAllTraces(self, scopelist, path, tag):
        for scope in scopelist:
            self.server.plecs.scope(scope, 'SaveTraces', f"{Path(path).as_posix()}/{scope.split('/')[-1]}_{tag}.trace")

    @staticmethod
    def clear_data_folders(folder_paths):
        """Delete the files (not the sub-folders) of each result folder."""
        for folder in map(Path, folder_paths):
            if not folder.is_dir():
                print(f"Error: {folder} is not a directory.")
                continue
            for f in folder.iterdir():
                if f.is_file():
                    f.unlink()

#?----------------------------------------------------------------------------------------------------------------------------------------
class Sweep:
    """Sweep points: nested ModelVars access, parallel batch sizing, output files of a run, sweep point generation."""

    @staticmethod
    def set_nested(d, path, value):
        for key in path[:-1]:
            d                      = d[key]
        d[path[-1]]                = value

    @staticmethod
    def get_nested(d, path):
        for key in path:
            d                      = d[key]
        return d

    @staticmethod
    def apply_configs(mdlvar, configs, config_paths):
        """Write block configurations {name: value} (e.g. a mode preset) to every ModelVars path of config_paths[name]."""
        for name, value in configs.items():
            for path in config_paths[name]:
                Sweep.set_nested(mdlvar, path, value)
        return mdlvar

    @staticmethod
    def auto_batch_size(n_points, max_parallel=None, reserve=1):
        """Sweep points per parallel batch, from the CPU threads available to this process (minus `reserve` left for the
        OS / PLECS GUI), capped by max_parallel, then balanced so the batches are as even as possible
        (e.g. 20 points on 15 threads -> 2 batches of 10 instead of 15 + 5)."""
        threads                    = (os.process_cpu_count() if hasattr(os, 'process_cpu_count') else os.cpu_count()) or 1
        workers                    = max(1, min(threads - reserve, max_parallel or threads, n_points))
        n_batches                  = math.ceil(n_points / workers)
        return math.ceil(n_points / n_batches)

    @staticmethod
    def set_output_files(mdlvar, paths, run_id, sim_idx):
        """Output files of one run of the sweep run_id, written in mdlvar[OUTPUT_KEY]."""
        out                        = mdlvar[OUTPUT_KEY]
        out['sim_idx']             = sim_idx
        out['utc_numeric']         = run_id
        out['ToFile_path']         = (paths.timeseries / f"Results_{run_id}_{sim_idx}.csv").as_posix()
        out['logfile']             = (paths.log  / f"Log_{run_id}.log").as_posix()
        out['output_html']         = (paths.html / f"Html_{run_id}.html").as_posix()
        out['Traces']              = paths.traces.as_posix()
        out['Mat']                 = paths.mat.as_posix()
        return mdlvar

    @staticmethod
    def leaf_paths(d, prefix=()):
        """Key paths of every value of a nested dict (dicts are walked, everything else is a value)."""
        for k, v in d.items():
            if isinstance(v, dict):
                yield from Sweep.leaf_paths(v, prefix + (k,))
            else:
                yield prefix + (k,)

    @staticmethod
    def resolve_paths(base, sweep):
        """ModelVars path of each sweep name: a parameter name ('Vin') or the dotted end of its path ('Choke.L1',
        'PFC.Choke.L1'); it must match exactly one parameter of base, else a ValueError lists the candidates."""
        leaves                     = [p for p in Sweep.leaf_paths(base) if p[0] != OUTPUT_KEY]
        resolved                   = {}
        for name in sweep:
            tail                   = tuple(name.split('.'))
            found                  = [p for p in leaves if p[-len(tail):] == tail]
            if len(found) != 1:
                options            = [p for p in leaves if p[-1] == tail[-1]]
                raise ValueError(f"Sweep name '{name}' matches {len(found)} parameters; "
                                 f"use one of: {', '.join('.'.join(p) for p in options) or 'none (unknown name)'}")
            resolved[name]         = found[0]
        return resolved

    @staticmethod
    def build_points(base, sweep, run_id, paths, update_derived=None):
        """One deep-copied ModelVars per combination of the sweep values ({name: values}, names resolved by
        resolve_paths), with derived parameters (update_derived(mv), optional, e.g. calc.Derived.update) and output files
        updated. Returns a list of (label {sweep name: value}, ModelVars)."""
        sweep_paths                = Sweep.resolve_paths(base, sweep)
        points                     = []
        for sim_idx, values in enumerate(itertools.product(*sweep.values()), start=1):
            label                  = dict(zip(sweep, values))
            mv                     = copy.deepcopy(base)
            for name, value in label.items():
                Sweep.set_nested(mv, sweep_paths[name], value)
            if update_derived:
                update_derived(mv)
            Sweep.set_output_files(mv, paths, run_id, sim_idx)
            points.append((label, mv))
        return points
#?----------------------------------------------------------------------------------------------------------------------------------------
class RTBox:
    """
    Code generation goes through PLECS (plecs_server = the simpy connection), the hardware calls go to the RT Box's
    own XML-RPC server (rtbox_url, e.g. http://192.168.0.10:9998/RPC2), which is only contacted by connect().
    codegen_target is the subsystem with 'Enable code generation' checked (Target I/O blocks must sit on its top level).
    """

    def __init__(self,plecs_server,modelname,codegen_target,output_dir,rtbox_url=''):
        self.plecs                  =   plecs_server
        self.modelname              =   modelname
        self.codegen_target         =   codegen_target
        self.output_dir             =   str(output_dir)
        self.rtbox_url              =   rtbox_url
        self.server                 =   None
        self.elf                    =   None

    def generate_code(self,modelvars):
        """Run PLECS Coder on modelname/codegen_target with the given ModelVars, return the generated .elf path (None for non-RT Box targets)."""
        if not self.codegen_target:
            raise ValueError("CODEGEN_TARGET is empty: set it to the subsystem that has 'Enable code generation' checked.")
        os.makedirs(self.output_dir, exist_ok=True)
        target                      =   f"{self.modelname}/{self.codegen_target}"
        t0                          =   time.time()
        print(f"Generating code for {target} -> {self.output_dir}")
        self.plecs.plecs.codegen(target, {'ModelVars': modelvars}, self.output_dir)
        # The .elf base name depends on the model's Coder options, so take the one written by this build
        elfs                        =   [f for f in glob.glob(os.path.join(self.output_dir, '*.elf')) if os.path.getmtime(f) >= t0 - 1]
        self.elf                    =   max(elfs, key=os.path.getmtime) if elfs else None
        print(f"Code generated in {time.time() - t0:.1f} s" + (f": {self.elf}" if self.elf else " (no .elf produced)"))
        return self.elf

    def connect(self):
        if not self.rtbox_url:
            raise ValueError("RTBOX_URL is empty: set it to http://<rtbox-ip>:9998/RPC2.")
        self.server                 =   xmlrpc.client.ServerProxy(self.rtbox_url)

    def upload(self,elf=None):
        elf                         =   elf or self.elf
        if not elf or not os.path.isfile(elf):
            raise FileNotFoundError(f"No executable to upload: {elf}")
        print(f"Uploading {elf}")
        with open(elf, 'rb') as f:
            self.server.rtbox.load(xmlrpc.client.Binary(f.read()))

    def start(self):
        self.server.rtbox.start()
        print("RT Box running.")

    def stop(self):
        self.server.rtbox.stop()
        print("RT Box stopped.")

    def reboot(self):
        self.server.rtbox.reboot()

    def query(self):
        return self.server.rtbox.querySimulation()

    def log(self):
        return self.server.rtbox.getApplicationLog()

    def list_blocks(self):
        """(Programmable Value block names, Data Capture block names) of the running model."""
        return self.server.rtbox.getProgrammableValueBlocks(), self.server.rtbox.getDataCaptureBlocks()

    def set_value(self,block,values):
        self.server.rtbox.setProgrammableValue(block, [float(v) for v in values])

    def get_capture(self,blocks,poll_interval=1.0,timeout=None):
        """Wait for a trigger on the first Data Capture block, then read all of them: {block: data}."""
        t0                          =   time.time()
        while self.server.rtbox.getCaptureTriggerCount(blocks[0]) == 0:
            if timeout is not None and time.time() - t0 >= timeout:
                raise TimeoutError(f"No trigger on {blocks[0]} after {timeout} s.")
            time.sleep(poll_interval)
        return {block: self.server.rtbox.getCaptureData(block) for block in blocks}

    def run(self,set_values=None,capture_blocks=None,poll_interval=1.0,timeout=None):
        """Upload the generated .elf, start it, write set_values {block: [values]}, read capture_blocks, always stop."""
        self.connect()
        self.upload()
        captured                    =   {}
        self.start()
        try:
            inputs, outputs         =   self.list_blocks()
            print(f"Programmable Value blocks: {inputs}\nData Capture blocks      : {outputs}")
            for block, values in (set_values or {}).items():
                self.set_value(block, values)
            if capture_blocks:
                captured            =   self.get_capture(capture_blocks, poll_interval, timeout)
        except Exception:
            try:
                print(f"RT Box application log: {self.log()}")
            except Exception:
                pass
            raise
        finally:
            self.stop()
        return captured
#?----------------------------------------------------------------------------------------------------------------------------------------
