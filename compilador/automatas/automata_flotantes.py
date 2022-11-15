class automata_flot:
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
                self.state2(_str[i])
            if self.stateN == 3:
                self.state3(_str[i])
            if self.stateN == 4:
                self.state4(_str[i])
            if self.stateN == 5:
                self.state5(_str[i])		            
            else:
                return 0

        if self.stateN == 5:
            return 1
        else:
            return 0
    
    def start(self, c):
        if (c == '0'):
            self.stateN = 1
        else if(c == '-'):
            self.stateN = 2
        else if(c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or 
                    c == '6' or c == '7' or c == '8' or c == '9'):
            self.stateN = 3
        else:
            self.stateN = -1
        
    def state1(self,c):
        if (c == '.'):
            self.stateN = 4
        else:
            self.stateN = -1
    
    def state2(self,c):
        if(c == '0'):
            self.stateN = 1
        else if(c == '1' or c == '2' or c == '3' or c == '4' or c == '5' or 
                    c == '6' or c == '7' or c == '8' or c == '9'):
            self.stateN = 3
        else:
            self.stateN = -1
    
    def state3(self,c):
        if(c == '.'):
            self.stateN = 4
        else if c.isdigit():
            stateN = 3
        else:
            self.stateN = -1
    
    def state4(self,c):
        if c.isdigit():
            self.stateN = 5
        else:
            self.stateN = -1
    
    def state5(self,c):
        if c.isdigit():
            self.stateN = 5
        else:
            self.stateN = -1
    
    def verified(self,token):
        if isAccepted(token)
            return true
        else:
            return false