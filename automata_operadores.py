class automata_operador:
    int stateN = 0
    int isAccepted(char str[]):

        int len = len(str)
        
        for i in len:
            if (stateN == 0):
                start(str[i])
            else: 
                if (stateN == 1):
                    state1(str[i])
                else: 
                    if (stateN == 2):
                        state2(str[i])
                    else: 
                        if (stateN == 3):
                            state3(str[i])
                        else: 
                            if (stateN == 4):
                                state4(str[i])
                            else: 
                                if (stateN == 5):
                                    state5(str[i])
                                else: 
                                    if (stateN == 6):
                                        state6(str[i])
                                    else: 
                                        if (stateN == 7):
                                            state7(str[i])
                                        else: 
                                            if (stateN == 8):
                                                state8(str[i])
                                            else:
                                                return 0

        if (stateN == 1 or stateN == 7 or stateN == 8 or stateN == 2 or stateN == 3 or stateN == 6):
            return 1
        else:
            return 0
    
    def start(char c):
        if(c == '=' or c == '>' or c == '<' or c == '/' or c == '*' or c == '%' or c == '!'):
            stateN = 1
        else: 
            if(c == '&'):
                stateN = 4
            else: 
                if(c == '|'):
                    stateN = 5
                else: 
                    if(c == '-'):
                        stateN = 6
                    else: 
                        if(c == '+'):
                            stateN = 3
                        else
                            stateN = -1
        
    def state1(char c):
        if(c == '='):
            stateN = 2
        else:
            stateN = -1
    
    def state2(char c):
        stateN = -1
    
    def state3(char c):
        if(c == '+'):
            stateN = 7
        else: 
            if(c == '=')
                stateN = 2
            else:
                stateN = -1
    
    def state4(char c):
        if(c == '&'):
            stateN = 2
        else:
            stateN = -1
    
    def state5(char c):
        if(c == '|'):
            stateN = 2
        else:
            stateN = -1
    
    def state6(char c):
        if(c == '-'):
            stateN = 8
        else: 
            if(c == '=')
                stateN = 2
            else
            stateN = -1
    
    def state7(char c):
        stateN = -1
    
    def state8(char c):
        stateN = -1
    
    bool verified(char* token):
        if (isAccepted(token)):
            return true
        else:
            return false
