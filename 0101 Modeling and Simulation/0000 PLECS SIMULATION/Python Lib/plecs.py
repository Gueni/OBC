
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

    def log_parameters(self,parameters_dict, file, parent_key=None, indentation=0):
        max_key_length = max(len(str(key)) for key in parameters_dict.keys())

        for key, value in parameters_dict.items():
            if isinstance(value, dict):
                self.log_parameters(value, file, key, indentation)
            else:
                file.write(f"[{parent_key}]{'[' + str(key) + ']'.ljust(max_key_length)} = {str(value)}\n")

    def logParams(self,file,mdlvar) :
        with open(mdlvar['ToFile']['logfile'], "w") as file:
            self.log_parameters(mdlvar, file)
        file.close
#?----------------------------------------------------------------------------------------------------------------------------------------

