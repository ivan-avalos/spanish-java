class automata_cad:
    stateN = 0

    def isAccepted(self, _str):
        i = len(_str)
        _len = len(_str)

        for i in range(len):
            if self.stateN == 0:
                self.start(_str[i])
            if self.stateN == 1:
                self.state1(_str[i])
            if self.stateN == 2:
                self.state2(str[i])    
            else:
                return 0
        if self.stateN == 2
            return 1
        else:
            return 0
    
    def start(self, c):
        if (c == '\"'):
            self.stateN = 1
        else:
            self.stateN = -1
        
    def state1(self,c):
        if (c != '\"'):
            self.stateN = 1
        else:
            self.stateN = 2
    
    def state2(self,c):
        self.stateN = -1
    
    def verified(self,token)
    {
        if isAccepted(token):
            return true
        else:
            return false
    }