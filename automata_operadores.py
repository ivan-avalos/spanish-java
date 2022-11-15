
class automata_ope:
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
                self.start4(_str[i])
            if self.stateN == 5:
                self.state5(_str[i])
            if self.stateN == 6:
                self.state6(_str[i])
            if self.stateN == 7:
                self.state7(_str[i])
            if self.stateN == 8:
                self.state8(_str[i])
            else:
                return 0
        if (self.stateN == 1 or self.stateN == 7 or self.stateN == 8 or self.stateN == 2 or self.stateN == 3 or self.stateN == 6):
            return 1
        else:
            return 0
    
    def start(self,c):
        if(c == '=' or c == '>' or c == '<' or c == '/' or c == '*' or c == '%' or c == '!'):
            self.stateN = 1
        else if(c == '&'):
            self.stateN = 4
        else if(c == '|'):
            self.stateN = 5
        else if(c == '-'):
            selfstateN = 6
        else if(c == '+'):
            selfstateN = 3
        else:
            self.stateN = -1
        
    def state1(self,c):
        if(c == '='):
            self.stateN = 2
        else:
            self.stateN = -1

    def state2(self,c):
        self.stateN = -1
    
    def state3(self,c):
        if(c == '+'):
            self.stateN = 7
        else if(c == '='):
            self.stateN = 2
        else:
            self.stateN = -1
    
    def state4(self,c):
        if(c == '&'):
            self.stateN = 2
        else:
            self.stateN = -1
    
    def state5(self,c):
        if(c == '|'):
            self.stateN = 2
        else:
            self.stateN = -1
    
    def state6(self,c):
        if(c == '-'):
            self.stateN = 8
        else if(c == '='):
            self.stateN = 2
        else:
            self.stateN = -1
    
    def state7(self,c):
        self.stateN = -1
    
    def state8(self,c):
        self.stateN = -1
    
    def verified(self,token):
        if isAccepted(token):
            return true
        else:
            return false