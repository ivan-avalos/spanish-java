class automata_ident:
    stateN = 0
    
    def isAccepted(self, _str):
        i = len(_str)
        _len = len(_str)
        
        for i in range(len):
            if self.stateN == 0:
                self.start(_str[i])
            if self.stateN == 1:
                self.state1(_str[i])
            else:
                return 0
        if self.stateN == 1:
            return 1
        else:
            return 0
    
    def start(self, c):
        if (c.isalpha() or c == '_'):
            self.stateN = 1
        else:
            self.stateN = -1
        
    def state1(self, c):
        if (c.isalpha() or c == '_' or c.isdigit()):
            self.stateN = 1
        else:
            self.stateN = -1
        
    def no_es_main(self,token):
        if isAccepted(token):
            return true
        else:
            return false