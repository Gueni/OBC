

import xmlrpc.client

class simpy:
    
    def __init__(self,url,port,path,modelvar):
        """_summary_

        Args:
            url (_type_): _description_
            port (_type_): _description_
            path (_type_): _description_
            modelvar (_type_): _description_
        """
        self.url        =   url
        self.port       =   port
        self.path       =   path
        self.modelvar   =   modelvar
    
    def rpc_connect(self):
        """_summary_
        """
        self.server =   xmlrpc.client.ServerProxy(self.url + ':' + self.port)

    def load_model(self):
        """_summary_
        """
        #add bloc to test if path is valid 
        self.server.plecs.load(self.path)
    
    def ClearAllTraces(self,scopelist):
        """_summary_

        Args:
            scopedict (_type_): _description_
        """
        for val in scopelist:
            self.server.plecs.scope(val,'ClearTraces')

    def Set_sim_param(self):
        """_summary_
        """
        self.opts =  {'ModelVars' :  self.modelvar}

    def launch_sim(self,modelname):
        """_summary_
        """
        self.server.plecs.simulate(modelname, self.opts)

    def HoldAllTraces(self,scopelist):
        """_summary_

        Args:
            scopedict (_type_): _description_
        """
        for val in scopelist:
            self.server.plecs.scope(val,'HoldTrace')

    def saveAllTraces(self,scopelist,path):
        """_summary_

        Args:
            scopedict (_type_): _description_
        """
        for val in scopelist:
            self.server.plecs.scope(val, 'SaveTraces',path+"/"+ val[11:]+".trace")

    def close_cnx(self,modelname):
        self.server.plecs.close(modelname) 

    def log_parameters(self,parameters_dict, file, parent_key=None, indentation=0):
        max_key_length = max(len(str(key)) for key in parameters_dict.keys())

        for key, value in parameters_dict.items():
            if isinstance(value, dict):
                self.log_parameters(value, file, key, indentation)
            else:
                file.write(f"[{parent_key}]{'[' + str(key) + ']'.ljust(max_key_length)} = {str(value)}\n")
