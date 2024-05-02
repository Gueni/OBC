
#?----------------------------------------------------------------------------------------------------------------------------------------
#?                                  ____  __    _________________    ________  ___   ________
#?                                 / __ \/ /   / ____/ ____/ ___/   / ____/ / / / | / / ____/
#?                                / /_/ / /   / __/ / /    \__ \   / /_  / / / /  |/ / /     
#?                               / ____/ /___/ /___/ /___ ___/ /  / __/ / /_/ / /|  / /___   
#?                              /_/   /_____/_____/\____//____/  /_/    \____/_/ |_/\____/  
#?                              
#?----------------------------------------------------------------------------------------------------------------------------------------
import xmlrpc.client
#?----------------------------------------------------------------------------------------------------------------------------------------
class simpy:
    
    def __init__(self,url,port,path,modelvar):
        self.url        =   url
        self.port       =   port
        self.path       =   path
        self.modelvar   =   modelvar
    
    def rpc_connect(self):
        self.server =   xmlrpc.client.ServerProxy(self.url + ':' + self.port)

    def load_model(self):
        self.server.plecs.load(self.path)
    
    def ClearAllTraces(self,scopelist):
        for val in scopelist:
            self.server.plecs.scope(val,'ClearTraces')

    def Set_sim_param(self):
        self.opts =  {'ModelVars' :  self.modelvar}

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
        with open(file_path, 'w') as file:
            self.log_parameters(file, nested_dict, parent_keys=[])

    def log_parameters(self,file, nested_dict, parent_keys):
        for key, value in nested_dict.items():
            current_keys = parent_keys + [key]
            if isinstance(value, dict):
                self.log_parameters(file, value, current_keys)
            else:
                parent_path = "[" + "][".join(current_keys) + "]"
                file.write("{:<40}= {}\n".format(parent_path, value))

#?----------------------------------------------------------------------------------------------------------------------------------------

