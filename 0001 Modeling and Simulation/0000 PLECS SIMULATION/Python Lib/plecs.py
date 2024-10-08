
#?----------------------------------------------------------------------------------------------------------------------------------------
#?                                  ____  __    _________________    ________  ___   ________
#?                                 / __ \/ /   / ____/ ____/ ___/   / ____/ / / / | / / ____/
#?                                / /_/ / /   / __/ / /    \__ \   / /_  / / / /  |/ / /     
#?                               / ____/ /___/ /___/ /___ ___/ /  / __/ / /_/ / /|  / /___   
#?                              /_/   /_____/_____/\____//____/  /_/    \____/_/ |_/\____/  
#?                              
#?----------------------------------------------------------------------------------------------------------------------------------------
import copy
import xmlrpc.client
import subprocess
import os
#?----------------------------------------------------------------------------------------------------------------------------------------
class simpy:
    
    def __init__(self,url,port,path,modelvar,analysisvars='',analysisName='',parasim = False,paranum = 1):
        self.url            =   url
        self.port           =   port
        self.path           =   path
        self.modelvar       =   modelvar
        self.analysisvars   =   analysisvars
        self.analysisName   =   analysisName
        self.opts           =   []
        self.parasim             =   parasim 
        self.paranum             =   paranum

    def is_running(self,process_name):
        try:
            tasks = os.popen('tasklist').read().strip().split('\n')
            for task in tasks:
                if process_name.lower() in task.lower():
                    return True
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    def return_opts(self,parasim = False , paranum = 1):
        if not parasim and paranum == 1 : 
            self.opts  = { 'ModelVars': self.modelvar}  #, 'SolverOpts': self.slv0pts, 'AnalysisOpts': self.an10pts}
        else :
            self.opts  = [{'ModelVars' : [copy.deepcopy(self.modelvar) for _ in range(paranum)][x] for x in range(paranum)}]   #, 'SolverOpts': slv_list[x], 'AnalysisOpts': anl_list [x]} for x in range(instances)]  
            # [{'ModelVars' :, 'SolverOpts':, 'AnalysisOpts': } for x in range(paranum)]
        return self.opts        

    def find_executable(self,exe_name):
        documents_folder = os.path.expanduser("~/Documents")
        for root, dirs, files in os.walk(documents_folder):
            if exe_name in files:
                return os.path.join(root, exe_name)
        return None

    def launch_if_not_running(self):
        exe_name = "PLECS.exe"
        exe_path = self.find_executable(exe_name)
        if not exe_path:
            print(f"Could not find {exe_name} on your system.")
            return
        
        if not self.is_running(exe_name):
            subprocess.Popen(exe_path)
            print(f"{exe_name} has been launched from {exe_path}.")
        else:
            print(f"{exe_name} is already running.")

    def rpc_connect(self):
        self.launch_if_not_running()
        self.server =   xmlrpc.client.ServerProxy(self.url + ':' + self.port)

    def load_model(self):
        self.server.plecs.load(self.path)
    
    def ClearAllTraces(self,scopelist):
        for val in scopelist:
            self.server.plecs.scope(val,'ClearTraces')

    def Set_sim_param(self,mdlvars):
        self.modelvar = mdlvars
        # self.opts =  {'ModelVars' :  self.modelvar} 
        self.opts     = self.return_opts(self.parasim , self.paranum)
    
    def set_analysis_param(self,analysisvars):
        self.analysisvars = analysisvars
        self.analysisopts =  {'ModelVars' :  self.analysisvars }

    def launch_analysis(self,modelname):
        results = self.server.plecs.analyze(modelname, self.analysisName, self.analysisopts)
        return results
    
    def launch_sim(self,modelname):
        self.server.plecs.simulate(modelname, self.opts)

    def HoldAllTraces(self,scopelist):
        for val in scopelist:
            self.server.plecs.scope(val,'HoldTrace')

    def saveAllTraces(self,scopelist,mdl,path):
        for val in scopelist:
            self.server.plecs.scope(val, 'SaveTraces',path+"/"+ val[11:]+"_" +mdl.utc_numeric + "_.trace")

    def close_cnx(self,modelname):
        self.server.plecs.close(modelname) 

    def logParams(self,file_path, nested_dict):
        with open(file_path, 'a') as file:
            self.log_parameters(file, nested_dict, parent_keys=[])

    def log_parameters(self,file, nested_dict, parent_keys):
        for key, value in nested_dict.items():
            current_keys = parent_keys + [key]
            if isinstance(value, dict):
                self.log_parameters(file, value, current_keys)
                file.write("---------------------------------------------------------------------------------------------------\n")
            else:
                parent_path = "[" + "][".join(current_keys) + "]"
                file.write("{:<40}= {}\n".format(parent_path, value))

#?----------------------------------------------------------------------------------------------------------------------------------------