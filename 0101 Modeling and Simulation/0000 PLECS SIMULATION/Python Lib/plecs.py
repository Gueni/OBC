

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
    
    def ClearTrace(self,scopePath):
        """_summary_

        Args:
            scopePath (_type_): _description_
        """
        self.server.plecs.scope(scopePath,'ClearTraces')
    
    def ClearAllTraces(self,scopedict):
        """_summary_

        Args:
            scopedict (_type_): _description_
        """
        for val in scopedict:
            self.server.plecs.scope(val,'ClearTraces')

    def Set_sim_param(self):
        """_summary_
        """
        self.opts =  {'ModelVars' :  self.modelvar}

    def launch_sim(self,modelname):
        """_summary_
        """
        self.server.plecs.simulate(modelname, self.opts)

    def HoldTraces(self,scope):
        """_summary_
        """
        self.server.plecs.scope(scope,'HoldTrace')

    def HoldAllTraces(self,scopedict):
        """_summary_

        Args:
            scopedict (_type_): _description_
        """
        for key,val in scopedict:
            self.server.plecs.scope(val,'HoldTrace')

    def saveTraces(self,scope,ﬁleName):
        """_summary_
        """
        self.server.plecs.scope(scope, 'SaveTraces', ﬁleName)

    def saveAllTraces(self,scopedict,path):
        """_summary_

        Args:
            scopedict (_type_): _description_
        """
        for key,val in scopedict:
            self.server.plecs.scope(val, 'SaveTraces', path + key+".trace")

    def close_cnx(self,modelname):
        self.server.plecs.close(modelname) 

    def log_parameters(self,parameters_dict, file, parent_key=None, indentation=0):
        max_key_length = max(len(str(key)) for key in parameters_dict.keys())

        for key, value in parameters_dict.items():
            if isinstance(value, dict):
                self.log_parameters(value, file, key, indentation)
            else:
                file.write(f"[{parent_key}]{'[' + str(key) + ']'.ljust(max_key_length)} = {str(value)}\n")

    def interpolate_list(self,lst, max_length):
        start_value = lst[0]
        end_value = lst[-1]
        step = (end_value - start_value) // (len(lst) - 1)
        new_lst = [start_value + i * step for i in range(len(lst))]
        # Extend the list to match the maximum length
        new_lst.extend([end_value] * (max_length - len(lst)))
        return new_lst